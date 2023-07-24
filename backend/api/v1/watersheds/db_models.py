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
    dem_source = Column(
        String, comment='The name of the Digital Elevation Model used, e.g. CDEM or SRTM', nullable=True)
    click_point = Column(
        geoalchemy2.types.Geometry(
            geometry_type='POINT', srid=4326), comment='The coordinates of the original click point.')
    snapped_point = Column(
        geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326),
        comment='The coordinates used for delineation after snapping to a Flow Accumulation raster stream line.')
    area_sqm = Column(Numeric, comment='Area in square metres')
    cached_polygon = relationship(
        "WatershedCache", backref="generated_watershed", passive_deletes=True)
    dem_error = Column(
        Boolean,
        comment='Indicates if an error with the DEM watershed was flagged. '
        'The generated watershed will fall back on the FWA polygon watershed. '
        'Only applies to type DEM+FWA.')


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

    generated_watershed_id = Column(
        Integer, ForeignKey(GeneratedWatershed.generated_watershed_id),
        comment='The GeneratedWatershed record this cached polygon is associated with.', primary_key=True)
    watershed = Column(JSONB, nullable=False)
    last_accessed_date: Column(DateTime, nullable=False)


class StreamBurnedCDEMTile(BaseTable):
    """ Footprints for stream-burned CDEM tiles
        A filename reference is included for use with GDAL /vsis3/
        virtual filesystem and Minio/S3 storage.
        All filenames referenced in this table must be present in the S3 storage 'raster' bucket.
    """
    __tablename__ = 'stream_burned_cdem_tile'
    __table_args__ = {'schema': 'public'}

    stream_burned_cdem_tile_id = Column(Integer, primary_key=True)
    resolution = Column(
        Numeric, comment="The approximate/nominal resolution of this tile in metres per pixel", nullable=False)
    z_precision = Column(
        Integer, comment="Approximate precision of the z/elevation value.  0 for CDEM to indicate 1 m increments.",
        nullable=False)
    filename = Column(TEXT, comment="An s3 filename reference. Do not include bucket name.", nullable=False)
    geom = Column(geoalchemy2.types.Geometry(
        geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True))
