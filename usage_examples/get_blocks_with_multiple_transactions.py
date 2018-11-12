from pprint import pprint

from mongo_connection import get_db_connection

db = get_db_connection()

# checks if second element of array 'transactions' exists
blocks = db.blocks.find({'transactions.1': {'$exists': 1}})

if blocks.count() == 0:
    print('not found')
else:
    for block in blocks:
        pprint(block)
        print(block['height'], block['hash'])
