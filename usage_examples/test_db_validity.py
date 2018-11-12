from mongo_connection import get_db_connection

db = get_db_connection()

prev_block = {
    'hash': '0000000000000000000000000000000000000000000000000000000000000000'
}
height = -1

for block in db.blocks.find({}, {'hash': 1, 'prev_hash': 1, 'height': 1}).sort([('_id', 1)]):  # noqa
    height += 1
    print(height)
    if prev_block['hash'] != block['prev_hash'] or block['height'] != height:
        print(block)
        print(prev_block)
        break
    prev_block = block
