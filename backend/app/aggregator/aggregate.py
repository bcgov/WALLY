"""
Functions for aggregating data from web requests and database records
"""
import logging
import asyncio
import json
from typing import List
from urllib.parse import urlencode
from geojson import FeatureCollection, Feature
from aiohttp import ClientSession, ClientResponse
from app.aggregator.models import WMSRequest, WMSResponse


logger = logging.getLogger("aggregator")


def form_wms_query(req: WMSRequest) -> str:
    """ form_wms_query takes a WMSRequest object and returns a URL with query params """
    return req.url + urlencode(dict(req.q))


async def parse_result(res: ClientResponse, layer: str) -> asyncio.Future:
    """ parse_result takes a response and puts it in a WMSResponse, which
    provides a summary and a collection of features """
    body = await res.read()
    features = []
    fc = {}

    # try to load the response body.
    # if it's not JSON (e.g. xml, an html error page, etc.), it will fail
    # with a TypeError. In this case, we just continue with the defaults
    # set above.
    try:
        fc = json.loads(body)
    except TypeError as e:
        logger.error(e)
    except json.JSONDecodeError as e:
        logger.error(e)

    # check if fc looks like a geojson FeatureCollection, and if so,
    # make proper Features out of all the objects
    if res.status == 200 and fc.get("type") and fc.get("type") == "FeatureCollection" and fc.get("features"):
        for feat in fc["features"]:
            features.append(Feature(**feat))

    return WMSResponse(
        status=res.status,
        layer=layer,
        geojson=FeatureCollection(features)
    )


async def fetch(req: WMSRequest, session: ClientSession) -> asyncio.Future:
    """ asyncronously fetch one URL, expecting a geojson response """
    url = form_wms_query(req)
    async with session.get(url) as response:
        return await asyncio.ensure_future(parse_result(response, req.layer))


async def batch_fetch(
        semaphore: asyncio.Semaphore,
        req: WMSRequest,
        session: ClientSession) -> asyncio.Future:
    """
    batch_fetch uses a semaphore to make batched requests in parallel
    (up a limit equal to the size of the semaphore).
    """

    # The semaphore will block at the limit, and not make any more requests until
    # the first requests return, keeping the number of active requests bounded.
    async with semaphore:
        return await fetch(req, session)


async def fetch_all(requests: List[WMSRequest]) -> asyncio.Future:
    """
    fetch_all collects features from multiple sources, provided in a list
    of WMSRequest objects. It returns a "future" iterable. This function can
    be run with asyncio.run(fetch_all(requests)), which will block until
    all the requests are complete.
    """
    tasks = []
    semaphore = asyncio.Semaphore(10)
    headers = {'accept': 'application/json'}
    async with ClientSession(headers=headers) as session:
        for req in requests:
            # use the list of WMSRequests to form URLs and start adding the requests to the
            # request queue.
            task = asyncio.ensure_future(
                batch_fetch(semaphore, req, session))
            tasks.append(task)

        # return the gathered tasks, which will be a list of JSON responses when all requests return.
        return await asyncio.gather(*tasks)


def fetch_wms_features(requests: List[WMSRequest]) -> List[WMSResponse]:
    """ fetch_geojson_features collects features from one or more sources and aggregates
    them into a list of WMSResults, each containing the geojson response body and a status code """
    return asyncio.run(fetch_all(requests))
