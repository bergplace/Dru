import urllib.parse

import time

import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure


class DBIntegrityException(Exception):
    pass


class Mongo(object):
    """
    responsible for actions on mongo database, and for
    keeping data valid
    """

    def __init__(self, logger):
        self.logger = logger
        self.connection = self.establish_connection()
        self.collection = self.connection.bitcoin.blocks
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.saved_blocks_hashes = set()
        self.add_readonly_user()
        self.indexes_created = False

    def establish_connection(self):
        while True:
            try:
                mongo_container = 'btc-blockchain-db'
                self.logger.log('connecting to mongo at: {}'.format(mongo_container))
                username = urllib.parse.quote_plus(os.environ['MONGODB_ADMIN_USER'])
                password = urllib.parse.quote_plus(os.environ['MONGODB_ADMIN_PASS'])
                connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
                return connection
            except OperationFailure as e:
                self.logger.log('error {}, retrying in 1s'.format(e))
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
    def hash_and_height_of_last_saved_block(self):
        last_block = self.collection.find().sort([('_id', -1)]).limit(1)
        if last_block.count() != 0:
            return last_block[0]['hash'], last_block[0]['height']
        return self.genesis_hash, -1

    def save_block(self, block_hash, block):
        if block_hash in self.saved_blocks_hashes:
            raise DBIntegrityException('Block Hash not unique for block {}'.format(
                block_hash
            ))
        self.saved_blocks_hashes.add(block_hash)
        self.collection.insert_one(block)

    def check_hash_uniqueness(self, block_hash):
        return block_hash not in self.saved_blocks_hashes

    def create_indexes(self):
        if self.collection.count() > 500000 and not self.indexes_created:
            self.logger.log('creating height db index')
            self.collection.create_index([('height', ASCENDING)])
            self.logger.log('creating timestamp db index')
            self.collection.create_index([('timestamp', ASCENDING)])
            self.indexes_created = True

