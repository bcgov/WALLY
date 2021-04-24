import geoalchemy2
from sqlalchemy import String, Column, DateTime, ARRAY, TEXT, Integer, ForeignKey, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from api.db.base_class import BaseTable, BaseAudit
from api.v1.user.db_models import User
import uuid


class GeneratedWatershed(BaseAudit):
    __tablename__ = 'generated_watershed'
    __table_args__ = {'schema': 'public'}

    generated_watershed_id = Column(Integer, primary_key=True)
    wally_watershed_id = Column(String, comment='WALLY watershed identifier used to recreate watersheds. '
                                                'The format is the upstream delineation method followed by '
                                                'the POI encoded as base64.')
    processing_time = Column(
        Numeric, comment='How long it took to calculate this watershed.')
    upstream_method = Column(
        String, comment='The method used to calculate this watershed e.g. FWA+UPSTREAM, DEM+FWA etc.')
    is_near_border = Column(Boolean, comment='Indicates whether this watershed was determined to be near a border. '
                            'This affects how it was generated and refined.')
    click_point = Column(
        geoalchemy2.types.Geometry(
            geometry_type='POINT', srid=4326), comment='The coordinates of the original click point.')
    snapped_point = Column(geoalchemy2.types.Geometry(
        geometry_type='POINT', srid=4326), comment='The coordinates used for delineation after snapping to a Flow Accumulation raster stream line.')
    area_sqm = Column(Numeric, comment='Area in square metres')
    cached_polygon = relationship(
        "WatershedCache", backref="generated_watershed", passive_deletes=True)


class ApproxBorders(BaseTable):
    """ approximate border locations with WA/ID/MT/AB/NWT/YK/AK
        note that these may be drawn within BC, near the actual border, to help warn when approaching a boundary.
    """
    __tablename__ = 'fwa_approx_borders'
    __table_args__ = {'schema': 'public'}
    approx_border_id = Column(Integer, primary_key=True)
    border = Column(TEXT,  autoincrement=False, nullable=True)
    geom = Column(geoalchemy2.types.Geometry(
        geometry_type='LINESTRING', srid=3005, spatial_index=True))


class WatershedCache(BaseTable):
    __tablename__ = 'watershed_cache'
    __table_args__ = {'schema': 'public'}

    generated_watershed_id = Column(Integer, ForeignKey(GeneratedWatershed.generated_watershed_id),
                                    comment='The GeneratedWatershed record this cached polygon is associated with.', primary_key=True)
    watershed = Column(JSONB, nullable=False)
    last_accessed_date: Column(DateTime, nullable=False)
