import time
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from collections import deque, defaultdict
from pymongo import MongoClient
import os
import urllib.parse


class BlockchainDBMaintainer(object):

    def __init__(self):
        self.btc_data_dir_path = '/btc-blocks-data'
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.blk_files_previous_sizes = {}
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.verification_threshold = 6
        self.blocks_collection = self.get_blocks_collection()
        self.last_saved_block = self.get_hash_of_last_saved_block()

    def refresh_block_data(self):
        log('blocks data gathering starts')
        new_files_sizes = {path: os.path.getsize(path) for path in get_files(self.btc_data_dir_path)}
        files_to_check = []
        for file, size in new_files_sizes.items():
            if size != self.blk_files_previous_sizes.get(file, 0):
                files_to_check.append(file)
        self.blk_files_previous_sizes = new_files_sizes
        for i, blk_file in enumerate(files_to_check):
            for raw_block in get_blocks(blk_file):
                b = Block(raw_block)
                self.block_hash_chain[b.header.previous_block_hash] = [
                    b.hash, blk_file
                ]
            log('{}% ready'.format(100 * i / len(files_to_check)))

    def save_blocks(self):
        log('blocks saving starts')
        block_queue = deque()
        next_block = self.block_hash_chain.get(self.get_hash_of_last_saved_block(), None)
        while next_block:
            block_queue.append(next_block)
            if len(block_queue) >= self.verification_threshold:
                block_queue.popleft()
                self.save_one_block(*block_queue[0])
            next_block = self.block_hash_chain.get(block_queue[-1][0], None)

    def get_blocks_collection(self):
        mongo_container = 'btc-blockchain-db'
        log('connecting to mongo at: {}'.format(mongo_container))
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('password')
        return MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))\
            .bitcoin\
            .blocks

    def get_hash_of_last_saved_block(self):
        hash_of_last = self.blocks_collection.find({}).sort([('height', -1)]).limit(1)
        return hash_of_last[0].hash if hash_of_last.count() != 0 else self.genesis_hash

    def save_one_block(self, block_hash, file_path):
        block = None
        for raw_block in get_blocks(file_path):
            b = Block(raw_block)
            if b.hash == block_hash:
                block = b
                break
        self.blocks_collection.insert_one(self.block_to_dict(block))
        log('block {} inserted to db'.format(block_hash))

    def block_to_dict(self, block):
        return {
            'hash': block.hash,
            'version': block.header.version,
            'height': block.height,
            'prev_hash': block.header.previous_block_hash,
            'merkle_root': block.header.merkle_root,
            'timestamp': block.header.timestamp,
            'n_tx': block.n_transactions,
            'size': block.size,
            'bits': block.header.bits,
            'nonce': block.header.nonce,
            'difficulty': block.header.difficulty,
            'transactions': [self.transaction_to_dict(tx) for tx in block.transactions]
        }

    def transaction_to_dict(self, tx):
        return {
            'hash': tx.hash,
            'version': tx.version,
            'locktime': tx.locktime,
            'inputs': [self.input_to_dict(tx_input) for tx_input in tx.inputs],
            'outputs': [self.output_to_dict(output) for output in tx.outputs],
        }

    def input_to_dict(self, tx_input):
        return {
            'sequence_number': tx_input.sequence_number,
            'script': tx_input.script.script,
            'value': tx_input.script.value,
        }

    def output_to_dict(self, output):
        return {
            'value': output.value,
            'script': output.script.script,
            'adresses': [self.adress_to_dict(addr) for addr in output.addresses],
        }

    def adress_to_dict(self, addr):
        return {
            'hash': addr.hash,
            'public_key': addr.public_key,
            'address': addr.address,
            'type': addr.type,
        }

    def run(self):
        while True:
            self.refresh_block_data()
            self.save_blocks()
            log('current collection count: {}'.format(self.blocks_collection.count()))
            log('sleeps for 10 minutes')
            time.sleep(600)


def log(msg):
    print('[db-maintainer][{}] {}'.format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        msg
    ))


def get_ip_of(container):
    while True:
        log('trying to discover database container ip')
        with open('/etc/hosts', 'r') as f:
            for line in f.readlines():
                if container in line.split() and line.split()[0]:
                    return line.split()[0]
        time.sleep(10)


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
