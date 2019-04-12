import os
import time
import igraph
import pymongo
import logging
from web import celery_app
from web.mongo import Mongo
from .utils import auto_save_result
from django.conf import settings
from celery.utils.log import get_task_logger
from .netutils import *

logger = get_task_logger(__name__)

@celery_app.task
@auto_save_result
def get_block_by_height(height):
    block = Mongo.db(os.environ['MONGODB_NAME']).blocks.find_one({'height': height})
    block['_id'] = ''  # mongo ObjectID is not JSON serializable, and I don't yet have nice solution
    return block

@celery_app.task
@auto_save_result
def get_blocks(start_height, end_height):
    #rdb.set_trace()
    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
        (start_height <= max_height) and (end_height <= max_height):

        blocks = Mongo.db(os.environ['MONGODB_NAME']).blocks.find(
            {
                'height': {
                        '$gte': start_height,
                        '$lte': end_height
                }
            },
            {
                '_id': 0
            }
        )

        return [b for b in blocks]
    else:
        return None

@celery_app.task
@auto_save_result
def get_blocks_reduced(start_height, end_height):

    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
        (start_height <= max_height) and (end_height <= max_height):

        blocks = Mongo.db(os.environ['MONGODB_NAME']).blocks.find(
            {
                'height': {
                        '$gte': start_height,
                        '$lte': end_height
                }
            },
            {
                'height': 1,
                'tx.txid': 1,
                'tx.vin.addresses': 1,
                'tx.vin.coinbase': 1,
                'tx.vout.value': 1,
                'tx.vout.scriptPubKey.addresses': 1,
                '_id': 0
            }
        )

        return [b for b in blocks]
    else:
        return None

@celery_app.task
@auto_save_result
def get_edges(start_height, end_height):
    # rdb.set_trace()
    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
            (start_height <= max_height) and (end_height <= max_height):

        graph = get_graph(start_height, end_height)

        return [
            {
                'source': graph.vs[es.source]['name'],
                'target': graph.vs[es.target]['name'],
                'value': es['value'],
                'block_height': es['height']
            } for es in graph.es
        ]
    else:
        return None

@celery_app.task
@auto_save_result
def get_max_degree(start_height, end_height):

    max_height = get_max_height()

    if (start_height >= 0) and (end_height >= start_height) and \
            (start_height <= max_height) and (end_height <= max_height):

        graph = get_graph(start_height, end_height)

        # logger.info(graph.vcount())
        # logger.info(print(graph))

        vertices_max_degree = [graph.vs.select(_degree=graph.maxdegree())["name"], graph.maxdegree()]

        return vertices_max_degree

    else:
        return None

@celery_app.task
@auto_save_result
def wait_n_seconds(seconds):
    time.sleep(seconds)
    return {'result': f'waited {seconds}s'}
