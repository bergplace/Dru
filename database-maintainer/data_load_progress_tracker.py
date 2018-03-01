import time
import urllib.parse

from pymongo import MongoClient

mongo_container = 'btc-blockchain-db'
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('password')
connection = MongoClient('mongodb://{}:{}@{}'.format(username, password, mongo_container))
col = connection.bitcoin.blocks


def fun():
    height = 510000
    old = col.count()
    print('number of blocks inserted: {}'.format(old))
    time.sleep(100)
    while True:
        new = col.count()
        print('number of blocks inserted: {}, being {}% of all, and {}h left'.format(
            new, 
            str(100 * new / height)[:4],
            str(100 * (height - new) / ((new - old) * 3600))[:4]
        ))
        old = new
        time.sleep(100)

if __name__ == '__main__':
    fun()
