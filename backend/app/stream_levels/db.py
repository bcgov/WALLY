from sqlalchemy import Column, Integer, Float, String
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from app.db.base_class import BaseTable

import app.stream_levels.models as streams_v1


class StreamStation(BaseTable):
    """ 
    A station where stream data is collected
    Data and schema from National Water Data Archive
    https://www.canada.ca/en/environment-climate-change/services/water-overview/ \
        quantity/monitoring/survey/data-products-services/national-archive-hydat.html

    """
    __tablename__ = "stations"

    station_number = Column(String, primary_key=True)
    station_name = Column(String)
    prov_terr_state_loc = Column(String)
    regional_office_id = Column(String)
    hyd_status = Column(String)
    sed_status = Column(String)
    latitude = Column(DOUBLE_PRECISION)
    longitude = Column(DOUBLE_PRECISION)
    drainage_area_gross = Column(DOUBLE_PRECISION)
    drainage_area_effect = Column(DOUBLE_PRECISION)
    rhbn = Column(Integer)
    real_time = Column(Integer)
    sed_status = Column(Integer)


def get_stations(db: Session) -> List[streams_v1.StreamStation]:
    return db.query(StreamStation).filter(StreamStation.prov_terr_state_loc == 'BC').all()
