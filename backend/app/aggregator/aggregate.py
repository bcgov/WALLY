"""
Functions for aggregating data from web requests and database records
"""
import logging
import asyncio
import json
from typing import List
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from aiohttp import ClientSession
from app.aggregator.models import WMSRequest


logger = logging.getLogger("aggregator")


def form_wms_query(req: WMSRequest) -> str:
    """ form_wms_query takes a WMSRequest object and returns a URL with query params """
    return req.url + urlencode(dict(req.q))


async def fetch(url, session: ClientSession) -> asyncio.Future:
    """ asyncronously fetch one URL, expecting a geojson response """
    async with session.get(url) as response:
        return await response.read()


async def fetch_queue(semaphore, url, session) -> asyncio.Future:
    """
    fetch_queue uses a semaphore to make batched requests in parallel.
    """

    # The semaphore will block at the limit, and not make any more requests until
    # the first requests return, keeping the number of active requests bounded.
    async with semaphore:
        return await fetch(url, session)


async def fetch_all(requests: List[WMSRequest]) -> asyncio.Future:
    """
    fetch_all collects features from multiple sources
    """
    tasks = []
    semaphore = asyncio.Semaphore(10)
    headers = {'accept': 'application/json'}
    async with ClientSession(headers=headers) as session:
        for req in requests:
            # use the list of WMSRequests to form URLs and start adding the requests to the
            # request queue.
            url = form_wms_query(req)
            task = asyncio.ensure_future(
                fetch_queue(semaphore, url, session))
            tasks.append(task)

        # return the gathered tasks, which will be a list of JSON responses when all requests return.
        return await asyncio.gather(*tasks)


def fetch_wms_features(requests: List[WMSRequest]) -> FeatureCollection:
    """ fetch_geojson_features collects features from one or more sources and aggregates
    them into a single geojson FeatureCollection """

    results = asyncio.run(fetch_all(requests))

    features = []

    for i in results:
        # each result set can have multiple features, with the total of n * m (layers * features)
        # being the number of total points that a user has selected across all active layers.
        fc = json.loads(i)

        # check if the response looks like a FeatureCollection, if so, make Feature objects
        # out of the items in list
        if fc["type"] and fc["type"] == "FeatureCollection" and fc["features"]:
            for j in json.loads(i)["features"]:
                features.append(Feature(**j))

    return features
