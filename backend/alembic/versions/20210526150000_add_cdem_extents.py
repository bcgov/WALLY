"""add cdem extents

Revision ID: bb906a00fbe7
Revises: 702efdc8f3fa
Create Date: 2021-05-26 15:00:00.907115

"""
from alembic import op
import fiona
import os
import geoalchemy2
import sqlalchemy as sa
from shapely.geometry import shape, MultiPolygon
from sqlalchemy.dialects import postgresql
from api.db.base_class import BaseTable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# revision identifiers, used by Alembic.
revision = 'bb906a00fbe7'
down_revision = '702efdc8f3fa'
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
    __table_args__ = {'schema': 'dem'}

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
    op.create_table('stream_burned_cdem_tile',
                    sa.Column('stream_burned_cdem_tile_id', sa.INTEGER(), primary_key=True),
                    sa.Column('resolution', sa.NUMERIC(), autoincrement=False, nullable=False),
                    sa.Column('z_precision', sa.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('filename', sa.TEXT(), autoincrement=False, nullable=False),
                    sa.Column('geom', geoalchemy2.types.Geometry(
                        geometry_type='MULTIPOLYGON', srid=4326, spatial_index=True)),
                    schema='dem'
                    )

    connection = op.get_bind()
    SessionMaker = sessionmaker(bind=connection.engine)
    session = SessionMaker(bind=connection)

    dirname = os.path.dirname(__file__)
    dem_footprints = dirname + '/shapefiles/cdem_footprints.shp'

    with fiona.open(dem_footprints, 'r', crs="EPSG:4326") as shp:
        for feat in shp:
            tile = StreamBurnedCDEMTile(
                filename=feat['properties']['filename'],
                z_precision=feat['properties']['z_precisio'],
                resolution=feat['properties']['resolution'],
                geom='SRID=4326;' + MultiPolygon([shape(feat['geometry'])]).wkt
            )
            session.add(tile)
        session.commit()


def downgrade():
    op.drop_table('stream_burned_cdem_tile', schema='dem')
    return
