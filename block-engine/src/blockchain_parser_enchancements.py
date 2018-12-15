"""
TODO:
- add block height
- use Base58Check where appropriate
"""
from bitcoin.core.script import CScriptTruncatedPushDataError  # noqa pylint: disable=import-error
from bitcoin.core.script import CScriptInvalidError  # noqa pylint: disable=import-error
from blockchain_parser.block import Block  # noqa pylint: disable=import-error
from blockchain_parser.blockchain import get_blocks  # noqa pylint: disable=import-error
from output_addresses import NonExistingTransactionOutputException  # noqa

import logger


def get_block(block_info):
    """get block"""
    for i, raw_block in enumerate(get_blocks(block_info.path)):
        if block_info.index == i:
            return Block(raw_block), block_info.height
    return None


class BlockToDict:
    """Convert Block do python dict"""
    def __init__(self, output_addresses):
        self.output_addresses = output_addresses

    def transform(self, block, height):
        """Make conversion"""
        try:
            timestamp = block.header.timestamp
            return {
                'hash': block.hash,
                'version': block.header.version,
                'height': height,
                'prev_hash': block.header.previous_block_hash,
                'merkle_root': block.header.merkle_root,
                'timestamp': timestamp,
                'n_tx': block.n_transactions,
                'size': block.size,
                'bits': block.header.bits,
                'nonce': block.header.nonce,
                'difficulty': block.header.difficulty,
                'transactions': [
                    self.transaction_to_dict(tx, timestamp)
                    for tx in block.transactions
                ]
            }
        except Exception as exception:
            logger.Logger.log("exception for block: {}".format(block.hash))
            raise exception

    def transaction_to_dict(self, blk_tx, timestamp):
        """tx to dict"""
        try:
            outputs = [
                self.output_to_dict(output, blk_tx.hash)
                for output in blk_tx.outputs
            ]
            tx_hash = blk_tx.hash
            self.output_addresses.add_from_outputs(tx_hash, timestamp, outputs)

            return {
                'hash': tx_hash,
                # 'version': tx.version,
                'locktime': blk_tx.locktime,
                'outputs': outputs,
                'inputs': [
                    self.input_to_dict(tx_input, tx_hash)
                    for tx_input in blk_tx.inputs
                ],
            }
        except Exception as exception:
            logger.Logger.log(
                'unknown exception when processing tx: {}'.format(blk_tx.hash)
            )
            raise exception

    def output_to_dict(self, output, tx_hash):
        """output to dict"""
        try:
            return {
                'value': output.value,
                # 'script': output.script.script,
                'addresses': [
                    self.adress_to_dict(addr) for addr in output.addresses
                ],
            }
        except CScriptTruncatedPushDataError:
            # problem with script, cannot get addresses
            logger.Logger.log(
                'CScriptTruncatedPushDataError for tx hash: {}'.format(
                    tx_hash
                )
            )
        except CScriptInvalidError:
            # problem with script, cannot get addresses
            logger.Logger.log('CScriptInvalidError for tx hash: {}'.format(
                tx_hash
            ))
        return {
            'value': output.value,
            # 'script': output.script.script,
            'addresses': [],
        }

    def input_to_dict(self, tx_input, parent_tx_hash):
        """input to dict"""
        tx_hash = tx_input.transaction_hash
        tx_index = tx_input.transaction_index
        try:
            output_timestamp, addresses = self.output_addresses.get(
                tx_hash, tx_index
            )
            return {
                'transaction_hash': tx_hash,
                'transaction_index': tx_index,
                'addresses': addresses,
                'output_timestamp': output_timestamp,
            }
        except NonExistingTransactionOutputException:
            logger.Logger.log(
                'tx with non existing input: {}'.format(parent_tx_hash)
            )
            return {
                'transaction_hash': tx_hash,
                'transaction_index': tx_index,
                'addresses': [],
                'output_timestamp': None,
            }

    def adress_to_dict(self, addr):  # pylint: disable=no-self-use
        """ address to dict """
        return {
            'hash': addr.hash,
            'public_key': addr.public_key,
            'address': addr.address,
            'type': addr.type,
        }
