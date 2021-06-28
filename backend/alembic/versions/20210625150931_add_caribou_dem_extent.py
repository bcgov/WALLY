"""add caribou dem extent

Revision ID: 4a24ff1d746e
Revises: bb906a00fbe7
Create Date: 2021-06-25 15:09:31.861834

"""
from alembic import op
import fiona
import os
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.db.base_class import BaseTable
from shapely.geometry import shape, MultiPolygon

# revision identifiers, used by Alembic.
revision = '4a24ff1d746e'
down_revision = 'bb906a00fbe7'
branch_labels = None
depends_on = None

Base = declarative_base()


class StreamBurnedCDEMTile(Base):
    """ Footprints for stream-burned CDEM tiles
        A filename reference is included for use with GDAL /vsis3/
        virtual filesystem and Minio/S3 storage.
        All filenames referenced in this table must be present in the S3 storage 'raster' bucket.
    """
    __tablename__ = 'stream_burned_cdem_tile'
    __table_args__ = {'schema': 'dem', 'extend_existing': True}

    stream_burned_cdem_tile_id = sa.Column(sa.Integer, primary_key=True)
    resolution = sa.Column(
        sa.Numeric, comment="The approximate/nominal resolution of this tile in metres per pixel", nullable=False)
    z_precision = sa.Column(
        sa.Integer, comment="Approximate precision of the z/elevation value.  0 for CDEM to indicate 1 m increments.",
        nullable=False)
    filename = sa.Column(sa.TEXT, comment="An s3 filename reference. Do not include bucket name.", nullable=False)
    geom = sa.Column(geoalchemy2.types.Geometry(
        geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True))


def upgrade():
    connection = op.get_bind()
    SessionMaker = sessionmaker(bind=connection.engine)
    session = SessionMaker(bind=connection)

    dirname = os.path.dirname(__file__)
    dem_footprint = dirname + '/shapefiles/caribou_extent.shp'

    with fiona.open(dem_footprint, 'r', crs="EPSG:4326") as shp:
        for feat in shp:
            tile = StreamBurnedCDEMTile(
                filename="Burned_Caribou_4326.tif",
                z_precision=0,
                resolution=25,
                geom='SRID=4326;' + MultiPolygon([shape(feat['geometry'])]).wkt
            )
            session.add(tile)
        session.commit()
    # ### end Alembic commands ###


def downgrade():
    pass
