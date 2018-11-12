"""
Update database
"""

import time

import os

from blk_files_reader import BLKFilesReader
from blockchain_parser_enchancements import BlockToDict, get_block  # noqa

from logger import Logger
from output_addresses import OutputAddresses
import mongo


class BlockchainDBMaintainer:
    """
    responsible for taking raw blocks from
    bitcoin data directory, and putting them
    in json format to MongoDB database
    """

    def __init__(self):
        self.logger = Logger()
        self.mongo = mongo.Mongo(self.logger)
        self.blk_files_reader = BLKFilesReader(self.logger, self.mongo)
        self.output_addresses = OutputAddresses(
            limit=int(os.environ['TX_ADDRESS_CACHE_LIMIT']),
            mongo=self.mongo,
            logger=self.logger
        )
        self.block_to_dict = BlockToDict(self.output_addresses)
        self.blockchain = None

    def run(self):
        """execution starts here"""
        while True:
            self.blockchain = self.blk_files_reader.get_ordered_blocks()
            self.save_blocks()
            self.logger.log('current collection count: {}'.format(
                self.mongo.blocks_collection.count()
            ))
            self.mongo.create_indexes()
            self.logger.log('sleeps for 10 minutes')
            time.sleep(600)

    def save_blocks(self):
        """saves blocks"""
        n_blocks_to_process = len(self.blockchain)
        self.logger.log(
            'processing of {} blocks starts'.format(n_blocks_to_process)
        )
        for i, block_info in enumerate(self.blockchain):
            self.logger.log_processing(i, n_blocks_to_process)
            block_to_save = self.block_to_dict.transform(
                *get_block(block_info)
            )
            self.mongo.save_block(block_info.hash, block_to_save)


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
