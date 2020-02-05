"""
Aggregate data from different WMS and/or API sources.
"""
from logging import getLogger
import json
import geojson
from geojson import FeatureCollection, Feature
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from shapely.geometry import shape, MultiPolygon, Polygon, Point
from shapely.ops import transform


from api.db.utils import get_db
from api.v1.hydat.db_models import Station as StreamStation
from api.layers.freshwater_atlas_watersheds import FreshwaterAtlasWatersheds

from api.v1.aggregator.controller import (
    databc_feature_search,

    EXTERNAL_API_REQUESTS,
    API_DATASOURCES,
    DATABC_GEOMETRY_FIELD,
    DATABC_LAYER_IDS)
from api.v1.aggregator.schema import WMSGetMapQuery, WMSGetFeatureQuery, ExternalAPIRequest, LayerResponse
from api.v1.aggregator.helpers import transform_4326_3005, transform_3005_4326
from api.v1.aggregator.excel import xlsxExport
from api.v1.watersheds.controller import (
    calculate_glacial_area,
    precipitation,
    surface_water_rights_licences,
    get_watershed,
    surficial_geology,
)
from api.v1.watersheds.schema import (
    WatershedDetails,
    LicenceDetails,
    SurficialGeologyDetails,
    SurficialGeologyTypeSummary
)
from api.v1.isolines.controller import calculate_runnoff_in_area


logger = getLogger("aggregator")

router = APIRouter()


@router.get('/')
def get_watersheds(
    db: Session = Depends(get_db),
    point: str = Query(
        "", title="Search point",
        description="Point to search within")
):
    """ returns a list of watersheds at this point, if any.
    Watersheds are sourced from the following datasets:
    https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-assessment-watersheds
    https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries
    https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-watersheds

    """
    assessment_watershed_layer_id = 'WHSE_BASEMAPPING.FWA_ASSESSMENT_WATERSHEDS_POLY'
    fwa_watersheds_layer_id = 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY'
    hydrometric_watershed_layer_id = 'WHSE_WATER_MANAGEMENT.HYDZ_HYD_WATERSHED_BND_POLY'

    search_layers = ','.join([
        assessment_watershed_layer_id,
        fwa_watersheds_layer_id,
        hydrometric_watershed_layer_id
    ])

    if not point:
        raise HTTPException(
            status_code=400, detail="No search point. Supply a `point` (geojson geometry)")

    if point:
        point_parsed = json.loads(point)
        point = Point(point_parsed)

    watersheds = databc_feature_search(search_layers, search_area=point)

    if not len(watersheds.features):
        return FeatureCollection([])

    watershed_features = [
        Feature(
            geometry=transform(transform_3005_4326, shape(ws.geometry)),
            properties=dict(ws.properties),
            id=ws.id
        ) for i, ws in enumerate(watersheds.features)]

    for feature in watershed_features:
        isoline_runoff = calculate_runnoff_in_area(db, shape(feature.geometry))
        feature.properties["ISOLINE_ANNUAL_RUNOFF"] = isoline_runoff["runoff"]
        feature.properties["ISOLINE_AREA"] = isoline_runoff["area"]

    return FeatureCollection(watershed_features)


@router.get('/calc')
def calculate_watershed(
    db: Session = Depends(get_db),
    point: str = Query(
        "", title="Search point",
        description="Point to search within")
):
    """ calculates watershed area upstream of a POI """
    if not point:
        raise HTTPException(
            status_code=400, detail="No search point. Supply a `point` (geojson geometry)")

    if point:
        point_parsed = json.loads(point)
        point = Point(point_parsed)

    q = """

    SELECT  ST_AsGeoJSON(ST_Union(geom))
    FROM    (
        SELECT
            "GEOMETRY" as geom
        FROM    freshwater_atlas_watersheds
        WHERE   "FWA_WATERSHED_CODE" ilike (
            SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
            FROM    freshwater_atlas_watersheds fwa2
            WHERE   ST_Contains(
                "GEOMETRY",
                ST_SetSRID(ST_GeomFromText(:search_point), 4326)
            )
        )
        AND split_part("LOCAL_WATERSHED_CODE", '-', (
            SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
            FROM freshwater_atlas_watersheds
            WHERE   ST_Contains(
                "GEOMETRY",
                ST_SetSRID(ST_GeomFromText(:search_point), 4326)
            ))::int
        )::int >= split_part((
            SELECT "LOCAL_WATERSHED_CODE"
            FROM freshwater_atlas_watersheds
            WHERE   ST_Contains(
                "GEOMETRY",
                ST_SetSRID(ST_GeomFromText(:search_point), 4326)
            )
        ), '-', (
            SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
            FROM freshwater_atlas_watersheds
            WHERE   ST_Contains(
                "GEOMETRY",
                ST_SetSRID(ST_GeomFromText(:search_point), 4326)
            ))::int
        )::int

    ) combined_watersheds
    """

    # SELECT  ST_AsGeoJSON(ST_Union(geom))
    # FROM    (
    #     SELECT
    #         "GEOMETRY" as geom,
    #         left(right(left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')), 8), 6) as fwa_minor_code
    #     FROM    freshwater_atlas_watersheds
    #     WHERE   "FWA_WATERSHED_CODE" ilike (
    #         SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
    #         FROM    freshwater_atlas_watersheds fwa2
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         )
    #     )
    #     AND   split_part("FWA_WATERSHED_CODE", '-', (
    #         SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         ))::int
    #     )::int > split_part((
    #         SELECT "LOCAL_WATERSHED_CODE"
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         )
    #     ), '-', (
    #         SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         ))::int
    #     )::int
    #     AND split_part("LOCAL_WATERSHED_CODE", '-', (
    #         SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         ))::int
    #     )::int > split_part((
    #         SELECT "LOCAL_WATERSHED_CODE"
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         )
    #     ), '-', (
    #         SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
    #         FROM freshwater_atlas_watersheds
    #         WHERE   ST_Contains(
    #             "GEOMETRY",
    #             ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #         ))::int
    #     )::int

    # AND left(right(left(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')), 8), 6)::int > (
    #     SELECT  left(right(left(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')), 8), 6)::int as fwa_local_code
    #     FROM    freshwater_atlas_watersheds fwa2
    #     WHERE   ST_Contains(
    #         "GEOMETRY",
    #         ST_SetSRID(ST_GeomFromText(:search_point), 4326)
    #     )
    # )

    logger.info('---------------------------------------------------')
    logger.info(point.wkt)
    logger.info('---------------------------------------------------')

    res = db.execute(q, {"search_point": point.wkt})

    fc = FeatureCollection(
        [Feature(geometry=geojson.loads(row[0]), id="Calculated") for row in res])

    return fc


@router.get('/{dataset_watershed_id}')
def watershed_stats(
    db: Session = Depends(get_db),
    dataset_watershed_id: str = Path(...,
                                     title="The watershed ID prefixed by dataset name")


):
    """ aggregates statistics/info about a watershed """

    watershed = get_watershed(dataset_watershed_id)

    watershed_area = watershed.properties['FEATURE_AREA_SQM']

    watershed_poly = shape(watershed.geometry)
    projected_geometry_area = watershed_poly.area

    watershed_rect = watershed_poly.minimum_rotated_rectangle

    glacial_area_m, glacial_coverage = calculate_glacial_area(
        db, transform(transform_3005_4326, watershed_rect))

    return WatershedDetails(
        glacial_coverage=glacial_coverage,
        glacial_area=glacial_area_m,
        watershed_area=watershed_area,
        projected_geometry_area=projected_geometry_area,
    )


@router.get('/{dataset_watershed_id}/licences')
def get_watershed_demand(
    dataset_watershed_id: str = Path(...,
                                     title="The watershed ID prefixed by dataset name")
):
    """ returns data about watershed demand by querying DataBC """

    watershed = get_watershed(dataset_watershed_id)

    watershed_poly = shape(watershed.geometry)

    licence_data = surface_water_rights_licences(
        transform(transform_3005_4326, watershed_poly))

    return licence_data


@router.get('/{dataset_watershed_id}/surficial_geology')
def get_surficial_geology(
    dataset_watershed_id: str = Path(...,
                                     title="The watershed ID prefixed by dataset name")
):
    """ returns data about watershed demand by querying DataBC """

    watershed = get_watershed(dataset_watershed_id)

    watershed_area = watershed.properties['FEATURE_AREA_SQM']

    watershed_poly = shape(watershed.geometry)

    projected_geometry_area = watershed_poly.area

    surf_geol_summary = surficial_geology(
        transform(transform_3005_4326, watershed_poly))

    return surf_geol_summary
