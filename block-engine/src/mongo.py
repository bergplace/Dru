"""
Mongo handler
"""
import traceback
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
        self.create_indexes()

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
                database = connection[os.environ['CRYPTO']]
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
                roles=[{'role': 'read', 'db': os.environ['CRYPTO']}]
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
        last_block = self.collection.find().sort([('height', -1)]).limit(1)
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
        self.logger.info('creating height db index')
        self.collection.create_index([('height', ASCENDING)])
        self.logger.info('creating timestamp db index')
        self.collection.create_index([('timestamp', ASCENDING)])
        self.logger.info('creating tx hash db index')
        self.collection.create_index([('tx.txid', ASCENDING)])

    def get_tx_out_addr(self, tx_hash, out_index):
        """get_tx"""
        try:
            result = None
            result = self.collection.find_one(
                {'tx.txid': tx_hash},
                {'tx.vout.$': 1}
            )
            return result['tx'][0]['vout'][out_index]['scriptPubKey']['addresses']
        except Exception as e:
            self.logger.error(f'{traceback.format_exc()} '
                              f'for txid:index {tx_hash}:{out_index} '
                              f'querry result {result}')
            return []

