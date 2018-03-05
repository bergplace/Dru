import urllib.parse

import time

import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure

from utils import log


class DBIntegrityException(Exception):
    pass


class Mongo(object):
    """
    responsible for actions on mongo database, and for
    keeping data valid
    """

    def __init__(self):
        self.connection = self.establish_connection()
        self.collection = self.connection.bitcoin.blocks
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.saved_blocks_hashes = set()
        self.add_readonly_user()

    @staticmethod
    def establish_connection():
        while True:
            try:
                mongo_container = 'btc-blockchain-db'
                log('connecting to mongo at: {}'.format(mongo_container))
                username = urllib.parse.quote_plus(os.environ['MONGODB_ADMIN_USER'])
                password = urllib.parse.quote_plus(os.environ['MONGODB_ADMIN_PASS'])
                connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
                return connection
            except OperationFailure as e:
                log('error {}, retrying in 1s'.format(e))
                time.sleep(1)

    def add_readonly_user(self):
        self.connection.bitcoin.add_user(
            os.environ['MONGODB_READONLY_USER'],
            os.environ['MONGODB_READONLY_PASS'],
            roles=[{'role': 'read', 'db': 'bitcoin'}]
        )

    @property
    def blocks_collection(self):
        return self.collection

    @property
    def hash_of_last_saved_block(self):
        last_block = self.collection.find().sort([('_id', -1)]).limit(1)
        return last_block[0]['hash'] if last_block.count() != 0 else self.genesis_hash

    def save_block(self, block_hash, block):
        if block_hash in self.saved_blocks_hashes:
            raise DBIntegrityException('Block Hash not unique for block {}'.format(
                block_hash
            ))
        self.saved_blocks_hashes.add(block_hash)
        self.collection.insert_one(block)

    def check_hash_uniqueness(self, block_hash):
        return block_hash not in self.saved_blocks_hashes
