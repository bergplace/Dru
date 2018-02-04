from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
from collections import deque

"""
General description:

on start:
    gather block info
loop:
    get hash of last block in db
    check in witch file next valid block is
    if there is no such information 
        update block info
        and check in witch file next valid block is
    load it to db
    
problems:
    not verified blocks, get only those confirmed
    by 5 other
    
    
structure of block info:

    {previous_block_hash: (this_block_hash, filename)}
"""


class BlockchainDBMaintainer(object):

    def __init__(self, config):
        self.btc_data_dir_path = config['btc_data_dir_path']
        self.block_hash_chain = {}
        self.checked_blk_files = set()
        self.genesis_hash = '0000000000000000000000000000000000000000000000000000000000000000'
        self.last_verified = self.genesis_hash
        self.verification_threshold = 6

    def refresh_block_data(self):
        print('blocks data gathering starts')
        files_to_check = sorted(set(get_files(self.btc_data_dir_path))
                                - self.checked_blk_files)
        self.checked_blk_files = set(files_to_check) | self.checked_blk_files
        for i, blk_file in enumerate(files_to_check):
            for raw_block in get_blocks(blk_file):
                b = Block(raw_block)
                self.block_hash_chain[b.header.previous_block_hash] = [
                    b.hash, blk_file, False
                ]  # maybe add verified flag as well
            print('{}% ready'.format(100 * i / len(files_to_check)))

    def verify_blocks(self):
        print('blocks verification starts')
        block_stack = deque()
        # initialize block stack
        first_block = self.block_hash_chain.get(self.last_verified, None)
        if first_block is None:
            raise Exception('Last verified block not found')
        block_stack.append(first_block)
        for _ in range(self.verification_threshold):
            block = self.block_hash_chain.get(block_stack[-1][0], None)
            if block is None:
                return
            block_stack.append(block)
        # verify
        next_block = self.block_hash_chain.get(block_stack[-1][0], None)
        bc_length = len(self.block_hash_chain)
        counter = 0
        while next_block:
            counter += 1
            if counter % 100 == 0:
                print(counter/bc_length)
            block_stack.append(next_block)
            self.last_verified = block_stack[0]
            self.last_verified[2] = True
            block_stack.popleft()
            next_block = self.block_hash_chain.get(block_stack[-1][0], None)

    def run(self):
        self.refresh_block_data()
        self.verify_blocks()


if __name__ == '__main__':
    config = {
        'btc_data_dir_path': '/opt/platform/bitcoin-data/blocks',
        'db_maintainer_block_info_file_path': '/home/mp/block_info',
    }  # there will be config loader later on
    BlockchainDBMaintainer(config).run()
