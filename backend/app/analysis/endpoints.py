"""
Analysis functions for data in the Wally system
"""
import json
import geojson
from typing import List
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy import func
from sqlalchemy.orm import Session
from shapely.geometry import Point, shape, LineString
from shapely import wkt
from geoalchemy2.shape import to_shape
from app.db.utils import get_db
from app.analysis.wells.well_analysis import (
    get_wells_by_distance,
    merge_wells_datasources,
    get_screens,
    get_wells_along_line,
    get_line_buffer_polygon,
    get_parallel_line_offset
)
from app.analysis.licences.licence_analysis import get_licences_by_distance
from app.analysis.wells.models import WellDrawdown, WellSection, CrossSection
from app.analysis.licences.models import WaterRightsLicence
from app.analysis.wells.elevation_profile import (
    get_profile_geojson, geojson_to_profile_line, profile_line_by_length
)
from app.analysis.wells.elevation_surface import fetch_surface_lines
from app.analysis.first_nations.nearby_areas import get_nearest_locations
from app.analysis.first_nations.models import NearbyAreasResponse
logger = getLogger("geocoder")

router = APIRouter()


@router.get("/analysis/wells/nearby", response_model=List[WellDrawdown])
def get_nearby_wells(
        db: Session = Depends(get_db),
        point: str = Query(..., title="Point of interest",
                           description="Point of interest to centre search at"),
        radius: float = Query(1000, title="Search radius",
                              description="Search radius from point", ge=0, le=10000)
):
    """ finds wells near to a point
        fetches distance data using the Wally database, and combines
        it with screen data from GWELLS
    """

    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    wells_with_distances = get_wells_by_distance(db, point_shape, radius)

    # convert nearby wells to a list of strings of well tag numbers
    wells_to_search = map(lambda x: str(
        int(x[0])).lstrip("0"), wells_with_distances)

    wells_with_screens = get_screens(list(wells_to_search))

    wells_drawdown_data = merge_wells_datasources(
        wells_with_screens, wells_with_distances)

    return wells_drawdown_data


@router.get("/analysis/licences/nearby", response_model=List[WaterRightsLicence])
def get_nearby_licences(
        db: Session = Depends(get_db),
        point: str = Query(..., title="Point of interest",
                           description="Point of interest to centre search at"),
        radius: float = Query(1000, title="Search radius",
                              description="Search radius from point", ge=0, le=10000)
):
    """ search for licences near a point """
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    licences_with_distances = get_licences_by_distance(db, point_shape, radius)
    return licences_with_distances


@router.get("/analysis/wells/section", response_model=CrossSection)
def get_wells_section(
        db: Session = Depends(get_db),
        line: str = Query(..., title="Section line", description="Section line along which wells will be plotted"),
        radius: float = Query(200, title="Search radius",
                              description="Search radius (or offset) from line", ge=0, le=10000)
):
    """ search for wells along a line, returning a cross section of well data """

    line_parsed = json.loads(line)
    line_shape = LineString(line_parsed)

    left = get_parallel_line_offset(db, line_shape, -radius)
    right = get_parallel_line_offset(db, line_shape, radius)
    lines = [left[0], line_shape.wkt, right[0]]
    surface = fetch_surface_lines(lines) # surface of 3 lines used for 3d display

    profile_line_linestring = surface[1]
    profile_line = profile_line_by_length(db, profile_line_linestring)
    wells_along_line = get_wells_along_line(db, profile_line_linestring, radius)

    buffer = db.query(
        func.ST_asGeoJSON(get_line_buffer_polygon(
            profile_line_linestring, radius)).label('search_area')
    ).first()

    surface_lines = [list(line.coords) for line in surface]
    logger.info(surface_lines)

    section = CrossSection(search_area=geojson.loads(
        buffer[0]), wells=wells_along_line,
        elevation_profile=profile_line, surface=surface)

    return section


@router.get("/analysis/firstnations/nearby", response_model=NearbyAreasResponse)
def get_nearby_first_nations_areas(
    db: Session = Depends(get_db),
    geometry: str = Query(...,
                          title="Geometry to search near",
                          description="Geometry (such as a point or polygon) to search within and near to")
):
    """
    Search for First Nations Communities, First Nations Treaty Areas and First Nations Treaty Lands near a feature
    """
    geometry_parsed = json.loads(geometry)
    geometry_shape = shape(geometry_parsed)
    nearest = get_nearest_locations(db, geometry_shape)
    return nearest
