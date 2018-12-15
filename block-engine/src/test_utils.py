from coin_rpc.utils import RPC
from btc_block_iterator import BTCBlockIterator


zcash_url = 'http://localhost:8232'

zcash = RPC(zcash_url, 'user', 'pass')

print(zcash.getbestblockhash())
print('!!!!!!!!!!!!!!!!!!!!!!!!')

for block in BTCBlockIterator(zcash):
    print(block)

