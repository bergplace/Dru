from random import randint, choice
import aiohttp
import asyncio

URL = 'http://127.0.0.1:8000'
REPEAT_NUMBER = 10
SPREAD = 100
CURRENT_HEIGHT = 6000

APIS = [
    lambda offset: f'get_blocks/{offset}/{offset + randint(0, SPREAD)}',
    lambda offset: f'get_blocks_reduced/{offset}/{offset + randint(0, SPREAD)}',
    lambda offset: f'get_edges/{offset}/{offset + randint(0, SPREAD)}',
    lambda offset: f'get_degree/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("all", "in", "out"))}',
    lambda offset: f'get_degree_max/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("all", "in", "out"))}',
    lambda offset: f'get_betweenness/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}',
    lambda offset: f'get_betweenness_max/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}',
    lambda offset: f'get_closeness/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}',
    lambda offset: f'get_closeness_max/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}',
    lambda offset: f'get_transitivity/{offset}/{offset + randint(0, SPREAD)}',
    lambda offset: f'get_transitivity_global/{offset}/{offset + randint(0, SPREAD)}',
    lambda offset: f'get_diameter/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}',
    lambda offset: f'get_density/{offset}/{offset + randint(0, SPREAD)}/'
                   f'{choice(("true", "false"))}/{choice(("true", "false"))}',
]


async def fetch(session, url):
    async with session.get(url) as response:
        await response.text()


async def call_apis():
    async with aiohttp.ClientSession() as session:
        for api in APIS:
            for _ in range(REPEAT_NUMBER):
                url = f'{URL}/api/{api(randint(0, CURRENT_HEIGHT - SPREAD))}'
                await fetch(session, url)
                print(url)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_apis())
