import time
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from collections import deque
from pymongo import MongoClient
import os
import urllib.parse

"""
General description:

on start:
    gather block info
loop:
    get hash of last block in db
    check in witch file next valid block is
    if there is no such information 
        update block info
        and check in witch file next valid block is
    load it to db
    
problems:
    not verified blocks, get only those confirmed
    by 5 other
    
    
structure of block info:

    {previous_block_hash: (this_block_hash, filename)}
"""


class BlockchainDBMaintainer(object):

    def __init__(self):
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.last_verified = self.genesis_hash
        self.verification_threshold = 6
        self.blocks = self.get_blocks_collection()

    def refresh_block_data(self):
        log('blocks data gathering starts')
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

    def verify_blocks(self):
        log('blocks verification starts')
        block_queue = deque()
        next_block = self.block_hash_chain.get(self.last_verified, None)
        bc_length = len(self.block_hash_chain)
        counter = 0
        while next_block:
            counter += 1
            if counter % 100 == 0:
                log('{}%'.format(counter/bc_length))
            block_queue.append(next_block)
            self.last_verified = block_queue[0]
            self.last_verified[2] = True
            if len(block_queue) >= self.verification_threshold:
                block_queue.popleft()
            next_block = self.block_hash_chain.get(block_queue[-1][0], None)

    def get_blocks_collection(self):
        mongo_ip = os.environ['BTC_BLOCKCHAIN_DB_PORT_27017_TCP_ADDR']
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        return MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_ip))\
            .bitcoin\
            .blocks

    def get_hash_of_last_saved_block(self):
        hash_of_last = self.blocks.find({}).sort([('height', -1)]).limit(1)
        return hash_of_last[0] if hash_of_last.count() != 0 else None

    def run(self):
        log(str(self.get_hash_of_last_saved_block().count()))
        while True:
            self.refresh_block_data()
            self.verify_blocks()
            log('sleeps for 10 minutes')
            time.sleep(600)


def log(msg):
    print('[db-maintainer][{}] {}'.format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        msg
    ))


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
