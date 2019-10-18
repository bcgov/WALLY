"""
Database tables and data access functions for Water Survey of Canada's
National Water Data Archive Hydrometic Data
"""
import logging

from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point
from app.layers.ground_water_wells import GroundWaterWells

logger = logging.getLogger("api")


def get_wells_by_distance(db: Session, search_point: Point, radius: float):
    """ List wells by distance from a point.
    """

    if radius > 10000:
        # some regions have thousands of wells in a 10km radius... limit search to that.
        return []

    # search within a given radius, adding a distance column denoting
    # distance from the centre point in metres
    # geometry columns are cast to geography to use metres as the base unit.
    q = db.query(GroundWaterWells) \
        .filter(
            func.ST_DWithin(func.Geography(GroundWaterWells.GEOMETRY),
                            func.ST_GeographyFromText(search_point.wkt), radius)
    ) \
        .with_entities(
            GroundWaterWells.WELL_TAG_NO,
            func.ST_Distance(func.Geography(GroundWaterWells.GEOMETRY),
                             func.ST_GeographyFromText(search_point.wkt)).label('distance')
    ).order_by('distance')

    return q.all()
