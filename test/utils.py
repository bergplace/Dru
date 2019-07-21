import json
from time import sleep

import requests


class Dru:
    # until it's not in docker
    base_url = "http://localhost:8000"
    blocks_ready = False

    @staticmethod
    def get(url):
        if not Dru.blocks_ready:
            Dru._wait_for_blocks()
        return Dru.get_result(requests.get(Dru._url(url)))

    @staticmethod
    def post(url, data):
        return Dru.get_result(requests.post(Dru._url(url)))

    @staticmethod
    def _url(url):
        return Dru.base_url + url

    @staticmethod
    def _wait_for_blocks():
        height = 0
        while height < 1000:
            height = requests.get(Dru._url('/api/current_block_height')).json()['height']
            print(f"currently loaded blocks: {height}")
            sleep(1)
        Dru.blocks_ready = True

    @staticmethod
    def get_result(response):
        while True:
            result_url = response.json()['result_url']
            result = requests.get(result_url).json()
            if result['ready']:
                break
            if result['status'] == 'error':
                raise TaskError
            sleep(1)
        return result['data']


class TaskError(Exception):
    pass


def fixture(file):
    with open('test/fixtures/' + file, 'r') as f:
        return json.loads(f.read())
