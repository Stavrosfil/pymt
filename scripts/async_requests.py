import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup

BASE_URL = "http://m.oasth.gr/#index.php"
HEADERS = {"X-Requested-With": "XMLHttpRequest"}


async def fetch(url, params, session):
    async with session.get(url, params=params) as response:
        return await response.read()


async def run(stop_ids):
    tasks = []
    to_request = []

    for stop_id in stop_ids:
        to_request.append({"md": 4, "sn": 3, "start": stop_id})

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession(headers=HEADERS) as session:
        for params in to_request:
            task = asyncio.ensure_future(fetch(BASE_URL, params, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # You now have all response bodies in the responses list
        # print_responses(responses)
        return responses


def print_responses(results):
    for result in results:
        soup = BeautifulSoup(result.decode('utf-8'), 'html5lib')
        print(soup.prettify())


def get_stops(stop_ids):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(stop_ids))
    done = loop.run_until_complete(future)
    # print_responses(done)
    return done
