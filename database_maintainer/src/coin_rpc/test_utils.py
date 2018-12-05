from utils import RPC


zcash_url = 'http://127.0.0.1:8232'

zcash = RPC(zcash_url, 'user', 'pass')

print(zcash.getbestblockhash())
