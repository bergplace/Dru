"""
Update database
"""
import time
import traceback

from btc_block_iterator import BTCBlockIterator
from coin_rpc.utils import RPC
from logger import Logger

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

    def run(self):
        """execution starts here"""
        while True:
            start_time = time.time()
            self.save_blocks()
            self.logger.info('current collection count: {}'.format(
                self.mongo.blocks_collection.count()
            ))
            time.sleep(max(0, 100 - int(time.time() - start_time)))

    def save_blocks(self):
        """saves blocks"""
        for block in BTCBlockIterator(
                self.rpc_connection,
                self.logger,
                self.mongo.hash_of_last_saved_block):
            if block['height'] % 100 == 0:
                self.logger.info(f"saving block (height: {block['height']})")
            self.tx_cache.add_from_block(block)
            resolve_input_addresses(block, self.tx_cache, self.mongo, self.logger)
            self.mongo.save_block(block)


if __name__ == '__main__':
    while True:
        try:
            BlockchainDBMaintainer().run()
        except Exception as e:
            traceback.print_exc()
            time.sleep(10)


