import json
import logging
import requests
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.layers.water_rights_licences import WaterRightsLicenses
from app.analysis.licences.models import WaterRightsLicence
logger = logging.getLogger("api")


def get_licences_by_distance(db: Session, search_point: Point, radius: float) -> list:
    """ List water rights licences by distance from a point.
    """

    if radius > 10000:
        radius = 10000

    # search within a given radius, adding a distance column denoting
    # distance from the centre point in metres
    # geometry columns are cast to geography to use metres as the base unit.
    q = db.query(
        WaterRightsLicenses,
        func.ST_Distance(func.Geography(WaterRightsLicenses.SHAPE),
                         func.ST_GeographyFromText(search_point.wkt)).label('distance')
    ) \
        .filter(
            func.ST_DWithin(func.Geography(WaterRightsLicenses.SHAPE),
                            func.ST_GeographyFromText(search_point.wkt), radius)
    ) \
        .order_by('distance')

    results = q.all()

    licences = [WaterRightsLicence(**row[0].__dict__, distance=row[1]) for row in results]

    return licences
