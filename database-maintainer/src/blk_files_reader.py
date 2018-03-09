from collections import deque, defaultdict

import os

from blockchain_parser.block import Block
from blockchain_parser.blockchain import get_files, get_blocks


class BLKFilesReader(object):

    def __init__(self, logger, mongo):
        self.logger = logger
        self.mongo = mongo
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = defaultdict(set)
        self.checked_blk_files = set()
        self.blk_files_previous_sizes = {}
        self.files_with_unverified_blocks = set()
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
            next_block_info_set = self.block_hash_chain.get(block_info[0])
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
