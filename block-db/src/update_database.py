"""
Update database
"""
import logging
import time
import traceback

import os

from btc_block_iterator import BTCBlockIterator
from coin_rpc.utils import RPC

from output_addresses import OutputAddresses
import mongo


class BlockchainDBMaintainer:
    """
    responsible for taking raw blocks from
    bitcoin data directory, and putting them
    in json format to MongoDB database
    """

    def __init__(self):
        self.logger = logging.getLogger('block-db')
        self.mongo = mongo.Mongo(self.logger)
        self.rpc_connection = RPC('http://localhost:8232', 'user', 'pass')
        self.output_addresses = OutputAddresses(
            limit=int(os.environ['TX_ADDRESS_CACHE_LIMIT']),
            mongo=self.mongo,
            logger=self.logger
        )

    def run(self):
        """execution starts here"""
        while True:
            self.save_blocks()
            self.logger.info('current collection count: {}'.format(
                self.mongo.blocks_collection.count()
            ))
            self.mongo.create_indexes()
            self.logger.info('sleeps for 10 minutes')
            time.sleep(600)

    def save_blocks(self):
        """saves blocks"""
        for block in BTCBlockIterator(
                self.rpc_connection,
                self.logger,
                self.mongo.hash_of_last_saved_block):
            self.logger.info(f"saving block (hash: {block['hash']})")
            self.mongo.save_block(block)


if __name__ == '__main__':
    while True:
        try:
            BlockchainDBMaintainer().run()
        except Exception as e:
            traceback.print_exc()
            time.sleep(10)


