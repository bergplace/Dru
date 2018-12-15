from coin_rpc.utils import RPC
from btc_block_iterator import BTCBlockIterator

from logger import Logger

zcash_url = 'http://localhost:8232'

zcash = RPC(zcash_url, 'user', 'pass')

print(zcash.getbestblockhash())
print('!!!!!!!!!!!!!!!!!!!!!!!!')

logger = Logger()

for block in BTCBlockIterator(zcash, logger):
    print(block)

