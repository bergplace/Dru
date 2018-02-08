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

from utils import split_list, log, prepare_block_list


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
        self.blocks_to_process = 512
        self.blockchain = []

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

    def create_block_chain(self):
        self.blockchain = []
        block = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        while block:
            self.blockchain.append(block)
            block = self.block_hash_chain.get(block[0], None)
            if len(self.blockchain) % 1000 == 0:
                log('{} blocks in blockchain'.format(len(self.blockchain)))
        self.blockchain = self.blockchain[:-self.verification_threshold]

    def save_blocks_parallel(self):
        log('blocks saving starts with {} processes'.format(self.n_processes))
        pool = Pool(processes=self.n_processes)
        while self.blockchain:
            processed = pool.map(prepare_block_list, split_list(
                self.blockchain[:self.blocks_to_process],
                self.n_processes
            ))
            log('saves {} blocks'.format(self.blocks_to_process))
            for blocks in processed:
                for block in blocks:
                    self.save_block(block)
            self.blockchain = self.blockchain[self.blocks_to_process:]

    def get_blocks_collection(self):
        mongo_container = 'btc-blockchain-db'
        log('connecting to mongo at: {}'.format(mongo_container))
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
        return connection.bitcoin.blocks

    def get_hash_of_last_saved_block(self):
        last_block = self.blocks_collection.find().sort([('_id', -1)]).limit(1)
        return last_block[0]['hash'] if last_block.count() != 0 else self.genesis_hash

    def save_one_block(self, block_info):
        b = get_block(block_info)
        start = time.time()
        b = block_to_dict(b)
        self.t_block_to_dict += time.time() - start
        self.save_block(b)
        log('block {} inserted to db'.format(block_info[0]))

    def save_block(self, block):
        self.blocks_collection.insert_one(block)

    def run(self):
        while True:
            self.refresh_block_data()
            self.create_block_chain()
            self.save_blocks_parallel()
            log('current collection count: {}'.format(self.blocks_collection.count()))
            log('sleeps for 10 minutes')
            time.sleep(600)


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
