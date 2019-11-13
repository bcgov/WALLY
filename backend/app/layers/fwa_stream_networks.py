from sqlalchemy import Integer, String, Column, Float
from app.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry


class FwaStreamNetwork(BaseLayerTable):
    __tablename__ = 'fwa_stream_networks'

    ogc_fid = Column(Integer, primary_key=True)
    linear_feature_id = Column(Integer)
    watershed_group_id = Column(Integer)
    edge_type = Column(Integer)
    blue_line_key = Column(Integer)
    watershed_key = Column(Integer)
    fwa_watershed_code = Column(String)
    local_watershed_code = Column(String)
    watershed_group_code = Column(String)
    downstream_route_measure = Column(Float(53))
    length_metre = Column(Float(53))
    feature_source = Column(String)
    gnis_id = Column(Integer)
    gnis_name = Column(String)
    left_right_tributary = Column(String)
    stream_order = Column(Integer)
    stream_magnitude = Column(Integer)
    waterbody_key = Column(Integer)
    blue_line_key_50k = Column(Integer)
    watershed_code_50k = Column(String)
    watershed_key_50k = Column(Integer)
    watershed_group_code_50k = Column(String)
    gradient = Column(String)
    feature_code = Column(String)
    objectid = Column(Integer)
    se_anno_cad_data = Column(String)
    feature_length_m = Column(Float(53))
    geometry_len = Column('geometry.len', Integer)
    fme_feature_type = Column(String)
    geom = Column(Geometry('LINESTRING', 4326), index=True)
