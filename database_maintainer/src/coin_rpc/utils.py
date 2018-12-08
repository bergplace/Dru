"""
Utils for communicating with rpc api's of cryptocurrencies nodes
"""
import json
import requests
from requests.auth import HTTPBasicAuth


class RPC:

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
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


