import urllib

from pymongo import MongoClient


def get_blocks_collection():
    """
    connects to databases and returns MongoDB collection
    to work with
    """
    mongo_container = 'btc-blockchain-db'
    username = urllib.parse.quote_plus('btc-user')
    password = urllib.parse.quote_plus('btc-pass')
    connection = MongoClient(
        'mongodb://{}:{}@{}'.format(username, password, mongo_container)
    )
    return connection.bitcoin.blocks
