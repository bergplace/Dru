import urllib.parse

from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder
import pymongo
from mongo_credentials import MONGO_PASS, MONGO_USER, MONGO_PORT


MONGO_HOST = "156.17.248.236"
MONGO_DB = "bitcoin"


class MongoConnection(object):
    """
    useful when cannot connect via port 27017
    """
    def __init__(self):
        self.host = '156.17.248.236'
        self.db = 'bitcoin'
        self.user = 'root'
        self.password = 'password'
        self.server = self.get_server()

    def get_server(self):
        return SSHTunnelForwarder(
            self.host,
            ssh_username=self.user,
            ssh_password=self.password,
            remote_bind_address=('127.0.0.1', 27017)
        )

    def get_connection(self):
        self.server.start()
        client = pymongo.MongoClient('127.0.0.1', self.server.local_bind_port)
        return client[self.db]

    def close_connection(self):
        self.server.stop()


def try_simple_connection():
    con = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    db = con[MONGO_DB]
    db.authenticate(MONGO_USER, MONGO_PASS)
    print(db.collection_names())


def try_with_uri():
    client = MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
        urllib.parse.quote_plus(MONGO_USER),
        urllib.parse.quote_plus(MONGO_PASS),
        MONGO_HOST,
        MONGO_PORT,
        MONGO_DB
    ))
    print(client[MONGO_DB].collection_names())
    return client


if __name__ == '__main__':
    try_with_uri()
    #try_simple_connection()
    #conn = MongoConnection().get_connection()
    #print(conn.collection_names())
