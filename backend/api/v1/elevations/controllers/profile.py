""" functions for generating an elevation profile """
from geojson import Feature
from typing import List
import requests
from sqlalchemy.orm import Session
from shapely.geometry import LineString
from logging import getLogger

from api.v1.elevations.schema import Elevation

logger = getLogger("elevations.profile")


def get_profile_geojson(line: LineString) -> List[Feature]:
    """ get geojson elevations along a line (GeoGratis - Government of Canada) """
    steps = 10

    line = line.wkt

    if not line:
        return []

    resp = requests.get(
        f"http://geogratis.gc.ca/services/elevation/cdem/profile.json?path={line}&steps={steps}"
    )

    return resp.json()


def geojson_to_profile_line(elevations: List[Feature]) -> LineString:
    """ uses GeoGratis (Government of Canada) API to retrieve elevation along a profile
    line (as a LineString shape object"""

    profile_line = LineString(
        [
            (
                f.get("geometry").get("coordinates")[0],
                f.get("geometry").get("coordinates")[1],
                f.get("altitude")
            ) for f in elevations
        ]
    )

    return profile_line


def get_profile_line_by_length(db: Session, line: LineString):
    """ convert a LineStringZ (3d line) to elevations along the length of the line """

    q = """
    SELECT
            ST_Distance(ST_Force2D(geom),
                ST_StartPoint(
                    ST_Transform(
                        ST_SetSRID(
                            ST_GeomFromText(:line),
                            4326
                        ),
                        3005
                    )
                )
            ) as distance_from_origin,
            ST_Z(geom) as elevation
    FROM
        (select
            (
                ST_DumpPoints(
                    ST_Transform(
                        ST_SetSRID(
                            ST_GeomFromText(:line),
                            4326
                        ),
                        3005
                    )
                )
            ).geom
        ) as pts;
    """

    elevation_profile = []

    rows = db.execute(q, {"line": line.wkt})
    for row in rows:
        elevation_profile.append(Elevation(distance_from_origin=row[0], elevation=row[1]))

    return elevation_profile
