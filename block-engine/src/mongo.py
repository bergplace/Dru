"""
Mongo handler
"""

from urllib.parse import quote_plus  # pylint: disable=no-name-in-module
import time
import os

from pymongo import MongoClient, ASCENDING  # pylint: disable=import-error
from pymongo.errors import OperationFailure, DuplicateKeyError  # noqa pylint: disable=import-error

from constants import GENESIS_HASH


class DBIntegrityException(Exception):
    """custom db integrity exception"""
    pass


class Mongo:
    """
    responsible for actions on mongo database, and for
    keeping data valid
    """

    def __init__(self, logger):
        self.logger = logger
        self.database = self.establish_connection()
        self.collection = self.database.blocks
        self.saved_blocks_hashes = set()
        self.add_readonly_user()
        self.indexes_created = False
        self.output_addresses_index_created = False

    def establish_connection(self):
        """establish_connection"""
        while True:
            try:
                mongo_container = 'localhost'
                self.logger.info('connecting to mongo at: {}'.format(
                    mongo_container
                ))
                username = quote_plus(os.environ['MONGODB_ADMIN_USER'])
                password = quote_plus(os.environ['MONGODB_ADMIN_PASS'])
                connection = MongoClient('mongodb://{}:{}@{}'.format(
                    username, password, mongo_container
                ))
                database = connection['bitcoin']
                return database
            except OperationFailure as exception:
                self.logger.error('error {}, retrying in 1s'.format(exception))
                time.sleep(1)

    def add_readonly_user(self):
        """add_readonly_user"""
        try:
            self.database.command(
                "createUser",
                os.environ['MONGODB_READONLY_USER'],
                pwd=os.environ['MONGODB_READONLY_PASS'],
                roles=[{'role': 'read', 'db': 'bitcoin'}]
            )
        except DuplicateKeyError:
            pass

    @property
    def blocks_collection(self):
        """blocks_collection"""
        return self.collection

    @property
    def hash_and_height_of_last_saved_block(self):
        """hash_and_height_of_last_saved_block"""
        last_block = self.collection.find().sort([('_id', -1)]).limit(1)
        if last_block.count() != 0:
            return last_block[0]['hash'], last_block[0]['height']
        return GENESIS_HASH, -1

    @property
    def hash_of_last_saved_block(self):
        return self.hash_and_height_of_last_saved_block[0]

    def save_block(self, block):
        """save_block"""
        if block['hash'] in self.saved_blocks_hashes:
            raise DBIntegrityException(
                'Block Hash not unique for block {}'.format(
                    block['hash']
                )
            )
        self.saved_blocks_hashes.add(block['hash'])
        self.collection.insert_one(block)

    def check_hash_uniqueness(self, block_hash):
        """check_hash_uniqueness"""
        return block_hash not in self.saved_blocks_hashes

    def create_indexes(self):
        """create_indexes"""
        if not self.indexes_created:
            self.logger.info('creating height db index')
            self.collection.create_index([('height', ASCENDING)])
            self.logger.info('creating timestamp db index')
            self.collection.create_index([('timestamp', ASCENDING)])
            self.indexes_created = True

    def create_tx_hash_index(self):
        """create_tx_hash_index"""
        self.logger.info('creating tx hash db index')
        self.collection.create_index([('transactions.hash', ASCENDING)])
        self.output_addresses_index_created = True

    def get_tx(self, tx_hash):
        """get_tx"""
        if not self.output_addresses_index_created:
            self.create_tx_hash_index()
        return self.collection.find_one(
            {'transactions.hash': tx_hash},
            {'transactions.$': 1, 'timestamp': 1}
        )
