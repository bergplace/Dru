

def resolve_input_addresses(block, cache, mongo_connection):
    for tx in block['tx']:
        for tx_in in tx['vin']:
            if 'txid' in tx_in and 'vout' in tx_in:
                addresses = cache.get(tx_in['txid'], tx_in['vout'])
                if addresses:
                    tx_in['addresses'] = addresses
