from sqlalchemy import Integer, String, Column, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry


class FreshwaterAtlasStreamNetworks(BaseLayerTable):
    __tablename__ = 'freshwater_atlas_stream_networks'

    OGC_FID = Column(Integer, primary_key=True)
    LINEAR_FEATURE_ID = Column(Integer, index=True)
    WATERSHED_GROUP_ID = Column(Integer)
    EDGE_TYPE = Column(Integer)
    BLUE_LINE_KEY = Column(Integer)
    WATERSHED_KEY = Column(Integer)
    FWA_WATERSHED_CODE = Column(String)
    LOCAL_WATERSHED_CODE = Column(String)
    WATERSHED_GROUP_CODE = Column(String)
    DOWNSTREAM_ROUTE_MEASURE = Column(Float(53))
    LENGTH_METRE = Column(Float(53))
    FEATURE_SOURCE = Column(String)
    GNIS_ID = Column(Integer)
    GNIS_NAME = Column(String)
    LEFT_RIGHT_TRIBUTARY = Column(String)
    STREAM_ORDER = Column(Integer)
    STREAM_MAGNITUDE = Column(Integer)
    WATERBODY_KEY = Column(Integer)
    BLUE_LINE_KEY_50K = Column(Integer)
    WATERSHED_CODE_50K = Column(String)
    WATERSHED_KEY_50K = Column(Integer)
    WATERSHED_GROUP_CODE_50K = Column(String)
    GRADIENT = Column(String)
    FEATURE_CODE = Column(String)
    OBJECTID = Column(Integer)
    SE_ANNO_CAD_DATA = Column(String)
    FEATURE_LENGTH_M = Column(Float(53))
    GEOMETRY_LEN = Column('GEOMETRY.LEN', Integer)
    fme_feature_type = Column(String)
    GEOMETRY = Column(Geometry(srid=4326), index=True)

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name == "GEOMETRY" or column.name == "SHAPE" or column.name == "geom" or column.name == "GEOMETRY.LEN":
                continue
            d[column.name] = str(getattr(self, column.name))
        return d
