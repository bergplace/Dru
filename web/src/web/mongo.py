import os
import urllib.parse

from pymongo import MongoClient


class Mongo:
    @classmethod
    def db(cls, database_name=os.environ['MONGODB_NAME']):
        return MongoClient('mongodb://{}:{}@{}/{}'.format(
            urllib.parse.quote_plus(os.environ['MONGODB_READONLY_USER']),
            urllib.parse.quote_plus(os.environ['MONGODB_READONLY_PASS']),
            'mongo',
            database_name
        ))[database_name]
