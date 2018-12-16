import os
from collections import deque


class TxCache:

    def __init__(self):
        self.tx_dict = dict()
        self.tx_queue = deque()
        self.limit = int(os.environ['TX_ADDRESS_CACHE_LIMIT'])

    def add(self, tx_hash, tx_outputs):
        tx_hash = int(tx_hash, 16)
        self.tx_dict[tx_hash] = tuple(tx_outputs)
        self.tx_queue.append(tx_hash)
        if len(self.tx_queue) > self.limit:
            del self.tx_dict[self.tx_queue.popleft()]

    def add_from_block(self, block):
        for tx in block['tx']:
            tx_outs = []
            for out in tx['vout']:
                tx_outs.append(tuple(out.get('scriptPubKey', {}).get('addresses', [])))
            self.add(tx['txid'], tx_outs)

    def get(self, tx_hash, out_nr):
        tx_outs = self.tx_dict.get(int(tx_hash, 16))
        if tx_outs and len(tx_outs) > out_nr:
            return tx_outs[out_nr]
        return None
