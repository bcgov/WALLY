import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session

from app.layers.first_nations import CommunityLocation, TreatyArea, TreatyLand
from app.analysis.first_nations.models import (
    Community as CommunityResponse,
    TreatyArea as TreatyAreaResponse,
    TreatyLand as TreatyLandResponse,
    NearbyAreasResponse
)
logger = logging.getLogger("api")


def get_nearest_areas(db: Session, geometry):
    logger.info(geometry)

    # limit search to this radius
    radius = 50000

    community_q = db.query(
        CommunityLocation,
        func.ST_Distance(func.Geography(CommunityLocation.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(CommunityLocation.SHAPE),
                            func.ST_GeographyFromText(geometry.wkt), radius)
    ) \
        .order_by('distance')

    community_results = community_q.all()

    communities = [CommunityResponse(
        **row[0].__dict__, distance=row[1]) for row in community_results]

    area_q = db.query(
        TreatyArea,
        func.ST_Distance(func.Geography(TreatyArea.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
        func.ST_DWithin(func.Geography(TreatyArea.SHAPE),
                        func.ST_GeographyFromText(geometry.wkt), radius)
    ) \
        .order_by('distance')
    area_results = area_q.all()

    areas = [TreatyAreaResponse(**row[0].__dict__, distance=row[1])
             for row in area_results]

    land_q = db.query(
        TreatyLand,
        func.ST_Distance(func.Geography(TreatyLand.SHAPE),
                         func.ST_GeographyFromText(geometry.wkt)).label('distance')
    ) \
        .filter(
        func.ST_DWithin(func.Geography(TreatyLand.SHAPE),
                        func.ST_GeographyFromText(geometry.wkt), radius)
    ) \
        .order_by('distance')
    land_results = land_q.all()

    lands = [TreatyLandResponse(**row[0].__dict__, distance=row[1])
             for row in land_results]

    response = NearbyAreasResponse(
        nearest_communities=communities,
        nearest_treaty_areas=areas,
        nearest_treaty_lands=lands
    )

    return response
