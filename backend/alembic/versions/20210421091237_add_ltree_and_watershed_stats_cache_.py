"""add LTREE and watershed stats/cache tables

Revision ID: 702efdc8f3fa
Revises: a691dfe51337
Create Date: 2021-04-21 09:12:37.345503

"""
from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import LtreeType
from sqlalchemy.orm import relationship


# revision identifiers, used by Alembic.
revision = '702efdc8f3fa'
down_revision = 'a691dfe51337'
branch_labels = None
depends_on = None


def upgrade():

    # takes a while.
    op.execute(
        """
        select updategeometrysrid('freshwater_atlas_watersheds', 'GEOMETRY', 4326)
        """
    )

    # this group of operations takes a LONG while!
    op.add_column('freshwater_atlas_watersheds', sa.Column('wscode_ltree', LtreeType, sa.Computed(
        "(replace(replace((\"FWA_WATERSHED_CODE\")::text, '-000000'::text, ''::text), '-'::text, '.'::text))::ltree", persisted=True), autoincrement=False, nullable=True), schema='public')
    op.add_column('freshwater_atlas_watersheds', sa.Column('localcode_ltree', LtreeType, sa.Computed(
        "(replace(replace((\"LOCAL_WATERSHED_CODE\")::text, '-000000'::text, ''::text), '-'::text, '.'::text))::ltree", persisted=True), autoincrement=False, nullable=True), schema='public')
    op.add_column('freshwater_atlas_watersheds', sa.Column('fme_feature_type', sa.VARCHAR(),
                                                           autoincrement=False, nullable=True))
    op.create_index('freshwater_atlas_watersheds_localcode_ltree_idx1', 'freshwater_atlas_watersheds', [
                    'localcode_ltree'], unique=False, schema='public')
    op.create_index('freshwater_atlas_watersheds_localcode_ltree_idx', 'freshwater_atlas_watersheds', [
                    'localcode_ltree'], unique=False, schema='public')
    op.create_index('freshwater_atlas_watersheds_wscode_ltree_idx', 'freshwater_atlas_watersheds', [
                    'wscode_ltree'], unique=False, schema='public')
    op.create_index('freshwater_atlas_watersheds_wscode_ltree_gist_idx', 'freshwater_atlas_watersheds', [
                    'wscode_ltree'], unique=False, schema='public')

    # approx borders.  From https://github.com/smnorris/fwapg
    op.create_table('fwa_approx_borders',
                    sa.Column('approx_border_id',
                              sa.INTEGER(), primary_key=True),
                    sa.Column('border', sa.TEXT(),
                              autoincrement=False, nullable=True),
                    sa.Column('geom', geoalchemy2.types.Geometry(
                        geometry_type='LINESTRING', srid=3005, spatial_index=True)),
                    )

    op.execute("""
            INSERT INTO fwa_approx_borders
        (border, geom)
        SELECT
        'USA_49' as border,
            ST_Transform(
            ST_MakeLine(
                ST_SetSRID(ST_MakePoint(x, y), 4326)
            ),
            3005)
        AS geom
        FROM (SELECT
                generate_series(-123.3, -114.06, .01) AS x,
                49.00025 AS y) AS segments

        UNION ALL

        SELECT
        'YTNWT_60' as border,
            ST_Transform(
            ST_MakeLine(
                ST_SetSRID(ST_MakePoint(x, y), 4326)
            ),
            3005)
        AS geom
        FROM (SELECT
                generate_series(-139.05, -120.00, .01) AS x,
                59.9995 AS y) AS segments

        UNION ALL

        SELECT
        'AB_120' as border,
            ST_Transform(
            ST_MakeLine(
                ST_SetSRID(ST_MakePoint(x, y), 4326)
            ),
            3005)
        AS geom
        FROM (SELECT
                -120.0005 AS x,
                generate_series(60, 53.79914, -.01) AS y) AS segments;
    """)

    # hydrosheds data from hydrosheds.org (WWF)
    op.execute("create schema hydrosheds")
    op.create_table('hybas_lev12_v1c',
                    sa.Column('hybas_id', sa.BIGINT(),
                              autoincrement=False, nullable=False),
                    sa.Column('next_down', sa.NUMERIC(precision=11,
                              scale=0), autoincrement=False, nullable=True),
                    sa.Column('next_sink', sa.NUMERIC(precision=11, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('main_bas', sa.NUMERIC(precision=11, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('dist_sink', sa.NUMERIC(precision=10, scale=1),
                              autoincrement=False, nullable=True),
                    sa.Column('dist_main', sa.NUMERIC(precision=10, scale=1),
                              autoincrement=False, nullable=True),
                    sa.Column('sub_area', sa.NUMERIC(precision=10, scale=1),
                              autoincrement=False, nullable=True),
                    sa.Column('up_area', sa.NUMERIC(precision=10, scale=1),
                              autoincrement=False, nullable=True),
                    sa.Column('pfaf_id', sa.NUMERIC(precision=13, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('endo', sa.NUMERIC(precision=6, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('coast', sa.NUMERIC(precision=6, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('order', sa.NUMERIC(precision=6, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('sort', sa.NUMERIC(precision=11, scale=0),
                              autoincrement=False, nullable=True),
                    sa.Column('geom', geoalchemy2.types.Geometry(
                        geometry_type='MULTIPOLYGON', srid=3005, spatial_index=True)),
                    sa.PrimaryKeyConstraint(
                        'hybas_id', name='hybas_lev12_v1c_pkey'),
                    schema='hydrosheds'
                    )
    op.create_index('hybas_lev12_v1c_next_down_idx', 'hybas_lev12_v1c', [
                    'next_down'], unique=False, schema='hydrosheds')

    op.create_table('generated_watershed',

                    sa.Column('generated_watershed_id',
                              sa.Integer, primary_key=True),
                    sa.Column('wally_watershed_id', sa.String, comment='WALLY watershed identifier used to recreate watersheds. '
                              'The format is the upstream delineation method followed by '
                              'the POI encoded as base64.'),
                    sa.Column('create_date',
                              sa.DateTime, comment='Date and time (UTC) when the physical record was created in the database.', nullable=False),
                    sa.Column('create_user', sa.String,
                              comment='User who generated this watershed', nullable=False),
                    sa.Column('update_user', sa.String, nullable=False),
                    sa.Column('update_date', sa.DateTime, nullable=False),
                    sa.Column('processing_time',
                              sa.Numeric, comment='How long it took to calculate this watershed.'),
                    sa.Column('upstream_method',
                              sa.String, comment='The method used to calculate this watershed e.g. FWA+UPSTREAM, DEM+FWA etc.'),
                    sa.Column('is_near_border', sa.Boolean, comment='Indicates whether this watershed was determined to be near a border. '
                              'This affects how it was generated and refined.'),
                    sa.Column('click_point', geoalchemy2.types.Geometry(
                        geometry_type='POINT', srid=4326), comment='The coordinates of the original click point.'),
                    sa.Column('snapped_point', geoalchemy2.types.Geometry(
                        geometry_type='POINT', srid=4326), comment='The coordinates used for delineation after snapping to a Flow Accumulation raster stream line.'),
                    sa.Column('area_sqm', sa.Numeric,
                              comment='Area in square metres')
                    )

    op.create_table('watershed_polygon_cache',
                    sa.Column('generated_watershed_id', sa.Integer, sa.ForeignKey('generated_watershed.generated_watershed_id'),
                              comment='The GeneratedWatershed record this cached polygon is associated with.', primary_key=True),
                    sa.Column('geom', geoalchemy2.types.Geometry(
                        geometry_type='MULTIPOLYGON', srid=4326), nullable=False),
                    sa.Column('last_accessed_date', sa.DateTime,
                              comment='The date this cached record was last accessed.', nullable=False
                              )
                    )

    op.execute("""
    CREATE OR REPLACE FUNCTION prune_watershed_polygon_cache() RETURNS trigger
        LANGUAGE plpgsql
        AS $$
    BEGIN
    DELETE FROM watershed_polygon_cache WHERE last_accessed_date < NOW() - INTERVAL '1 days';
    RETURN NULL;
    END;
    $$;

    CREATE TRIGGER trigger_prune_watershed_polygon_cache
    AFTER INSERT ON watershed_polygon_cache
    EXECUTE PROCEDURE prune_watershed_polygon_cache();
    """)


def downgrade():
    pass

    # ### end Alembic commands ###
