import time
import multiprocessing
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
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
        self.n_processes = multiprocessing.cpu_count()
        self.saving_time = 0
        self.rest_time = 0
        self.rounds = 0
        self.t_block_to_dict = 0
        self.blocks_to_process = 512
        self.blockchain = []
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
            self.save_blocks_parallel()
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
        self.blockchain = []
        block = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        while block:
            self.blockchain.append(block)
            block = self.block_hash_chain.get(block[0], None)
            if len(self.blockchain) % 1000 == 0:
                log('{} blocks in blockchain'.format(len(self.blockchain)))
        self.blockchain = self.blockchain[:-self.verification_threshold]

    def save_blocks_parallel(self):
        """
        will this work after getting to the head?
        or maybe when self.blockchain is 513 elements, will it work?

        parses blocks to json on every core machine have,
        and then saves them in database
        """
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
                    self.save_block_to_db(block)
            self.blockchain = self.blockchain[self.blocks_to_process:]

    def save_blocks_parallel_async(self):
        pool = Pool()
        while self.blockchain:
            self.processes_count += 1
            pool.apply_async() # one block in one process
            while (self.processes_count >= self.process_count_limit or
                   len(self.processed_blocks) > self.process_count_limit):
                time.sleep(0.1)

            self.blockchain = self.blockchain[self.blocks_to_process:]

    def process_result_callback(self, result):
        hash, block = result
        self.processed_blocks[hash] = block

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
