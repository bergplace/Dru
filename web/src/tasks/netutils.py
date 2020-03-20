import os
import pymongo
import igraph
import logging

from web.mongo import Mongo


def get_max_height():
    max_height = \
        Mongo.db(os.environ['MONGODB_NAME']).blocks.find_one(sort=[("height", pymongo.DESCENDING)])['height']

    return max_height


def get_graph(start_height, end_height, directed):
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
        },
        no_cursor_timeout=True
    )

    graph = igraph.Graph(directed=directed)
    blocks = [block for block in blocks]
    for block in blocks:
        block_height = block['height']
        block_time = block['time']

        for transaction in block['tx']:
            transaction_txid = transaction['txid']
            transaction_vins = []

            for transaction_vin in transaction['vin']:
                if 'coinbase' in transaction_vin:
                    vin_address = 'coinbase'
                else:
                    vin_address = transaction_vin['addresses'][0]

                transaction_vins.append(vin_address)

                try:
                    vertex = graph.vs.find(vin_address)
                except ValueError:
                    graph.add_vertex(vin_address)

            transaction_vouts = {}

            for transaction_vout in transaction['vout']:
                vout_value = transaction_vout['value']
                vout_addresses = transaction_vout['scriptPubKey'].get('addresses')
                if vout_addresses:
                    vout_address = vout_addresses[0]
                    transaction_vouts[vout_address] = vout_value

                    try:
                        vertex = graph.vs.find(vout_address)
                    except ValueError:
                        graph.add_vertex(vout_address)

            for transaction_vin in transaction_vins:

                for transaction_vout, transaction_value in transaction_vouts.items():
                    graph.add_edge(transaction_vin, transaction_vout, value=transaction_value, txid=transaction_txid,
                                   height=block_height, time=block_time)

    if directed is False:
        graph.to_undirected()

    return graph
