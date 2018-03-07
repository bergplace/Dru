import time
from mongo_connection import get_db_connection


def test_getting_blocks_with_height_between(db, lower_bound, upper_bound):
    start_t = time.time()
    blocks = []
    query = db.blocks.find({'height': {'$gte': lower_bound, '$lte': upper_bound}})
    for block in query:
        blocks.append(block)
    return time.time() - start_t


if __name__ == '__main__':
    db = get_db_connection()
    print(test_getting_blocks_with_height_between(db, 400000, 400001))
