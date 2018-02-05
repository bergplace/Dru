import time
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from collections import deque
from pymongo import MongoClient
import os
import urllib.parse

"""
TODO:
saving blocks - mirror the structure of block from blockchain.info
initializing db - creating indexes
fix getting info about totally processed blk files
switch from using depreciated links to using bridge network
"""


class BlockchainDBMaintainer(object):

    def __init__(self):
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.last_verified = self.genesis_hash   # mam last saved więc to nie będzie potrzxebne
        self.verification_threshold = 6
        self.blocks_collection = self.get_blocks_collection()
        self.last_saved_block = self.get_hash_of_last_saved_block()

    def refresh_block_data(self):
        log('blocks data gathering starts')
        # check all blk files that are 128Mb
        # process all of them and after, add them as checked
        files_to_check = sorted(set(get_files(self.btc_data_dir_path))  # there is bug
                                - self.checked_blk_files)
        self.checked_blk_files = set(files_to_check) | self.checked_blk_files
        for i, blk_file in enumerate(files_to_check):
            for raw_block in get_blocks(blk_file):
                b = Block(raw_block)
                self.block_hash_chain[b.header.previous_block_hash] = [
                    b.hash, blk_file, False
                ]
            log('{}% ready'.format(100 * i / len(files_to_check)))

    def save_blocks(self):
        log('blocks saving starts')
        block_queue = deque()
        next_block = self.block_hash_chain.get(self.last_verified, None)
        while next_block:
            block_queue.append(next_block)
            if len(block_queue) >= self.verification_threshold:
                block_queue.popleft()
                self.last_verified = block_queue[0]
                self.last_verified[2] = True
                self.save_one_block(self.last_verified)
            next_block = self.block_hash_chain.get(block_queue[-1][0], None)

    def get_blocks_collection(self):
        mongo_ip = os.environ['BTC_BLOCKCHAIN_DB_PORT_27017_TCP_ADDR']
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        return MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_ip))\
            .bitcoin\
            .blocks

    def get_hash_of_last_saved_block(self):
        hash_of_last = self.blocks_collection.find({}).sort([('height', -1)]).limit(1)
        return hash_of_last[0].hash if hash_of_last.count() != 0 else self.genesis_hash

    def save_one_block(self, block_hash, file_path):
        block = None
        for b in get_blocks(file_path):
            if b.hash == block_hash:
                block = b
                break
        self.blocks_collection.insert_one(self.block_to_dict(block))

    def block_to_dict(self, block):
        block_dict = {
            'hash': block.hash,
            'height': block.height,
            'prev_hash': block.header.previous_block_hash,
            'version': block.header.version,
            'merkle_root': block.header.merkle_root,
            'timestamp': block.header.timestamp,
            'difficulty': block.header.difficulty,
            'transactions': None # trochę się niechce już dzisiaj ;)
        }

    def run(self):
        log(str(self.get_hash_of_last_saved_block().count()))
        while True:
            self.refresh_block_data()
            self.save_blocks()

            log('sleeps for 10 minutes')
            time.sleep(600)


def log(msg):
    print('[db-maintainer][{}] {}'.format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        msg
    ))


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
