import time
from pprint import pprint

from mongo_connection import get_db_connection


def test_getting_blocks_with_height_between(db, lower_bound, upper_bound):
    """
    result 7.03.2018 for 400000 to 400099: 103.1s
    """
    start_t = time.time()
    blocks = []
    query = db.blocks.find({'height': {'$gte': lower_bound, '$lte': upper_bound}})
    for block in query:
        print(block['hash'])
        blocks.append(block)
    return time.time() - start_t


def test_getting_one_block(db, height):
    start_t = time.time()
    block = db.blocks.find_one({'height': height})
    pprint(block)
    return time.time() - start_t


if __name__ == '__main__':
    db = get_db_connection()
    #print(test_getting_blocks_with_height_between(db, 200000, 200099))
    print(test_getting_one_block(db, 299586))
