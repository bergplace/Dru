"""
Utils for communicating with rpc api's of cryptocurrencies nodes
"""
import json
import os

import requests
from requests.auth import HTTPBasicAuth


class RPC:

    def __init__(self):
        self.url = 'http://localhost:' + os.environ['CRYPTO_PORT']
        self.user = os.environ['CRYPTO_USER']
        self.password = os.environ['CRYPTO_PASS']
        self.headers = {
            'content-type': 'application/json',
        }
        self.id = 0

    def __getattr__(self, item):
        def _call_rpc(*args):
            payload = {
                "method": item,
                "params": args,
                "jsonrpc": "2.0",
                "id": self.id,
            }
            self.id += 1
            response = requests.post(
                self.url,
                data=json.dumps(payload),
                headers=self.headers,
                auth=HTTPBasicAuth('user', 'pass')
            )
            result = json.loads(response.text)
            if result.get('error'):
                raise BitcoinRPCError(f"error: {result['error']} for payload: {payload}")
            return result['result']

        return _call_rpc


class BitcoinRPCError(Exception):
    pass


