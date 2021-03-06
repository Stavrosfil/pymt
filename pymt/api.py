import asyncio
import concurrent.futures

import requests

import pymt.helpers.metadata
from pymt import default_logger


@pymt.helpers.metadata.timer()
def get_async(urls):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_main(urls))


@pymt.helpers.metadata.timer()
def get_stop_telematics(stop):
    return requests.get(stop.get_telematics_url()).json()


@pymt.helpers.metadata.timer()
def get_line_telematics(line, day=0):
    return requests.get(line.get_telematics_url(day)).json()


async def _main(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                requests.get,
                url
            )
            for url in urls
        ]
        responses = await asyncio.gather(*futures)
        return [rf for r in responses if (rf := r.json()) is not None]
