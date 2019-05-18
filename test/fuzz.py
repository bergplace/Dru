from random import randint, choice
import aiohttp
import asyncio

URL = 'http://localhost:8000'
REPEAT_NUMBER = 10

APIS = [
    lambda: f'get_blocks/{randint(0, 1000)}/{randint(1000, 2000)}',
    lambda: f'get_blocks_reduced/{randint(0, 1000)}/{randint(1000, 2000)}',
    lambda: f'get_edges/{randint(0, 1000)}/{randint(1000, 2000)}',
    lambda: f'get_degree/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("all", "in", "out"))}',
    lambda: f'get_degree_max/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("all", "in", "out"))}',
    lambda: f'get_betweenness/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("true", "false"))}',
    lambda: f'get_betweenness_max/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("true", "false"))}',
    lambda: f'get_closeness/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("true", "false"))}',
    lambda: f'get_closeness_max/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("true", "false"))}',
    lambda: f'get_transitivity/{randint(0, 1000)}/{randint(1000, 2000)}',
    lambda: f'get_transitivity_global/{randint(0, 1000)}/{randint(1000, 2000)}',
    lambda: f'get_diameter/{randint(0, 1000)}/{randint(1000, 2000)}/{choice(("true", "false"))}',
    lambda: f'get_density/{randint(0, 1000)}/{randint(1000, 2000)}/'
            f'{choice(("true", "false"))}/{choice(("true", "false"))}',
]


async def fetch(session, url):
    async with session.get(url) as response:
        await response.text()


async def call_apis():
    async with aiohttp.ClientSession() as session:
        for api in APIS:
            for _ in range(REPEAT_NUMBER):
                url = f'{URL}/api/{api()}'
                await fetch(session, url)
                print(url)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_apis())
