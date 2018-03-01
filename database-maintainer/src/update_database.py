import time
import multiprocessing
from collections import deque

from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from copy import deepcopy, copy
from pymongo import MongoClient
from blockchain_parser_enchancements import block_to_dict, get_block
import os
import urllib.parse
from multiprocessing import Pool
from utils import split_list, log


class BlockchainDBMaintainer(object):
    """
    responsible for taking raw blocks from
    bitcoin data directory, and putting them
    in json format to MongoDB database
    """

    def __init__(self):
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.blk_files_previous_sizes = {}
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.verification_threshold = 6
        self.blocks_collection = self.get_blocks_collection()
        self.last_saved_block = self.get_hash_of_last_saved_block()
        self.n_processes = multiprocessing.cpu_count() * 4
        self.saving_time = 0
        self.rest_time = 0
        self.rounds = 0
        self.t_block_to_dict = 0
        self.blocks_to_process = 512
        self.blockchain = deque()
        # for new async processing
        self.processes_count = 0
        self.process_count_limit = 100
        self.processed_blocks = dict()

    @staticmethod
    def get_blocks_collection():
        """
        connects to databases and returns MongoDB collection
        to work with
        """
        mongo_container = 'btc-blockchain-db'
        log('connecting to mongo at: {}'.format(mongo_container))
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
        return connection.bitcoin.blocks

    def get_hash_of_last_saved_block(self):
        last_block = self.blocks_collection.find().sort([('_id', -1)]).limit(1)
        return last_block[0]['hash'] if last_block.count() != 0 else self.genesis_hash

    def run(self):
        """execution starts here"""
        while True:
            self.refresh_block_data()
            self.create_block_chain()
            self.save_blocks_parallel_async()
            log('current collection count: {}'.format(self.blocks_collection.count()))
            log('sleeps for 10 minutes')
            time.sleep(600)

    def refresh_block_data(self):
        """
        creates dictionary that holds information about
        in witch blk file the block with specific block hash
        sits, and at witch position in blk file it is
        """
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
        """
        returns file paths of blk files that still need to be checked,
        it knows that by looking witch blk files had grown by size since
        last execution
        """
        new_file_sizes = {path: os.path.getsize(path) for path in get_files(self.btc_data_dir_path)}
        files_to_check = []
        for file, size in new_file_sizes.items():
            if size != self.blk_files_previous_sizes.get(file, 0):
                files_to_check.append(file)
        self.blk_files_previous_sizes = new_file_sizes
        return files_to_check

    def create_block_chain(self):
        """
        creates list of consecutive blocks starting with
        last block in database, and ending with block that
        have at least 'self.verification_threshold' blocks
        after it
        """
        self.blockchain = deque()
        block_info = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        while block_info:
            self.blockchain.append(block_info)
            block_info = self.block_hash_chain.get(block_info[0], None)
            if len(self.blockchain) % 1000 == 0:
                log('{} blocks in blockchain'.format(len(self.blockchain)))
        for _ in range(self.verification_threshold):
            if len(self.blockchain) != 0:
                self.blockchain.pop()

    def save_blocks_parallel_async(self):
        pool = Pool(processes=self.n_processes)
        for block_info in copy(self.blockchain):
            self.processes_count += 1
            pool.apply_async(
                self.process_single_block,
                block_info,
                callback=self.process_result_callback
            )
            while (self.processes_count > self.process_count_limit or
                   len(self.processed_blocks) > self.process_count_limit):
                time.sleep(0.2)

            self.blockchain = self.blockchain[self.blocks_to_process:]

    @staticmethod
    def process_single_block(block_info):
        return block_info[0], block_to_dict(get_block(block_info))

    def process_result_callback(self, result):
        self.processes_count -= 1
        (block_hash, _, _), block = result
        self.processed_blocks[block_hash] = block
        block_to_save = self.processed_blocks.get(self.blockchain[0], None)
        if block_to_save:
            self.save_block_to_db(block_to_save)
            del self.processed_blocks[self.blockchain[0]]
            self.blockchain.popleft()

    def save_block_to_db(self, block):
        self.blocks_collection.insert_one(block)


def prepare_block_list(block_info_list):
    """
    this function is executed by every worker
    it takes list of blocks to process, and returns list of processed blocks

    elements the list of blocks it gets are in the form of file path to blk file
    and position of block in that file
    """
    return list(map(lambda x: block_to_dict(get_block(x)), block_info_list))


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
