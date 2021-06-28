"""
Map layers (layers module) API endpoints/handlers.
"""
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from geojson import FeatureCollection, Feature, Point
from sqlalchemy.orm import Session
from api.db.utils import get_db
from api.v1.hydat.db_models import Station as StreamStation, DailyFlow, DailyLevel
from api.v1.hydat.controller import get_fasstr_flow_stats, get_fasstr_longterm_summary
import api.v1.hydat.schema as hydat_schema

logger = getLogger("hydat")

router = APIRouter()


@router.get("/all")
def list_stations(db: Session = Depends(get_db)):
    """
    List stream monitoring stations from data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """

    # fetch stations from database
    stations = db.query(StreamStation).filter(
        StreamStation.prov_terr_state_loc == 'BC')

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


@router.get("/{station_number}", response_model=hydat_schema.StreamStationResponse)
def get_station(station_number: str, db: Session = Depends(get_db)):
    """
    Get information about a stream monitoring station. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """

    # get basic station info
    stn = db.query(StreamStation).get(station_number)

    if not stn:
        raise HTTPException(status_code=404, detail="Station not found")

    # get list of years for which data is available at this station
    # this helps hint at which years are worth displaying on selection boxes, etc.
    flow_years = DailyFlow.get_available_flow_years(db, station_number)
    level_years = DailyLevel.get_available_level_years(db, station_number)

    # combine queries/info into the StreamStation API model
    data = hydat_schema.StreamStationResponse(
        name=stn.station_name,
        url=f"/api/v1/hydat/{stn.station_number}",
        flow_years=[stn.year for stn in flow_years],
        level_years=[stn.year for stn in level_years],
        stream_flows_url=f"/api/v1/hydat/{stn.station_number}/flows",
        stream_levels_url=f"/api/v1/hydat/{stn.station_number}/levels",
        stream_stats_url=f"/api/v1/hydat/{stn.station_number}/stats",
        external_urls=[
            {
                "name": "Real-Time Hydrometric Data (Canada)",
                "url": f"https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={stn.station_number}"
            },
        ],
        **stn.__dict__)
    return data


@router.get("/{station_number}/levels", response_model=List[hydat_schema.MonthlyLevel])
def list_monthly_levels_by_year(station_number: str, year: int = None, db: Session = Depends(get_db)):
    """ Monthly average levels for a given station and year. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html
    """
    # check station exists
    stn = db.query(StreamStation).get(station_number)
    if not stn:
        raise HTTPException(status_code=404, detail="Station not found")

    return DailyLevel.get_monthly_levels_by_station(db, station_number, year)


@router.get("/{station_number}/flows")
def list_monthly_flows_by_year(station_number: str, year: int = None, db: Session = Depends(get_db)):
    """ Monthly average flows for a given station and year. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html """

    # check station exists
    stn = db.query(StreamStation).get(station_number)
    if not stn:
        raise HTTPException(status_code=404, detail="Station not found")

    if not year:
        return get_fasstr_longterm_summary(db, station_number)

    return DailyFlow.get_monthly_flows_by_station(db, station_number, year)


@router.get("/{station_number}/stats", response_model=hydat_schema.FASSTRFlowStatsSummary)
def list_monthly_flows_by_year(station_number: str, full_years: bool = True, db: Session = Depends(get_db)):
    """ Monthly average flows for a given station and year. Data sourced from the National Water Data Archive.

    https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html """

    return get_fasstr_flow_stats(db, station_number, full_years)
