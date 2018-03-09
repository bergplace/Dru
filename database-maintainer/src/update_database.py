import time
import multiprocessing
import traceback
from collections import deque, defaultdict

from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from copy import copy
import mongo
from blockchain_parser_enchancements import block_to_dict, get_block
import os
from multiprocessing import Pool

from logger import Logger


class BlockchainDBMaintainer(object):
    """
    responsible for taking raw blocks from
    bitcoin data directory, and putting them
    in json format to MongoDB database
    """

    def __init__(self):
        self.logger = Logger()
        self.mongo = mongo.Mongo(self.logger)
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = defaultdict(set)
        self.checked_blk_files = set()
        self.blk_files_previous_sizes = {}
        self.files_with_unverified_blocks = set()
        self.verification_threshold = 6
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

    def run(self):
        """execution starts here"""
        while True:
            self.refresh_block_data()
            self.create_block_chain()
            self.check_data_validity()
            self.save_blocks_parallel_async()
            self.logger.log('current collection count: {}'.format(self.mongo.blocks_collection.count()))
            self.mongo.create_indexes()
            self.logger.log('sleeps for 10 minutes')
            time.sleep(600)

    def refresh_block_data(self):
        """
        creates dictionary that holds information about
        in witch blk file the block with specific block hash
        sits, and at witch position in blk file it is
        """
        self.logger.log('blocks data gathering starts')
        files_to_check = self.get_files_to_check()
        self.logger.log('files to check: {}'.format(files_to_check))
        for blk_i, blk_file in enumerate(files_to_check):
            for rb_i, raw_block in enumerate(get_blocks(blk_file)):
                b = Block(raw_block)
                self.block_hash_chain[b.header.previous_block_hash].add(
                    (b.hash, blk_file, rb_i)
                )
            self.logger.log('loading blockchain {0:.2f}% ready'.format(100 * blk_i / len(files_to_check)))
        self.logger.log('{} blocks to check'.format(len(self.block_hash_chain)))

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
        files_to_check = list(set(files_to_check) | self.files_with_unverified_blocks)
        self.files_with_unverified_blocks = set()
        return files_to_check

    def create_block_chain(self):
        """
        creates list of consecutive blocks starting with
        last block in database, and ending with block that
        have at least 'self.verification_threshold' blocks
        after it
        """
        self.blockchain = deque()
        block_hash, height = self.mongo.hash_and_height_of_last_saved_block
        block_info_set = self.block_hash_chain.get(block_hash, None)
        while block_info_set:
            height += 1
            block_info = self.chose_non_orphan(block_info_set)
            self.blockchain.append(list(block_info) + [height])
            block_info_set = self.block_hash_chain.get(block_info[0], None)

        for _ in range(self.verification_threshold):
            if len(self.blockchain) != 0:
                self.blockchain.pop()
        self.logger.log('{} blocks to upload'.format(len(self.blockchain)))

    def chose_non_orphan(self, block_info_set):
        """
        returns block_info of block that have at least self.verification_threshold
        following blocks, or block with longest branch
        """
        if len(block_info_set) == 1:
            return block_info_set.pop()
        depths = []
        for block_info in block_info_set:
            depths.append((block_info, self.get_max_branch_length([block_info], 0)))
        return max(depths, key=lambda x: x[1])[0]

    def get_max_branch_length(self, block_info_set, depth):
        max_depth = 0
        if depth > self.verification_threshold or block_info_set is None:
            return depth - 1
        for block_info in block_info_set:
            next_block_info_set = self.block_hash_chain.get(block_info[0])
            max_depth = max(
                max_depth,
                self.get_max_branch_length(next_block_info_set, depth + 1)
            )
        return max_depth

    def check_data_validity(self):
        """checks if block hashes are unique,
        and if paths and indexes are unique"""
        if (len(self.blockchain)
                != len({block_hash for (block_hash, _, _, _) in self.blockchain})):
            raise Exception('self.blockchain contains doubled hashes')
        if (len(self.blockchain)
                != len({(path, i) for (_, path, i, _) in self.blockchain})):
            raise Exception('self.blockchain contains doubled path and index')

    def save_blocks_parallel_async(self):
        """
        starts fixed number of asynchronous parallel tasks processing blocks,
        when task has finished, callback function is called
        """
        n_blocks_to_process = len(self.blockchain)
        self.logger.log('processing of {} blocks starts'.format(n_blocks_to_process))
        pool = Pool(processes=self.n_processes)
        for i, block_info in enumerate(copy(self.blockchain)):
            self.logger.log_processing(i, n_blocks_to_process)
            self.processes_count += 1
            pool.apply_async(
                self.process_single_block,
                (block_info, ),  # for some reason it has to be in tuple
                callback=self.process_result_callback
            )
            while (self.processes_count > self.process_count_limit or
                   len(self.processed_blocks) > self.process_count_limit):
                time.sleep(0.1)
        pool.close()
        pool.join()

    @staticmethod
    def process_single_block(block_info):
        """function to run in every worker"""
        result = None
        try:
            result = block_to_dict(*get_block(block_info))
        except:
            return block_info[0], result, traceback.format_exc()

        return block_info[0], result, None

    def process_result_callback(self, result):
        """
        callback function for tasks started by 'save_blocks_parallel_async'
        """
        self.processes_count -= 1
        block_hash, block, err = result

        if err:
            self.logger.log('ERROR IN BLOCK')
            self.logger.log(block_hash)
            self.logger.log(err)

        self.processed_blocks[block_hash] = block

        while True:
            block_to_save = self.processed_blocks.get(self.next_block_hash, None)
            if block_to_save is None:
                break
            self.mongo.save_block(self.next_block_hash, block_to_save)
            del self.processed_blocks[self.next_block_hash]
            self.blockchain.popleft()

    @property
    def next_block_hash(self):
        """returns hash of next block to save to db"""
        return self.blockchain[0][0]


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
