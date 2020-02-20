# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ARRAY


class UpstreamWatershedCache(BaseLayerTable):
    __tablename__ = 'upstream_watershed_cache'

    watershed_feature_id = Column(Integer, primary_key=True, autoincrement=False, comment='watershed_feature_id represents the base '
                                  'feature/polygon from the Freshwater Atlas Watersheds that we want to find features upstream of.')
    include_features = Column(ARRAY(Integer), comment='additional features included in this polygon')
    geom = Column(Geometry(geometry_type='Polygon'), comment='The cached Polygon geometry')
    area = Column(Float, comment='The area of the polygon in square metres')
