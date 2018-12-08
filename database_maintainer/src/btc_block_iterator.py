

class BTCBlockIterator:

    def __init__(self, connection, start_hash=None, verification_threshold=6):
        self.connection = connection
        self.start_hash = start_hash
        self.verification_threshold = verification_threshold
        self.blockchain = []
        self.recreate_blockchain()
        self.current_hash_index = len(self.blockchain) - self.verification_threshold + 1

    def __iter__(self):
        return self

    def __next__(self):
        self.current_hash_index -= 1
        if self.current_hash_index < 0:
            raise StopIteration
        return self.connection.getblock(self.blockchain[self.current_hash_index], 2)

    def recreate_blockchain(self):
        block = {'hash': self.connection.getbestblockhash()}
        while True:
            block = self.connection.getblock(block['hash'])
            self.blockchain.append(block['hash'])
            if block.get('previousblockhash', self.start_hash) == self.start_hash:
                break
