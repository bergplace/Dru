import os
import time
import igraph
import pymongo
import logging
from web import celery_app
from web.mongo import Mongo
from .utils import auto_save_result, heights_are_valid
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
    if heights_are_valid(start_height, end_height):
        
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
    if heights_are_valid(start_height, end_height):

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
    if heights_are_valid(start_height, end_height):

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
def get_degree_max(start_height, end_height, mode):
    if heights_are_valid(start_height, end_height) and mode in ('all', 'in', 'out'):

        mode = mode.upper()

        if mode == 'ALL':
            graph = get_graph(start_height, end_height, False)
        else:
            graph = get_graph(start_height, end_height, True)

        return dict.fromkeys(graph.vs.select(_degree=graph.maxdegree(mode=mode))["name"], graph.maxdegree(mode=mode))

    else:
        return None

@celery_app.task
@auto_save_result
def get_degree(start_height, end_height, mode):
    if heights_are_valid(start_height, end_height) and mode in ('all', 'in', 'out'):

        mode = mode.upper()

        if mode == 'ALL':
            graph = get_graph(start_height, end_height, False)
        else:
            graph = get_graph(start_height, end_height, True)

        return dict(zip(graph.vs()["name"], graph.degree(mode=mode)))

    else:
        return None

@celery_app.task
@auto_save_result
def get_betweenness_max(start_height, end_height, directed):
    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):

        graph = get_graph(start_height, end_height, directed == "true")

        return dict.fromkeys(graph.vs.select(_betweenness=max(graph.betweenness()))["name"], max(graph.betweenness()))

    else:
        return None

@celery_app.task
@auto_save_result
def get_betweenness(start_height, end_height, directed):
    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed == "true")

        return dict(zip(graph.vs(), graph.betweenness()))

    else:
        return None

@celery_app.task
@auto_save_result
def wait_n_seconds(seconds):
    time.sleep(seconds)
    return {'result': f'waited {seconds}s'}
