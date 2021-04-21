from geoalchemy2 import Geometry, MultiPolygon, Point
from sqlalchemy import String, Column, DateTime, ARRAY, TEXT, Integer, ForeignKey, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from api.db.base_class import BaseTable
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.v1.user.db_models import User

import uuid


class Base(object):
    pass


Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


class GeneratedWatershed(Base):
    __tablename__ = 'generated_watershed'
    __table_args__ = {'schema': 'public'}

    generated_watershed_id = Column(Integer, primary_key=True)
    wally_watershed_id = Column(String, comment='WALLY watershed identifier used to recreate watersheds. '
                                                'The format is the upstream delineation method followed by '
                                                'the POI encoded as base64.')
    create_date = Column(
        DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    create_user = Column(UUID, ForeignKey(User.user_uuid),
                         comment='User who generated this watershed')

    processing_time = Column(
        Numeric, comment='How long it took to calculate this watershed.')
    upstream_method = Column(
        String, comment='The method used to calculate this watershed e.g. FWA+UPSTREAM, DEM+FWA etc.')
    is_near_border = Column(Boolean, comment='Indicates whether this watershed was determined to be near a border. '
                            'This affects how it was generated and refined.')
    click_point = Column(
        Point(srid=4326), comment='The coordinates of the original click point.')
    snapped_point = Column(Point(
        srid=4326), comment='The coordinates used for delineation after snapping to a Flow Accumulation raster stream line.')
    area_sqm = Column(Numeric, comment='Area in square metres')
    cached_polygon = relationship(
        "WatershedPolygonCache", backref="generated_watershed", passive_deletes=True, lazy='joined')


class WatershedPolygonCache(Base):
    __tablename__ = 'watershed_cache'
    __table_args__ = {'schema': 'public'}

    generated_watershed_id = Column(Integer, ForeignKey(GeneratedWatershed.generated_watershed_id),
                                    comment='The GeneratedWatershed record this cached polygon is associated with.', primary_key=True)
    geom = Column(MultiPolygon(srid=4326))
