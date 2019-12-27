import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session

from api.layers.first_nations import CommunityLocations, TreatyAreas, TreatyLands
from api.v1.firstnations.schema import (
    Community as CommunityResponse,
    TreatyAreas as TreatyAreasResponse,
    TreatyLands as TreatyLandsResponse,
    NearbyAreasResponse
)
logger = logging.getLogger("api")

# arbitrary maximum radius (in metres) to search within.
# in the future, this could be a user-configurable option.
MAX_RADIUS = 50000


def get_nearest_communities(db: Session, geometry):
    """ get nearest First Nations Community Locations"""

    community_q = db.query(
        CommunityLocations,
        func.ST_Distance(func.Geography(CommunityLocations.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(CommunityLocations.SHAPE),
                            func.ST_GeographyFromText(geometry.wkt), MAX_RADIUS)
    ) \
        .order_by('distance')

    community_results = community_q.all()

    return [CommunityResponse(
        **row[0].__dict__, distance=row[1]) for row in community_results]


def get_nearest_treaty_lands(db: Session, geometry):
    """ gets nearest First Nations Treaty Lands """

    land_q = db.query(
        TreatyLands,
        func.ST_Distance(func.Geography(TreatyLands.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
        func.ST_DWithin(func.Geography(TreatyLands.SHAPE),
                        func.ST_GeographyFromText(geometry.wkt), MAX_RADIUS)
    ) \
        .order_by('distance')
    land_results = land_q.all()

    return [TreatyLandsResponse(**row[0].__dict__, distance=row[1])
            for row in land_results]


def get_nearest_treaty_areas(db: Session, geometry):
    """ gets the nearest First Nations Treaty Areas """
    area_q = db.query(
        TreatyAreas,
        func.ST_Distance(func.Geography(TreatyAreas.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
        func.ST_DWithin(func.Geography(TreatyAreas.SHAPE),
                        func.ST_GeographyFromText(geometry.wkt), MAX_RADIUS)
    ) \
        .order_by('distance')
    area_results = area_q.all()

    return [TreatyAreasResponse(**row[0].__dict__, distance=row[1])
            for row in area_results]


def get_nearest_locations(db: Session, geometry):
    """
    returns the nearest areas and locations from the following datasets (available on DataBC):
    First Nations Community Locations
    First Nations Treaty Lands
    First Nations Treaty Areas
    """
    return NearbyAreasResponse(
        nearest_communities=get_nearest_communities(db, geometry),
        nearest_treaty_areas=get_nearest_treaty_areas(db, geometry),
        nearest_treaty_lands=get_nearest_treaty_lands(db, geometry)
    )
