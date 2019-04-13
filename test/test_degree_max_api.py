from unittest import TestCase
from utils import Dru, fixture


class TestDegreeMaxAPI(TestCase):

    def test_degree_max_all(self):
        block = Dru.get('/api/get_degree_max/0/99/all')
        test_block = fixture('zcash_degree_max_all.json')

        self.assertEqual(block, test_block)

    def test_degree_max_in(self):
        block = Dru.get('/api/get_degree_max/0/99/in')
        test_block = fixture('zcash_degree_max_in.json')

        self.assertEqual(block, test_block)

    def test_degree_max_out(self):
        block = Dru.get('/api/get_degree_max/0/99/out')
        test_block = fixture('zcash_degree_max_out.json')

        self.assertEqual(block, test_block)
