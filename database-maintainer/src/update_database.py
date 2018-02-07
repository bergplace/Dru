import time

import resource

import multiprocessing
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from collections import deque, defaultdict
from pymongo import MongoClient
from blockchain_parser_enchancements import block_to_dict, get_block
import os
import urllib.parse
import random
from multiprocessing import Pool
import numpy


"""
ok  zrobić w tej mojej strukturze tj block_hash_chain zamiast
    hashu dać raw_block, albo chociaż numer bloku w blk,
    generalnie optymalizacja pełną parą.



Może nabrać kilka bloków, a potem Pool.map zrobić współbierznie
tj mam listę hashy i nazw plików i może numerów bloku w pliku,
wrzucam do p.map i dostaję dicty, a potem je wysyłam


z tego słownika bloków można usówać wpisy po zapisaniu i otwarciu kolejnego

Wyniki:
8.435987043380738


SPRAWDZIĆ ŁĄCZNY CZAS PRZETWARZANIA NA DICTA
"""

TESTING = False


class BlockchainDBMaintainer(object):

    def __init__(self):
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.blk_files_previous_sizes = {}
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.verification_threshold = 6
        self.blocks_collection = self.get_blocks_collection()
        self.last_saved_block = self.get_hash_of_last_saved_block()
        self.n_processes = multiprocessing.cpu_count()
        self.saving_time = 0
        self.rest_time = 0
        self.rounds = 0
        self.t_block_to_dict = 0
        self.amount_of_blocks_procesed_at_once = 512

    def refresh_block_data(self):
        log('blocks data gathering starts')
        files_to_check = self.get_files_to_check()
        log('files to check: {}'.format(files_to_check))
        for blk_i, blk_file in enumerate(files_to_check):
            for rb_i, raw_block in enumerate(get_blocks(blk_file)):
                b = Block(raw_block)
                self.block_hash_chain[b.header.previous_block_hash] = [
                    b.hash, blk_file, rb_i
                ]
            log('{}% ready'.format(100 * blk_i / len(files_to_check)))

    def get_files_to_check(self):
        new_file_sizes = {path: os.path.getsize(path) for path in get_files(self.btc_data_dir_path)}
        files_to_check = []
        for file, size in new_file_sizes.items():
            if size != self.blk_files_previous_sizes.get(file, 0):
                files_to_check.append(file)
        self.blk_files_previous_sizes = new_file_sizes
        return files_to_check

    def save_blocks(self):
        log('blocks saving starts')
        block_queue = deque()
        next_block = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        while next_block:
            block_queue.append(next_block)
            if len(block_queue) >= self.verification_threshold:
                block_queue.popleft()
                self.save_one_block(block_queue[0])
            next_block = self.block_hash_chain.get(block_queue[-1][0], None)

    def save_blocks_parallel(self):
        log('blocks saving starts with {} processes'.format(self.n_processes))
        block_queue = deque()
        next_block = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        block_queue.append(next_block)
        pool = Pool(processes=self.n_processes)
        blocks_list = []
        while next_block:
            if len(block_queue) >= self.verification_threshold:
                blocks_list.append(block_queue.popleft())
                if len(blocks_list) >= self.amount_of_blocks_procesed_at_once:
                    processed = pool.map(prepare_block_list, self.split_list(blocks_list, self.n_processes))
                    log('saves {} blocks'.format(len(processed) * len(processed[0])))
                    for lst in processed:
                        for block in lst:
                            self.save_block(block)
            next_block = self.block_hash_chain.get(block_queue[-1][0], None)
            block_queue.append(next_block)

    def split_list(self, lst, n):
        splitted = []
        for i in reversed(range(1, n + 1)):
            split_point = len(lst)//i
            splitted.append(lst[:split_point])
            lst = lst[split_point:]
        return splitted

    def get_blocks_collection(self):
        if TESTING:
            return FakeMongoCollection()

        mongo_container = 'btc-blockchain-db'
        log('connecting to mongo at: {}'.format(mongo_container))
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
        return connection.bitcoin.blocks

    def get_hash_of_last_saved_block(self):
        hash_of_last = self.blocks_collection.find({}).sort([('height', -1)]).limit(1)
        return hash_of_last[0].hash if hash_of_last.count() != 0 else self.genesis_hash

    def save_one_block(self, block_info):
        b = get_block(block_info)
        start = time.time()
        b = block_to_dict(b)
        self.t_block_to_dict += time.time() - start
        self.save_block(b)
        log('block {} inserted to db'.format(block_info[0]))

    def save_block(self, block):
        self.blocks_collection.insert_one(block)

    def test_saving(self):
        """
        AVG TIME: 16.905670595169067
        AVG TIME: 14.144430899620057"""
        blocks = list(self.block_hash_chain.values())
        res = []
        for _ in range(10):
            try:
                start = time.time()
                for _ in range(100):
                    rand_block = random.choice(blocks)
                    self.save_one_block(rand_block)
                res.append(time.time() - start)
                print('PARTIAL TIME: {}, TO DICT: {}'.format(
                    time.time() - start,
                    self.t_block_to_dict
                ))
                self.t_block_to_dict = 0
            except RuntimeError:
                pass
        print('AVG TIME: {}'.format(sum(res)/len(res)))

    def test_saving_parallel(self):
        """
        AVG TIME: 14.166110968589782
        AVG TIME: 17.581450843811034
        """
        blocks = list(self.block_hash_chain.values())
        res = []
        p = Pool(processes=self.n_processes)
        for _ in range(10):
            try:
                start = time.time()
                rand_blocks = [[random.choice(blocks) for _ in range(25)] for _ in range(4)]
                p.map(prepare_block_list, rand_blocks)
                p.map(prepare_block_list, self.split_list(rand_blocks[0], self.n_processes))
                res.append(time.time() - start)
                print('PARTIAL TIME: {}'.format(time.time() - start))
            except RuntimeError:
                pass
        print('AVG TIME: {}'.format(sum(res) / len(res)))

    def run(self):
        #resource.setrlimit(resource.RLIMIT_AS, (4 * 10**9, 4 * 10**9))
        while True:
            if TESTING:
                self.btc_data_dir_path = '/home/marcin/blocks'
            self.refresh_block_data()
            if TESTING:
                self.test_saving_parallel()
                raise RuntimeError()
            self.save_blocks_parallel()
            log('current collection count: {}'.format(self.blocks_collection.count()))
            log('sleeps for 10 minutes')
            time.sleep(600)


def prepare_block_list(block_info_list):
    return list(map(lambda x: block_to_dict(get_block(x)), block_info_list))


def log(msg):
    if TESTING:
        return
    print('[db-maintainer][{}] {}'.format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        msg
    ))


class FakeMongoCollection(object):

    def insert_one(self, sth):
        pass

    def find(self, sth):
        return self

    def sort(self, sth):
        return self

    def limit(self, sth):
        return self

    def count(self):
        return 0


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
