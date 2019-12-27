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
from sqlalchemy.orm import Session
from typing import List
import logging
from api.v1.catalogue.db_models import DisplayCatalogue
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from api.v1.aggregator.schema import ExternalAPIRequest, LayerResponse

logger = logging.getLogger("aggregator")


def build_wms_query(req: ExternalAPIRequest) -> str:
    """ build_wms_query takes a ExternalAPIRequest object and returns a URL with query params """

    base_url = req.url

    if not base_url.endswith('?'):
        base_url += '?'

    return base_url + urlencode(dict(req.q))


async def parse_result(res: ClientResponse, req: ExternalAPIRequest) -> asyncio.Future:
    """ parse_result takes a response and puts it in a LayerResponse, which
    provides a summary and a collection of features """
    body = await res.read()
    features = []
    data = {}
    fc = {}

    # try to load the response body.
    # if it's not JSON (e.g. xml, an html error page, etc.), it will fail
    # with a TypeError. In this case, we just continue with the defaults
    # set above.
    try:
        data = json.loads(body)
    except TypeError as e:
        logger.error(e)
    except json.JSONDecodeError as e:
        logger.error(e)

    # check if data looks like a geojson FeatureCollection, and if so,
    # make proper Features out of all the objects
    if (res.status == 200 and
        hasattr(data, "get") and
        "type" in data and
        data.get("type") == "FeatureCollection" and
            "features" in data):
        for feat in data["features"]:
            features.append(Feature(**feat))

    # if we didn't recognize a geojson response, check if a formatter was supplied to create geojson.
    elif res.status == 200 and req.formatter and len(data) > 0:
        features = req.formatter(data)['features']

    return LayerResponse(
        status=res.status,
        layer=req.layer,
        geojson=FeatureCollection(features)
    )


async def fetch(req: ExternalAPIRequest, session: ClientSession) -> asyncio.Future:
    """ asyncronously fetch one URL, expecting a geojson response """
    url = build_wms_query(req)

    logger.info(url)

    async with session.get(url) as response:
        return await asyncio.ensure_future(parse_result(response, req))


async def batch_fetch(
        semaphore: asyncio.Semaphore,
        req: ExternalAPIRequest,
        session: ClientSession) -> asyncio.Future:
    """
    batch_fetch uses a semaphore to make batched requests in parallel
    (up a limit equal to the size of the semaphore).
    """

    # The semaphore will block at the limit, and not make any more requests until
    # the first requests return, keeping the number of active requests bounded.
    async with semaphore:
        return await fetch(req, session)


async def fetch_all(requests: List[ExternalAPIRequest]) -> asyncio.Future:
    """
    fetch_all collects features from multiple sources, provided in a list
    of ExternalAPIRequest objects. It returns a "future" iterable. This function can
    be run with asyncio.run(fetch_all(requests)), which will block until
    all the requests are complete.
    """
    tasks = []
    semaphore = asyncio.Semaphore(10)
    headers = {'accept': 'application/json'}

    async with ClientSession(headers=headers) as session:
        for req in requests:
            # use the list of ExternalAPIRequests to form URLs and start adding the requests to the
            # request queue.
            task = asyncio.ensure_future(
                batch_fetch(semaphore, req, session))
            tasks.append(task)

        # return the gathered tasks, which will be a list of JSON responses when all requests return.
        return await asyncio.gather(*tasks)


def fetch_wms_features(requests: List[ExternalAPIRequest]) -> List[LayerResponse]:
    """ fetch_geojson_features collects features from one or more sources and aggregates
    them into a list of WMSResults, each containing the geojson response body and a status code """
    return asyncio.run(fetch_all(requests))


def get_display_catalogue(db: Session, display_data_names: List[str]):
    q = db.query(DisplayCatalogue).options(joinedload(DisplayCatalogue.wms_catalogue),
                                           joinedload(
                                               DisplayCatalogue.api_catalogue),
                                           joinedload(DisplayCatalogue.vector_catalogue))\
        .filter(DisplayCatalogue.display_data_name.in_(display_data_names))\
        .all()
    # [logger.info(vars(x)) for x in q]
    return q


def get_layer_feature(db: Session, layer_class, feature_id):

    q = db.query(layer_class).filter(
        layer_class.primary_key() == feature_id).one_or_none()
    geom = layer_class.get_geom_column(db)
    if q is None:
        raise HTTPException(
            status_code=404, detail="Feature information not found.")

    return layer_class.get_as_feature(q, geom)

