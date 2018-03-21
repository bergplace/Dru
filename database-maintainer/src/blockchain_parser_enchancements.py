"""
TODO:
- add block height
- use Base58Check where appropriate
"""
from bitcoin.core.script import CScriptTruncatedPushDataError, CScriptInvalidError
from blockchain_parser.block import Block
from blockchain_parser.blockchain import get_blocks

import logger


def get_block(block_info):
    for i, raw_block in enumerate(get_blocks(block_info.path)):
        if block_info.index == i:
            return Block(raw_block), block_info.height


def block_to_dict(block, height):
    return {
        'hash': block.hash,
        'version': block.header.version,
        'height': height,
        'prev_hash': block.header.previous_block_hash,
        'merkle_root': block.header.merkle_root,
        'timestamp': block.header.timestamp,
        'n_tx': block.n_transactions,
        'size': block.size,
        'bits': block.header.bits,
        'nonce': block.header.nonce,
        'difficulty': block.header.difficulty,
        'transactions': [transaction_to_dict(tx) for tx in block.transactions]
    }


def transaction_to_dict(tx):
    return {
        'hash': tx.hash,
        # 'version': tx.version,
        'locktime': tx.locktime,
        'outputs': [output_to_dict(output, tx.hash) for output in tx.outputs],
        'inputs': [input_to_dict(tx_input) for tx_input in tx.inputs],
    }


def output_to_dict(output, tx_hash):
    try:
        return {
            'value': output.value,
            # 'script': output.script.script,
            'addresses': [adress_to_dict(addr) for addr in output.addresses],
        }
    except CScriptTruncatedPushDataError:
        """
        hard to say at this point what is the reason this exception is thrown
        but it happened once at block 
        000000000000000000c81eeaa0e0274e0376a8ec21f801c4b78b3a6c71ef37e6
        and is supposedly linked to not valid script value
        """
        logger.Logger.log('CScriptTruncatedPushDataError for tx hash: {}'.format(
            tx_hash
        ))
    except CScriptInvalidError:
        """I guess it means that script is invalid..."""
        logger.Logger.log('CScriptInvalidError for tx hash: {}'.format(
            tx_hash
        ))
    return {
        'value': output.value,
        # 'script': output.script.script,
        'addresses': [],
    }


def input_to_dict(tx_input):
    return {
        # 'sequence_number': tx_input.sequence_number,
        # 'script': tx_input.script.script,
        # 'value': tx_input.script.value,
        'transaction_hash': tx_input.transaction_hash,
        'transaction_index': tx_input.transaction_index,
    }


def adress_to_dict(addr):
    return {
        'hash': addr.hash,
        'public_key': addr.public_key,
        'address': addr.address,
        'type': addr.type,
    }
