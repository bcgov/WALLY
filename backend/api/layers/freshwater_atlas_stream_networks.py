from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry


class FreshwaterAtlasStreamNetworks(BaseLayerTable):
    __tablename__ = 'fwa_stream_networks_sp'

    LINEAR_FEATURE_ID = Column(
        'linear_feature_id', Integer, index=True, primary_key=True)
    WATERSHED_GROUP_ID = Column('watershed_group_id', Integer)
    EDGE_TYPE = Column('edge_type', Integer)
    BLUE_LINE_KEY = Column('blue_line_key', Integer)
    FWA_WATERSHED_CODE = Column('fwa_watershed_code', String)
    LOCAL_WATERSHED_CODE = Column('local_watershed_code', String)
    DOWNSTREAM_ROUTE_MEASURE = Column('downstream_route_measure', Float(53))
    LENGTH_METRE = Column('length_metre', Float(53))
    FEATURE_SOURCE = Column('feature_source', String)
    GNIS_ID = Column('gnis_id', Integer)
    GNIS_NAME = Column('gnis_name', String)
    LEFT_RIGHT_TRIBUTARY = Column('left_right_tributary', String)
    STREAM_ORDER = Column('stream_order', Integer)
    STREAM_MAGNITUDE = Column('stream_magnitude', Integer)
    WATERBODY_KEY = Column('waterbody_key', Integer)
    BLUE_LINE_KEY_50K = Column('blue_line_key_50k', Integer)
    WATERSHED_CODE_50K = Column('watershed_code_50k', String)
    WATERSHED_KEY_50K = Column('watershed_key_50k', Integer)
    WATERSHED_GROUP_CODE_50K = Column('watershed_group_code_50k', String)
    GRADIENT = Column('gradient', String)
    FEATURE_CODE = Column('feature_code', String)
    GEOMETRY = Column('geom', Geometry(srid=4326), index=True)

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name == "GEOMETRY" or column.name == "SHAPE" or column.name == "geom" or column.name == "GEOMETRY.LEN":
                continue
            d[column.name] = str(getattr(self, column.name))
        return d

    __table_args__ = {'schema': 'whse_basemapping'}
