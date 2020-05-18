import aiohttp
import asyncio

# Example 3: asynchronous requests with larger thread pool
import concurrent.futures
import requests


def get_stop_telematics(stop):
    response = requests.get("http://oasth.gr/el/api/getStopArrivals/{}/?a=1".format(stop._id)).json()
    return response


def get_line_telematics(line, day=0):
    response = requests.get("http://oasth.gr/el/api/getBusLocation/{}/?a=1".format(line.days[day])).json()
    return response


# ---------------------------------------------------------------------------------------


# async def get(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return response
#
#
# loop = asyncio.get_event_loop()
#
# coroutines = [get("http://oasth.gr/el/api/getBusLocation/{}/?a=1".format(l)) for l in
#               ["2328", "2329", "2279", "2307", "193", "192"]]
#
# results = [r.text for r in loop.run_until_complete(asyncio.gather(*coroutines))]
#
# print("Results: %s" % results)


# ---------------------------------------------------------------------------------------


async def main(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                requests.get,
                'http://oasth.gr/el/api/getBusLocation/{}/?a=1'.format(l)
            )
            for l in urls
        ]
        responses = await asyncio.gather(*futures)
        return [r.json() for r in responses]


def get_async(urls):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main(urls))
