import json

import requests


class Dru:
    # until it's not in docker
    base_url = "http://localhost:8000"

    @staticmethod
    def get(url):
        return Dru.get_result(requests.get(Dru._url(url)))

    @staticmethod
    def post(url, data):
        return Dru.get_result(requests.post(Dru._url(url)))

    @staticmethod
    def _url(url):
        return Dru.base_url + url

    @staticmethod
    def get_result(response):
        while True:
            result_url = response.json()['result_url']
            result = requests.get(result_url).json()
            if result['ready']:
                break
            if result['status'] == 'error':
                raise TaskError
        return result['data']


class TaskError(Exception):
    pass


def fixture(file):
    with open('test/fixtures/' + file, 'r') as f:
        return json.loads(f.read())
