from collections import deque, defaultdict

import os

import time
from blockchain_parser.block import Block
from blockchain_parser.blockchain import get_files, get_blocks

from block_info import BlockInfo


class BLKFilesReader(object):

    def __init__(self, logger, mongo):
        self.logger = logger
        self.mongo = mongo
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = defaultdict(set)
        self.time_of_last_file_checking = 0
        self.blk_files_previous_sizes = {}
        self.verification_threshold = 6
        self.blockchain = deque()

    def get_ordered_blocks(self):
        """
        returns sequence of block_info starting from next
        to load to db, to last verified block
        """
        self.refresh_block_data()
        self.create_block_chain()
        self.check_data_validity()
        return self.blockchain

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
                    BlockInfo(hash=b.hash, path=blk_file,
                              index=rb_i, height=-1)
                )
            self.logger.log('loading blk files {0:.2f}% ready'.format(100 * blk_i / len(files_to_check)))
        self.logger.log('{} blocks in blocks directory'.format(len(self.block_hash_chain)))

    def get_files_to_check(self):
        """
        returns file paths of blk files that still need to be checked
        """
        new_time_of_last_file_checking = time.time()
        files_to_check = []
        for path in get_files(self.btc_data_dir_path):
            if os.path.getmtime(path) > self.time_of_last_file_checking:
                files_to_check.append(path)
        self.time_of_last_file_checking = new_time_of_last_file_checking
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
        block_info_set = self.block_hash_chain.get(block_hash)
        while block_info_set:
            height += 1
            block_info = self.chose_non_orphan(block_info_set)
            block_info.height = height
            self.blockchain.append(block_info)
            block_info_set = self.block_hash_chain.get(block_info.hash)

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
            depths.append((block_info, self.get_max_branch_length({block_info}, 0)))
        return max(depths, key=lambda x: x[1])[0]

    def get_max_branch_length(self, block_info_set, depth):
        """
        returns maximal depth that branch reaches, or self.verification_threshold
        if it goes deep enough
        """
        max_depth = 0
        if depth > self.verification_threshold or block_info_set is None:
            return depth - 1
        for block_info in block_info_set:
            next_block_info_set = self.block_hash_chain.get(block_info.hash)
            max_depth = max(
                max_depth,
                self.get_max_branch_length(next_block_info_set, depth + 1)
            )
        return max_depth

    def check_data_validity(self):
        """checks if block hashes are unique,
        and if paths and indexes are unique"""
        # checks if hashes are unique
        if (len(self.blockchain)
                != len({block_hash for (block_hash, _, _, _) in self.blockchain})):
            raise Exception('self.blockchain contains doubled hashes')

        # checks if paths and indexes are unique
        if (len(self.blockchain)
                != len({(path, i) for (_, path, i, _) in self.blockchain})):
            raise Exception('self.blockchain contains doubled path and index')
