from unittest import TestCase
from utils import Dru, fixture


class TestBlockByHeightAPI(TestCase):

    def test_genesis_block(self):
        block = Dru.get('/api/block_by_height/0')
        test_block = fixture('zcash_genesis_block.json')

        for b in block, test_block:
            # this value changes!
            b['confirmations'] = None
            b['valuePools'] = None

        self.assertEqual(block, test_block)
