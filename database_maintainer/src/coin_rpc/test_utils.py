from utils import RPC


zcash_url = 'http://localhost:8232'

zcash = RPC(zcash_url, 'user', 'pass')

print(zcash.getbestblockhash())
