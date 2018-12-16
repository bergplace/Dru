

def resolve_input_addresses(block, cache, mongo, logger):
    tx_count = 0
    tx_with_id_and_vout = 0
    tx_cached = 0
    for tx in block['tx']:
        for tx_in in tx['vin']:
            tx_count += 1
            if 'txid' in tx_in and 'vout' in tx_in:
                tx_with_id_and_vout += 1
                tx_hash, out_index = tx_in['txid'], tx_in['vout']
                addresses = cache.get(tx_hash, out_index)
                if addresses:
                    tx_cached += 1
                    tx_in['addresses'] = addresses
                else:
                    tx_in['addresses'] = mongo.get_tx_out_addr(tx_hash, out_index)

