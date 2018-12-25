import logging

class BTCBlockIterator:

    def __init__(self, connection, logger, start_hash=None, verification_threshold=10):
        logger.info("initializing block iterator")
        self.logger = logger
        self.connection = connection
        self.start_hash = start_hash
        self.verification_threshold = verification_threshold
        self.blockchain = []
        self.recreate_blockchain()
        self.current_hash_index = len(self.blockchain)

    def __iter__(self):
        return self

    def __next__(self):
        self.current_hash_index -= 1
        if self.current_hash_index < self.verification_threshold:
            raise StopIteration
        return self.connection.getblock(self.blockchain[self.current_hash_index], 2)

    def recreate_blockchain(self):
        self.logger.info("start creating blockchain")
        block = {'previousblockhash': self.connection.getbestblockhash()}
        while True:
            if block.get('previousblockhash', self.start_hash) == self.start_hash:
                break # ERROR: IF START BLOCK IS AFTER BEST BLOCK, IT WILL DUPLICATE ENTRIES
            block = self.connection.getblock(block.get('previousblockhash'))
            self.blockchain.append(block['hash'])
            if len(self.blockchain) % 100 == 0:
                self.logger.info(f"reading block (height: {block['height']})")

        self.logger.info(f"blockchain recreated, got {len(self.blockchain)} blocks")
