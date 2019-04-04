from unittest import TestCase
from utils import Dru, fixture


class TestBlockByHeightAPI(TestCase):

    def test_genesis_block(self):
        self.assertEqual(
            Dru.get('/api/block_by_height/0'),
            fixture('zcash_genesis_block.json')
        )

