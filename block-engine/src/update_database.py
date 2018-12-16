"""
Update database
"""
import time
import traceback

import os

from btc_block_iterator import BTCBlockIterator
from coin_rpc.utils import RPC
from logger import Logger

from output_addresses import OutputAddresses
import mongo
from tx_cache import TxCache
from tx_resolve import resolve_input_addresses


class BlockchainDBMaintainer:
    """
    responsible for inserting blocks from cryptocurency node
    to mongoDB and resolving transaction input addresses
    """

    def __init__(self):
        self.logger = Logger()
        self.mongo = mongo.Mongo(self.logger)
        self.rpc_connection = RPC()
        self.tx_cache = TxCache()
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
            self.logger.info('sleeps for 100 seconds')
            time.sleep(100)

    def save_blocks(self):
        """saves blocks"""
        for block in BTCBlockIterator(
                self.rpc_connection,
                self.logger,
                self.mongo.hash_of_last_saved_block):
            if block['height'] % 100 == 0:
                self.logger.info(f"saving block (height: {block['height']})")
            resolve_input_addresses(block, self.tx_cache, self.mongo)
            self.tx_cache.add_from_block(block)
            self.mongo.save_block(block)


if __name__ == '__main__':
    while True:
        try:
            BlockchainDBMaintainer().run()
        except Exception as e:
            traceback.print_exc()
            time.sleep(10)

