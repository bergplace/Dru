from collections import deque
from pprint import pprint

import constants


class OutputAddresses(object):

    def __init__(self, limit):
        self.limit = limit
        self.addresses = dict()
        self.dict_keys_queue = deque()

    def add_from_outputs(self, tx_hash, timestamp, outputs):
        self.dict_keys_queue.append(tx_hash)
        if len(self.dict_keys_queue) > self.limit:
            del self.addresses[self.dict_keys_queue.popleft()]

        self.addresses[tx_hash] = (timestamp, [out['addresses'] for out in outputs])

    def get(self, tx_hash, index):
        if tx_hash == constants.genesis_hash:
            return None, None
        addresses = self.addresses.get(tx_hash)
        if addresses:
            timestamp, outputs = addresses
            return timestamp, outputs[index]
        print(tx_hash)
        print('NOT FOUND, FUCK!')
