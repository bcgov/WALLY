import logging
import asyncio
import json
from typing import List
from urllib.parse import urlencode
from shapely.geometry import LineString, Point
from geojson import FeatureCollection, Feature
from aiohttp import ClientSession, ClientResponse

logger = logging.getLogger("elevation_surface")


async def parse_result(res: ClientResponse) -> asyncio.Future:
    """  """
    body = await res.read()
    line = {}

    try:
        line = json.loads(body)
    except TypeError as e:
        logger.error(e)
    except json.JSONDecodeError as e:
        logger.error(e)

    # check if fc looks like a geojson FeatureCollection, and if so,
    # make proper Features out of all the objects
    # if res.status == 200 and line.get("altitude") != None

    return LineString(
        [
            (
                point.get("geometry").get("coordinates")[0],
                point.get("geometry").get("coordinates")[1],
                point.get("altitude")
            ) for point in line
        ]
    )

async def fetch(line: str, session: ClientSession) -> asyncio.Future:
    """ asyncronously fetch one URL, expecting a geojson response """
    steps = 10
    if not line:
        return []
    url = f"http://geogratis.gc.ca/services/elevation/cdem/profile.json?path={line}&steps={steps}"
    async with session.get(url) as response:
        return await asyncio.ensure_future(parse_result(response))


async def batch_fetch(
        semaphore: asyncio.Semaphore,
        req: str,
        session: ClientSession) -> asyncio.Future:
    """
    batch_fetch uses a semaphore to make batched requests in parallel
    (up a limit equal to the size of the semaphore).
    """

    async with semaphore:
        return await fetch(req, session)


async def fetch_all(requests: List[str]) -> asyncio.Future:
    """
    """
    tasks = []
    semaphore = asyncio.Semaphore(10)
    headers = {'accept': 'application/json'}
    
    async with ClientSession(headers=headers) as session:
        for req in requests:
            task = asyncio.ensure_future(
                batch_fetch(semaphore, req, session))
            tasks.append(task)

        # return the gathered tasks, which will be a list of JSON responses when all requests return.
        return await asyncio.gather(*tasks)


def fetch_surface_lines(requests: List[str]) -> List[Feature]:
    """
    """
    return asyncio.run(fetch_all(requests))