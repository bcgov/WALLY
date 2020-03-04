# coding: utf-8
from sqlalchemy import Integer, String, Column, Float, DateTime
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ARRAY


class UpstreamWatershedCache(BaseLayerTable):
    __tablename__ = 'upstream_watershed_cache'
    upstream_watershed_cache_id = Column(Integer, primary_key=True, autoincrement=True)
    watershed_feature_id = Column(Integer, index=True, comment='watershed_feature_id represents the base '
                                  'feature/polygon from the Freshwater Atlas Watersheds that we want to find features upstream of.')
    include_features = Column(ARRAY(Integer), comment='additional features included in this polygon')
    geom = Column(Geometry(geometry_type='Polygon'), comment='The cached Polygon geometry')
    create_date = Column(DateTime, comment="Date that this cache record was created")
    update_date = Column(DateTime, comment="Date that this cache record was updated")
    expiry_date = Column(DateTime, comment="Date that this cache record should expire")
