import asyncio
from aiohttp import ClientSession
import json
from pymt.default_logger import log_time

BASE_URL = "https://oasth.gr/el/api/getStopArrivals/"


@log_time("Query requests to OASTH")
def get_stops(stops):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(_run(stops))
    done = loop.run_until_complete(future)
    return done


async def _fetch(url, params, session):
    async with session.get(url, params=params) as response:
        return await response.read()


async def _run(stop_ids):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for stop_id in stop_ids:
            task = asyncio.ensure_future(_fetch(BASE_URL + str(stop_id), {"a": "1"}, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        # You now have all response bodies in the responses list
        return [(json.loads(r) if r is not None else None) for r in responses]
