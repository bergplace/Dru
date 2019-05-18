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
def get_blocks(start_height, end_height):
    """Returns the list of blocks for a given range of blocks' heights.

    The returned JSON can be used for further processing if none of the endpoints
    is suitable for performing the requested analysis.
    Note that this endpoint returns whole blocks, no attributes are stripped.

    """
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
    """Returns the list of blocks for a given range of blocks' heights, yet with limited fields.

    The returned fields are the following:
    - height
    - time
    - transaction id
    - input addresses (or coinbase)
    - output addresses
    - value

    As such, this is a limited version of get_blocks endpoint.
    The returned JSON can be used for further processing if none of the endpoints
    is suitable for performing the requested analysis.

    """

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
                'time': 1,
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
    """Returns the list of edges blocks for a given range of blocks' heights.
    These edges can be easily imported into graph-processing libraries.

    Fields returned:
     - source address
     - destination address
     - value of the transactions
     - block height
     - block time

    """

    if heights_are_valid(start_height, end_height):

        graph = get_graph(start_height, end_height, 'false')

        return [
            {
                'source': graph.vs[es.source]['name'],
                'target': graph.vs[es.target]['name'],
                'value': es['value'],
                'block_height': es['height'],
                'block_time': es['time']
            } for es in graph.es
        ]
    else:
        return None


@celery_app.task
@auto_save_result
def get_degree(start_height, end_height, mode):
    """Returns the list of addresses and the value of degree corresponding to them.

    The graph is created from the blocks in the range [start_height, end_height].
    The graph will be built as directed, but using mode all variants of the measure
    can be computed:
     - all - total degree of the node
     - in - in-degree of the node
     - out - out-degree

    """

    if heights_are_valid(start_height, end_height) and mode in ('all', 'in', 'out'):

        mode = mode.upper()

        graph = get_graph(start_height, end_height, mode != 'ALL')

        return dict(zip(graph.vs()["name"], graph.degree(mode=mode)))

    else:
        return None


@celery_app.task
@auto_save_result
def get_degree_by_block(start_height, end_height, address, mode):
    """Returns the list of addresses and the value of degree corresponding to them.

    The graph is created from the blocks in the range [start_height, end_height].
    This variant computes the degree in each block separately.
    The graph will be built as directed, but using mode all variants of the measure
    can be computed:
     - all - total degree of the node
     - in - in-degree of the node
     - out - out-degree

    """

    if heights_are_valid(start_height, end_height) and mode in ('all', 'in', 'out'):

        mode = mode.upper()
        degrees = []

        for height in range(start_height, end_height + 1):

            graph = get_graph(height, height, mode != 'ALL')

            if address in graph.vs()["name"]:
                degree = {'height': height,
                         'degree': graph.degree(vertices=graph.vs.find(address).index, mode=mode)}
                degrees.append(degree)
            else:
                degree = {'height': height,
                         'degree': None}
                degrees.append(degree)

        return {'address': address,
                'mode': mode,
                'degrees': degrees}

    else:
        return None


@celery_app.task
@auto_save_result
def get_degree_max(start_height, end_height, mode):
    """Returns the list of addresses and the value of degree corresponding to them.

    The graph is created from the blocks in the range [start_height, end_height].
    The graph will be built as directed, but using mode all variants of the measure
    can be computed:
     - all - total degree of the node
     - in - in-degree of the node
     - out - out-degree

    """

    if heights_are_valid(start_height, end_height) and mode in ('all', 'in', 'out'):

        mode = mode.upper()

        graph = get_graph(start_height, end_height, mode != 'ALL')

        return dict.fromkeys(graph.vs.select(_degree=graph.maxdegree(mode=mode))["name"], graph.maxdegree(mode=mode))

    else:
        return None


@celery_app.task
@auto_save_result
def get_betweenness(start_height, end_height, directed):
    """Returns the list of addresses and the value of betweenness corresponding to them.

    The graph is created from the blocks in the range [start_height, end_height].
    The graph can be built either as directed or undirected.
    Note: as all shortest paths have to be computed, this operation is time-consuming. Use with care.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed == "true")
        return dict(zip(graph.vs()["name"], graph.betweenness()))
    else:
        return None


@celery_app.task
@auto_save_result
def get_betweenness_max(start_height, end_height, directed):
    """Returns the address and the value of betwenneess in the graph created

    The graph is created from the from the blocks in the range [start_height, end_height].
    The graph can be built either as directed or undirected.

    Note: as all shortest paths have to be computed, this operation is time-consuming. Use with care.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):

        graph = get_graph(start_height, end_height, directed == "true")

        return dict.fromkeys(graph.vs.select(_betweenness=max(graph.betweenness()))["name"], max(graph.betweenness()))

    else:
        return None


@celery_app.task
@auto_save_result
def get_closeness(start_height, end_height, directed):
    """Returns the list of addresses and the value of closeness corresponding to them.

    The graph is created from the from the blocks in the range [start_height, end_height].
    The graph can be built either as directed or undirected.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed == "true")

        return dict(zip(graph.vs()["name"], graph.closeness()))

    else:
        return None


@celery_app.task
@auto_save_result
def get_closeness_max(start_height, end_height, directed):
    """Returns the address and the value of the closeness in the graph.

    The graph is created from the from the blocks in the range [start_height, end_height].
    The graph can be built either as directed or undirected.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed == "true")

        return dict(zip(graph.vs()["name"], graph.closeness()))

    else:
        return None


@celery_app.task
@auto_save_result
def get_transitivity(start_height, end_height):
    """Returns the nodes' clustering coefficient in the graph.

    The graph is created from the blocks in the range [start_height, end_height]
    For global clustering coefficient value, use for get_transitivity_global.

    """

    if heights_are_valid(start_height, end_height):
        graph = get_graph(start_height, end_height, directed="false")
        return dict(zip(graph.vs()["name"], graph.transitivity_local_undirected(None, "zero")))
    else:
        return None


@celery_app.task
@auto_save_result
def get_transitivity_global(start_height, end_height):
    """Returns the clustering coefficient of the graph created from the blocks in the range [start_height, end_height].

    This value is global for the graph. For node-level clustering coefficient, use get_transitivity.

    """

    if heights_are_valid(start_height, end_height):
        graph = get_graph(start_height, end_height, directed="false")
        return graph.transitivity_undirected()
    else:
        return None


@celery_app.task
@auto_save_result
def get_diameter(start_height, end_height, directed):
    """Returns the diameter of the graph created from the blocks in the range [start_height, end_height].

    The graph can be considered as directed or undirected.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed)
        return graph.diameter()
    else:
        return None


@celery_app.task
@auto_save_result
def get_density(start_height, end_height, directed, loops):
    """Returns the density of the graph created from the blocks in the range [start_height, end_height].

    The graph can be considered as directed or undirected.
    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false') and loops in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed)
        return graph.density()
    else:
        return None


@celery_app.task
@auto_save_result
def are_connected(start_height, end_height, address1, address2, directed):
    """Returns true/false information whether two addresses are connected within a given range of blocks.

    If any of these addresses does not exist in the graph, None will be returned.

    """

    if heights_are_valid(start_height, end_height) and directed in ('true', 'false'):
        graph = get_graph(start_height, end_height, directed)
        if address1 in graph.vs()["name"] and address2 in graph.vs()["name"]:
            return [{'start_height': start_height,
                     'end_height': end_height,
                     'address1': address1,
                     'address2': address2,
                     'directed': directed,
                     'are_connected': graph.are_connected(address1, address2)}]
        else:
            return None
    else:
        return None


@celery_app.task
@auto_save_result
def get_transactions_value(start_height, end_height, address1, address2):
    """Returns the count and total value of transactions between two addresses in the graph.

    The graph is created from the blocks in the range [start_height, end_height].

    If any of these addresses does not exist in the graph, None will be returned.

    """

    if heights_are_valid(start_height, end_height):
        graph = get_graph(start_height, end_height, directed="true")
        if address1 in graph.vs()["name"] and address2 in graph.vs()["name"]:
            edges = graph.es.select(_between=([graph.vs.find(address1).index],[graph.vs.find(address2).index]))
            return [{'start_height': start_height,
                     'end_height': end_height,
                     'address1': address1,
                     'address2': address2,
                     'transactions_count': len(edges),
                     'transactions_value': sum(edges["value"])}]
        else:
            return None
    else:
        return None
