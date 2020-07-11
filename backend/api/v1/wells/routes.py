import json
import geojson
from typing import List
from logging import getLogger
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from shapely.geometry import Point, LineString, mapping

from api.db.utils import get_db
from api.v1.wells.schema import WellDrawdown, CrossSection, CrossSectionExport, WellsExport
from api.v1.aggregator.excel import geojson_to_xlsx
from api.v1.elevations.controllers.profile import get_profile_line_by_length
from api.v1.elevations.controllers.surface import fetch_surface_lines
from api.v1.wells.controller import (
    get_wells_by_distance,
    get_waterbodies_along_line,
    merge_wells_datasources,
    create_line_buffer,
    get_wells_with_drawdown,
    get_wells_by_aquifer,
    get_wells_along_line,
    get_line_buffer_polygon,
    get_parallel_line_offset,
    get_cross_section_export
)

logger = getLogger("wells")

router = APIRouter()


@router.get("/nearby", response_model=List[WellDrawdown])
def get_nearby_wells(
        point: str = Query(..., title="Point of interest",
                           description="Point of interest to centre search at"),
        radius: float = Query(1000, title="Search radius",
                              description="Search radius from point", ge=0, le=10000),
):
    """ finds wells near a given point
        gets wells and their corresponding subsurface data from GWELLS
        and computes distance
    """
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    wells_nearby = get_wells_with_drawdown(point_shape, radius)

    return wells_nearby


@router.get("/nearby/aquifers")
def get_nearby_wells_by_aquifer(
        point: str = Query(..., title="Point of interest",
                           description="Point of interest to centre search at"),
        radius: float = Query(1000, title="Search radius",
                              description="Search radius from point", ge=0, le=10000),
):
    """ finds wells near to a point
        fetches distance data using the Wally database, and combines
        it with subsurface data from GWELLS
    """
    point_parsed = json.loads(point)
    point_shape = Point(point_parsed)

    return get_wells_by_aquifer(point_shape, radius)


@router.post("/nearby/export")
def export_nearby_wells(
        req: WellsExport
):
    """ 
    finds wells near to a point
    fetches distance data using the Wally database,
    combines it with screen data from GWELLS and
    filters based on well list in request
    """
    point_parsed = json.loads(req.point)
    export_wells = req.export_wells

    well_tag_numbers = ','.join([str(wtn) for wtn in export_wells])
    point_shape = Point(point_parsed)

    wells_drawdown_data = get_wells_with_drawdown(point_shape, req.radius, well_tag_numbers)
    wells_copy = [well.dict(exclude={'screen_set'}) for well in wells_drawdown_data]

    # flatten pertinent aquifer information for export
    for well in wells_copy:
        if well['aquifer']:
            aquifer = well.get('aquifer')
            well['aquifer_id'] = aquifer.get('aquifer_id')
            well['aquifer_material'] = aquifer.get('material_desc')
            del well['aquifer']

    return geojson_to_xlsx(
        [geojson.FeatureCollection(
            [
                geojson.Feature(
                    geometry=geojson.Point([x.get('longitude'), x.get('latitude')]),
                    properties=x
                ) for x in wells_copy
            ],
            properties={
                "name": "Available drawdown"
            }
        )]
    )


@router.get("/section", response_model=CrossSection)
def get_wells_section(
        db: Session = Depends(get_db),
        line: str = Query(..., title="Section line",
                          description="Section line along which wells will be plotted"),
        radius: float = Query(200, title="Search radius",
                              description="Search radius (or offset) from line", ge=0, le=10000)
):
    """ search for wells along a line, returning a cross section of well data """

    line_parsed = json.loads(line)
    line_shape = LineString(line_parsed)

    left = get_parallel_line_offset(db, line_shape, -radius)
    left_half = get_parallel_line_offset(db, line_shape, -radius / 2)
    right = get_parallel_line_offset(db, line_shape, radius)
    right_half = get_parallel_line_offset(db, line_shape, radius / 2)
    lines = [left[0], left_half[0], line_shape.wkt, right_half[0], right[0]]

    # surface of 5 lines used for 3d display
    try:
        surface = fetch_surface_lines(lines)
    except:
        raise HTTPException(
            status_code=502, detail="unable to retrieve elevations from GeoGratis CDEM API")

    profile_line_linestring = surface[2]
    profile_line = get_profile_line_by_length(db, profile_line_linestring)
    wells_along_line = get_wells_along_line(
        db, profile_line_linestring, radius)

    buffer = create_line_buffer(profile_line_linestring, radius)

    surface_lines = [list(line.coords) for line in surface]
    # we need to reverse the point lists for the -radius results
    surface_lines[0].reverse()
    surface_lines[1].reverse()

    # waterbodies that cross profile
    waterbodies_along_line = get_waterbodies_along_line(
        line_shape, profile_line_linestring)

    # logger.info(surface_lines)
    section = CrossSection(search_area=mapping(buffer), wells=wells_along_line,
                           waterbodies=waterbodies_along_line,
                           elevation_profile=profile_line, surface=surface_lines)

    return section


@router.post("/section/export")
def get_wells_section_export(
        req: CrossSectionExport
):
    """ gather well information for many wells and export an excel report """

    return get_cross_section_export(req)
