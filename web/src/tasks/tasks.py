import os
import time
import pymongo
import logging
import pandas
from web import celery_app
from web.mongo import Mongo
from .utils import auto_save_result
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# this will go to netutils.py

def get_max_height():
    max_height = \
        Mongo.db(os.environ['MONGODB_NAME']).blocks.find_one(sort=[("height", pymongo.DESCENDING)])['height']

    return max_height

# this will go to netutils.py - end

@celery_app.task
@auto_save_result
def get_block_by_height(height):
    block = Mongo.db(os.environ['MONGODB_NAME']).blocks.find_one({'height': height})
    block['_id'] = ''  # mongo ObjectID is not JSON serializable, and I don't yet have nice solution
    return block

@celery_app.task
@auto_save_result
def get_blocks_range(start_height, end_height):
    #rdb.set_trace()
    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
        (start_height <= max_height) and (end_height <= max_height):

        blocks = Mongo.db(os.environ['MONGODB_NAME']).blocks.find( { 'height': { '$gte': start_height, \
                                                                                 '$lte': end_height } } )

        blocks_all = []

        for block in blocks:
            block['_id'] = ''
            blocks_all.append(block)
        return blocks_all
    else:
        return None


@celery_app.task
@auto_save_result
def get_blocks_number(start_height, num_of_blocks):
    #rdb.set_trace()
    max_height = get_max_height()

    if num_of_blocks > 0:
        end_height = start_height + num_of_blocks - 1

    if (num_of_blocks > 0) and (start_height >= 0) and (end_height >= start_height) and \
        (start_height <= max_height) and (end_height <= max_height):

        blocks = Mongo.db(os.environ['MONGODB_NAME']).blocks.find( { 'height': { '$gte': start_height, \
                                                                                 '$lte': end_height } } )

        blocks_all = []

        for block in blocks:
            block['_id'] = ''
            blocks_all.append(block)
        return blocks_all
    else:
        return None

@celery_app.task
@auto_save_result
def get_edges_range(start_height, end_height):
    # rdb.set_trace()
    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
            (start_height <= max_height) and (end_height <= max_height):

        blocks = Mongo.db(os.environ['MONGODB_NAME']).blocks.find({'height': {'$gte': start_height, \
                                                                              '$lte': end_height}})

        transactions_all = []

        for block in blocks:
            logger.info('asdf')
            block_height = block['height']
            for transaction in block['tx']:
                transaction_txid = transaction['txid']
                transaction_vins = []

                for transaction_vin in transaction['vin']:
                    if 'coinbase' in transaction_vin:
                        transaction_vins.append(transaction_vin['coinbase'][0])
                    else:
                        transaction_vins.append(transaction_vin['addresses'][0])

                transaction_vouts = {}

                for transaction_vout in transaction['vout']:
                    vout_value = transaction_vout['value']

                    vout_address = transaction_vout['scriptPubKey']['addresses'][0]
                    transaction_vouts[vout_address] = vout_value

        # CSV to be returned here

        return transaction_txid
    else:
        return None

@celery_app.task
@auto_save_result
def wait_n_seconds(seconds):
    time.sleep(seconds)
    return {'result': f'waited {seconds}s'}
