import os
import urllib.parse

from pymongo import MongoClient


class Mongo:
    _connections = {}

    @classmethod
    def db(cls, database_name):
        if database_name in cls._connections:
            return cls._connections[database_name][database_name]
        cls._connections[database_name] = MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
            urllib.parse.quote_plus(os.environ['MONGODB_READONLY_USER']),
            urllib.parse.quote_plus(os.environ['MONGODB_READONLY_PASS']),
            os.environ['MONGODB_HOST'],
            os.environ['MONGODB_PORT'],
            database_name
        ))
        return cls._connections[database_name][database_name]
