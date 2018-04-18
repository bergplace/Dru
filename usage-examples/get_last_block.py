from pprint import pprint

from mongo_connection import get_db_connection

db = get_db_connection()
block = db.blocks.find().sort([('height', -1)])[0]
#pprint(block)
print(block['height'], block['hash'])

tx = db.blocks.find({'transactions.hash': 'f4eeefa1218122b53d0969de1a7daab8b0c383929db1d1ad64c18a7282c64694'})[0]
for t in tx['transactions']:
    if t['hash'] == 'f4eeefa1218122b53d0969de1a7daab8b0c383929db1d1ad64c18a7282c64694':
        pprint(t)

tx = db.blocks.find({'transactions.hash': 'bb77f4a58e0c23a21f7a261255064acf69d939971f770b42d1f0d9839bdb469b'})[0]
for t in tx['transactions']:
    if t['hash'] == 'bb77f4a58e0c23a21f7a261255064acf69d939971f770b42d1f0d9839bdb469b':
        pprint(t)



