import urllib.parse

from pymongo import MongoClient
from mongo_credentials import MONGO_PASS, MONGO_USER, MONGO_PORT, MONGO_HOST

MONGO_DB = "bitcoin"


def get_db_connection():
    client = MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
        urllib.parse.quote_plus(MONGO_USER),
        urllib.parse.quote_plus(MONGO_PASS),
        MONGO_HOST,
        MONGO_PORT,
        MONGO_DB
    ))
    return client[MONGO_DB]


if __name__ == '__main__':
    get_db_connection()
    # try_simple_connection()
    # conn = MongoConnection().get_connection()
    # print(conn.collection_names())
