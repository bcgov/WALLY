"""add watershed function

Revision ID: f2b445f6650c
Revises: 5dd642b61ff0
Create Date: 2020-02-08 00:06:44.544948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f2b445f6650c'
down_revision = '5dd642b61ff0'
branch_labels = None
depends_on = None


def upgrade():

    with_intarray = """


        with starting_ws as (
            select  loc_code_arr - 0 as arr,
            left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code,
            "GEOMETRY" as geom
            from    freshwater_atlas_watersheds
            where   "WATERSHED_FEATURE_ID" = 4459183
        ),
        full_ws as (
            SELECT
                "GEOMETRY" as geom,
                "FEATURE_AREA_SQM" as area,
                "WATERSHED_FEATURE_ID",
                loc_code_arr
            FROM    freshwater_atlas_watersheds, starting_ws s
            WHERE   "FWA_WATERSHED_CODE" like s.fwa_local_code
        )
        select ws.geom, ws.area
        from full_ws ws, starting_ws s
        where
            ws.loc_code_arr[icount(s.arr) - 1] >
            s.arr[icount(s.arr) - 1]
        OR "WATERSHED_FEATURE_ID" = include




            AND 
        loc_code_arr[icount(loc_code_tr.arr - 0) - 1] >=
        loc_code_tr.arr[icount(loc_code_tr.arr - 0) - 1]
    

        AND 
        loc_code_arr[icount(loc_code_tr.arr - 0) - 1] >=
        loc_code_tr.arr[icount(loc_code_tr.arr - 0) - 1]
        OR "WATERSHED_FEATURE_ID" = include



, starting_ws s
        where
            ws.loc_code_arr[icount(s.arr) - 1] >
            s.arr[icount(s.arr) - 1]
        OR "WATERSHED_FEATURE_ID" = include


    alter table freshwater_atlas_watersheds add column loc_code_arr integer[];
    update freshwater_atlas_watersheds set loc_code_arr = string_to_array("LOCAL_WATERSHED_CODE", '-')::int[];
    create index freshwater_atlas_watersheds_loc_code_arr_idx on freshwater_atlas_watersheds using gin (loc_code_arr gin__int_ops);

    CREATE OR REPLACE
    FUNCTION public.calculate_upstream_catchment(upstream_from INTEGER default NULL)
    RETURNS TABLE(
        geom Geometry(Polygon, 4326),
        area float
    )
    AS $$
        with starting_ws as (
            select  loc_code_arr - 0 as arr,
            left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code,
            "GEOMETRY" as geom
            from    freshwater_atlas_watersheds
            where   "WATERSHED_FEATURE_ID" = upstream_from
        )
        SELECT
            "GEOMETRY" as geom,
            "FEATURE_AREA_SQM" as area

        FROM    freshwater_atlas_watersheds, starting_ws s
        WHERE   "FWA_WATERSHED_CODE" like s.fwa_local_code

    $$
    LANGUAGE 'sql'
    STABLE
    ;

    CREATE OR REPLACE
    FUNCTION public.calculate_upstream_catchment_starting_upstream(upstream_from INTEGER default NULL, include INTEGER default NULL)
    RETURNS TABLE(
        geom Geometry(Polygon, 4326),
        area float
    )
    AS $$
        with starting_ws as (
            select  loc_code_arr - 0 as arr,
            left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code,
            "GEOMETRY" as geom
            from    freshwater_atlas_watersheds
            where   "WATERSHED_FEATURE_ID" = upstream_from
        )
        SELECT
            "GEOMETRY" as geom,
            "FEATURE_AREA_SQM" as area

        FROM    freshwater_atlas_watersheds, starting_ws s
        WHERE   "FWA_WATERSHED_CODE" like s.fwa_local_code


    $$
    LANGUAGE 'sql'
    STABLE
    ;

    
    
    """

    # note on the WHERE clause in the following query:
    # the comparison between split_part functions is important.
    # to start at the first stream downstream from the source polygon,
    # use >=.  To start at the first stream upstream from the source polygon,
    # use >.  Starting at the first stream downstream will include that stream's
    # catchment area, but starting at the first stream upstream may not work when
    # close to the "headwaters" of a river. Both versions are included below.
    op.execute("""
        CREATE OR REPLACE
        FUNCTION public.calculate_upstream_catchment(upstream_from INTEGER default NULL)
        RETURNS TABLE(
            geom Geometry(Polygon, 4326),
            area float
        )
        AS $$
            SELECT
                "GEOMETRY" as geom,
                "FEATURE_AREA_SQM" as area
            FROM    freshwater_atlas_watersheds
            WHERE   "FWA_WATERSHED_CODE" ilike (
                SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
                FROM    freshwater_atlas_watersheds fwa2
                WHERE   "WATERSHED_FEATURE_ID" = upstream_from
            )
            AND split_part("LOCAL_WATERSHED_CODE", '-', (
                    SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                    FROM freshwater_atlas_watersheds
                    WHERE   "WATERSHED_FEATURE_ID" = upstream_from
                )::int
            )::int >= split_part((
                    SELECT "LOCAL_WATERSHED_CODE"
                    FROM freshwater_atlas_watersheds
                    WHERE "WATERSHED_FEATURE_ID" = upstream_from
                ), '-', (
                    SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                    FROM freshwater_atlas_watersheds
                    WHERE "WATERSHED_FEATURE_ID" = upstream_from
                )::int
            )::int
        $$
        LANGUAGE 'sql'
        STABLE
        ;

        CREATE OR REPLACE
        FUNCTION public.calculate_upstream_catchment_starting_upstream(upstream_from INTEGER default NULL, include INTEGER default NULL)
        RETURNS TABLE(
            geom Geometry(Polygon, 4326),
            area float
        )
        AS $$
            SELECT
                "GEOMETRY" as geom,
                "FEATURE_AREA_SQM" as area
            FROM    freshwater_atlas_watersheds
            WHERE   "FWA_WATERSHED_CODE" ilike (
                SELECT  left(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), strpos(regexp_replace("FWA_WATERSHED_CODE", '000000', '%'), '%')) as fwa_local_code
                FROM    freshwater_atlas_watersheds fwa2
                WHERE   "WATERSHED_FEATURE_ID" = upstream_from
            )
            AND split_part("LOCAL_WATERSHED_CODE", '-', (
                    SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                    FROM freshwater_atlas_watersheds
                    WHERE   "WATERSHED_FEATURE_ID" = upstream_from
                )::int
            )::int > split_part((
                    SELECT "LOCAL_WATERSHED_CODE"
                    FROM freshwater_atlas_watersheds
                    WHERE "WATERSHED_FEATURE_ID" = upstream_from
                ), '-', (
                    SELECT FLOOR(((strpos(regexp_replace("LOCAL_WATERSHED_CODE", '000000', '%'), '%')) - 4) / 7) + 1
                    FROM freshwater_atlas_watersheds
                    WHERE "WATERSHED_FEATURE_ID" = upstream_from
                )::int
            )::int
            OR "WATERSHED_FEATURE_ID" = include
        $$
        LANGUAGE 'sql'
        STABLE
        ;


    """)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    return
