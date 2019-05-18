from unittest import TestCase
from utils import Dru, fixture


class TestBlockByHeightAPI(TestCase):

    def test_genesis_block(self):
        blocks = Dru.get('/api/get_blocks/0/0')
        test_block = fixture('zcash_genesis_block.json')

        for b in blocks + [test_block]:
            # this value changes!
            b['_id'] = None
            b['confirmations'] = None
            b['valuePools'] = None

        self.assertEqual(blocks[0], test_block)
