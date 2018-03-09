import time
import multiprocessing
import traceback
from copy import copy
import mongo
from blk_files_reader import BLKFilesReader
from blockchain_parser_enchancements import block_to_dict, get_block
from multiprocessing import Pool

from logger import Logger


class BlockchainDBMaintainer(object):
    """
    responsible for taking raw blocks from
    bitcoin data directory, and putting them
    in json format to MongoDB database
    """

    def __init__(self):
        self.logger = Logger()
        self.mongo = mongo.Mongo(self.logger)
        self.blk_files_reader = BLKFilesReader(self.logger, self.mongo)
        self.n_processes = multiprocessing.cpu_count()
        self.blockchain = None
        self.processes_count = 0
        self.process_count_limit = self.n_processes * 4
        self.processed_blocks = dict()

    def run(self):
        """execution starts here"""
        while True:
            self.blockchain = self.blk_files_reader.get_ordered_blocks()
            self.save_blocks_parallel_async()
            self.logger.log('current collection count: {}'.format(self.mongo.blocks_collection.count()))
            self.mongo.create_indexes()
            self.logger.log('sleeps for 10 minutes')
            time.sleep(600)

    def save_blocks_parallel_async(self):
        """
        starts fixed number of asynchronous parallel tasks processing blocks,
        when task has finished, callback function is called
        """
        n_blocks_to_process = len(self.blockchain)
        self.logger.log('processing of {} blocks starts'.format(n_blocks_to_process))
        pool = Pool(processes=self.n_processes)
        for i, block_info in enumerate(copy(self.blockchain)):
            self.logger.log_processing(i, n_blocks_to_process)
            self.processes_count += 1
            pool.apply_async(
                self.process_single_block,
                (block_info, ),  # for some reason it has to be in tuple
                callback=self.process_result_callback
            )
            while (self.processes_count > self.process_count_limit or
                   len(self.processed_blocks) > self.process_count_limit):
                time.sleep(0.1)
        pool.close()
        pool.join()

    @staticmethod
    def process_single_block(block_info):
        """function to run in every worker"""
        result = None
        try:
            result = block_to_dict(*get_block(block_info))
        except:
            return block_info[0], result, traceback.format_exc()

        return block_info[0], result, None

    def process_result_callback(self, result):
        """
        callback function for tasks started by 'save_blocks_parallel_async'
        """
        self.processes_count -= 1
        block_hash, block, err = result

        if err:
            self.logger.log('ERROR IN BLOCK')
            self.logger.log(block_hash)
            self.logger.log(err)

        self.processed_blocks[block_hash] = block

        while True:
            block_to_save = self.processed_blocks.get(self.next_block_hash, None)
            if block_to_save is None:
                break
            self.mongo.save_block(self.next_block_hash, block_to_save)
            del self.processed_blocks[self.next_block_hash]
            self.blockchain.popleft()

    @property
    def next_block_hash(self):
        """returns hash of next block to save to db"""
        return self.blockchain[0][0]


if __name__ == '__main__':
    BlockchainDBMaintainer().run()
