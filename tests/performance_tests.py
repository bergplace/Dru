import time
from datetime import datetime
from pprint import pprint

from mongo_connection import get_db_connection


def test_getting_blocks_with_height_between(db, lower_bound, upper_bound):
    start_t = time.time()
    blocks = []
    query = db.blocks.find({'height': {'$gte': lower_bound, '$lte': upper_bound}})
    for block in query:
        blocks.append(block)
    return time.time() - start_t


def test_getting_n_wide_spread_blocks_between(db, n, lower_bound, upper_bound):
    start_t = time.time()
    step = int((upper_bound - lower_bound) / n)

    for height in range(lower_bound, upper_bound + 1, step):
        db.blocks.find_one({'height': height})
    return time.time() - start_t


def test_getting_blocks_with_time_between(db, lower_bound, upper_bound):
    start_t = time.time()
    blocks = []
    query = db.blocks.find({'timestamp': {'$gte': lower_bound, '$lte': upper_bound}})
    for block in query:
        blocks.append(block)
    return time.time() - start_t


if __name__ == '__main__':
    db = get_db_connection()

    # performance of fetching blocks by timestamp
    print(test_getting_blocks_with_time_between(
        db,
        datetime(2016, 2, 25, 16, 24, 0),
        datetime(2016, 2, 26, 7, 23, 0)
    ))

    # performance of consecutive blocks fetching
    print('blocks between height 0 - 99')
    print(test_getting_blocks_with_height_between(db, 0, 99))
    print('blocks between height 100000 - 100099')
    print(test_getting_blocks_with_height_between(db, 100000, 100099))
    print('blocks between height 200000 - 200099')
    print(test_getting_blocks_with_height_between(db, 200000, 200099))
    print('blocks between height 300000 - 300099')
    print(test_getting_blocks_with_height_between(db, 300000, 300099))
    print('blocks between height 400000 - 400099')
    print(test_getting_blocks_with_height_between(db, 400000, 400099))

    # performance of not consecutive blocks fetching
    print('100 blocks spread between height 0 - 100000')
    print(test_getting_n_wide_spread_blocks_between(db, 100, 0, 100000))
    print('100 blocks spread between height 100000 - 200000')
    print(test_getting_n_wide_spread_blocks_between(db, 100, 100000, 200000))
    print('100 blocks spread between height 200000 - 300000')
    print(test_getting_n_wide_spread_blocks_between(db, 100, 200000, 300000))
    print('100 blocks spread between height 300000 - 400000')
    print(test_getting_n_wide_spread_blocks_between(db, 100, 300000, 400000))

