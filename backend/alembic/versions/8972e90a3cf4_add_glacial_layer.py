"""add glacial layer

Revision ID: 8972e90a3cf4
Revises: db6313a85cf5
Create Date: 2019-12-30 12:45:47.276750

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA

# revision identifiers, used by Alembic.
revision = '8972e90a3cf4'
down_revision = 'db6313a85cf5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'freshwater_atlas_glaciers',
                          
        sa.Column('WATERBODY_POLY_ID', sa.Integer, primary_key=True, autoincrement=False, comment='The WATERBODY POLY ID is the unique key for the waterbody polygon spatial layer. It is not applied to the warehouse model only, i.e., it originates with the source FWA system.'),
        sa.Column('WATERSHED_GROUP_ID', sa.Integer, comment='An automatically generate id that uniquely identifies the watershed group feature.'),
        sa.Column('WATERBODY_TYPE', sa.String, comment='The type of waterbody. Possible values include: \'L\' (lake), \'R\' (double lined river), \'W\' (wetland), \'X\' (manmade river or lake), or \'G\' (glacier or icefield).'),
        sa.Column('WATERBODY_KEY', sa.Integer, comment='A unique identifier associated with waterbodies in order to group polygons that make up a single waterbody.'),
        sa.Column('AREA_HA', sa.Float, comment='Area of polygon (hectares).'),
        sa.Column('GNIS_ID_1', sa.Integer, comment='A BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable. In a grouped system the feature id of the BCGNIS group is provided here and any subsequent names provided in gnis_id2 and gnis_id3. Note: For Vancouver Island, Graham Island, and Moresby Island the names are not attached to the label points.'),
        sa.Column('GNIS_NAME_1', sa.String, comment='The name of the first BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).'),
        sa.Column('GNIS_ID_2', sa.Integer, comment='A second BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable.'),
        sa.Column('GNIS_NAME_2', sa.String, comment='The name of the second BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).'),
        sa.Column('GNIS_ID_3', sa.Integer, comment='A third BCGNIS (BC Geographical Names Information System) feature id attached to a waterbody or island, if applicable.'),
        sa.Column('GNIS_NAME_3', sa.String, comment='The name of the third BCGNIS (BC Geographical Names Information System) feature id (an English name was used where available, otherwise another language was selected).'),
        sa.Column('BLUE_LINE_KEY', sa.Integer, comment='The blue line key of the controlling route through the waterbody.'),
        sa.Column('WATERSHED_KEY', sa.Integer, comment='The watershed key of the controlling rout through the waterbody.'),
        sa.Column('FWA_WATERSHED_CODE', sa.String, comment='The watershed code of the controlling route through the waterbody.'),
        sa.Column('LOCAL_WATERSHED_CODE', sa.String, comment='The local watershed code associated with the waterbody.'),
        sa.Column('WATERSHED_GROUP_CODE', sa.String, comment='The watershed group codeof the watershed the feature is contained within.'),
        sa.Column('LEFT_RIGHT_TRIBUTARY', sa.String, comment='A value attributed via the watershed code to all waterbodies indicating on what side of the watershed they drain into.'),
        sa.Column('WATERBODY_KEY_50K', sa.Integer, comment='The \'best\' matched waterbody from the 1:50K Watershed Atlas. In cases where there are multiple matches to features in the 1:50K watershed atlas the match with the greatest overlapping area was used.'),
        sa.Column('WATERSHED_GROUP_CODE_50K', sa.String, comment='The group code from the 1:50K Watershed Atlas associated with the waterbody key 50k.'),
        sa.Column('WATERBODY_KEY_GROUP_CODE_50K', sa.String, comment='The waterbody key 50K with the group code 50K concatenated.'),
        sa.Column('WATERSHED_CODE_50K', sa.String, comment='The 1:50K Watershed Atlas watershed code associated with the waterbody key 50K.'),
        sa.Column('FEATURE_CODE', sa.String, comment='FEATURE CODE contains a value based on the Canadian Council of Surveys and Mapping\'s (CCSM) system for classification of geographic features.'),
        sa.Column('OBJECTID', sa.Float, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools'
                                'to store annotation, curve features and CAD data when using'
                                'the SDO_GEOMETRY storage data type.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a geometry in meters'),
        sa.Column('GEOMETRY', Geometry, comment='')
    )


def downgrade():
    pass
