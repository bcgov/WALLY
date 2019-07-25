"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from app.db.utils import get_db
import app.hydat.db as streams_repo
import app.hydat.models as streams_v1

logger = getLogger("api")

router = APIRouter()


@router.get("/hydat")
def list_stations(db: Session = Depends(get_db)):
    """
    List stream monitoring stations from data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """

    # fetch stations from database
    stations = streams_repo.get_stations(db)

    # add properties to geojson Feature objects
    points = [
        Feature(
            geometry=Point((stn.longitude, stn.latitude)),
            id=stn.station_number,
            properties={
                "name": stn.station_name,
                "type": "hydat",
                "url": f"/api/v1/hydat/{stn.station_number}",
                "description": "Stream discharge and water level data",
            }
        ) for stn in stations
    ]

    fc = FeatureCollection(points)
    return fc


@router.get("/hydat/{station_number}", response_model=streams_v1.StreamStation)
def get_station(station_number: str, db: Session = Depends(get_db)):
    """
    Get information about a stream monitoring station. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """

    # get basic station info
    stn = streams_repo.get_station_details(db, station_number)

    # get list of years for which data is available at this station
    # this helps hint at which years are worth displaying on selection boxes, etc.
    flow_years = streams_repo.get_available_flow_years(db, station_number)
    level_years = streams_repo.get_available_level_years(db, station_number)

    # combine queries/info into the StreamStation API model
    data = streams_v1.StreamStation(
        flow_years=[row.year for row in flow_years],
        level_years=[row.year for row in level_years],
        stream_flows_url=f"/api/v1/hydat/{stn.station_number}/flows",
        stream_levels_url=f"/api/v1/hydat/{stn.station_number}/levels",
        external_urls=[
            {
                "name": "Real-Time Hydrometric Data (Canada)",
                "url": f"https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={stn.station_number}"
            },
        ],
        **stn.__dict__)
    return data


@router.get("/hydat/{station_number}/levels", response_model=List[streams_v1.MonthlyLevel])
def list_monthly_levels_by_year(station_number: str, year: int = 2018, db: Session = Depends(get_db)):
    """ Monthly average levels for a given station and year. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """

    return streams_repo.get_monthly_levels_by_station(db, station_number, year)


@router.get("/hydat/{station_number}/flows", response_model=List[streams_v1.MonthlyFlow])
def list_monthly_flows_by_year(station_number: str, year: int = 2018, db: Session = Depends(get_db)):
    """ Monthly average flows for a given station and year. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html """

    return streams_repo.get_monthly_flows_by_station(db, station_number, year)
