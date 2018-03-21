from pprint import pprint

from mongo_connection import get_db_connection

db = get_db_connection()
block = db.blocks.find().sort([('height', -1)])[0]
pprint(block)
print(block['height'], block['hash'])