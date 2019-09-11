"""added habitat layer

Revision ID: 516ece576828
Revises: ce8988852432
Create Date: 2019-09-10 20:16:58.664976

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA

# revision identifiers, used by Alembic.
revision = '516ece576828'
down_revision = 'ce8988852432'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'critical_habitat_species_at_risk',

        sa.Column('CRITICAL_HABITAT_ID', sa.Integer, primary_key=True,
                  comment='CRITICAL_HABITAT_ID: is a system generated '
                          'unique identification number. This is the '
                          'primary key of this table. e.g., 1'),
        sa.Column('COSEWIC_SPECIES_ID', sa.String,
                  comment='COSEWIC_SPECIES_ID is a unique identification number assigned to '
                          'the species or taxa (including, if applicable, sub species and'
                          ' population) assessed by the Committee on the Status of Endangered '
                          'Wildlife in Canada (COSEWIC) and currently listed on SARA '
                          'Schedule 1; e.g., 1086.'),
        sa.Column('SCIENTIFIC_NAME', sa.String, comment='SCIENTIFIC_NAME is the standard scientific name for the'
                                                        ' SARA-listed species or taxa, and can include subspecies;'
                                                        ' e.g., Oreoscoptes montanus.'),
        sa.Column('COMMON_NAME_ENGLISH', sa.String, comment='COMMON_NAME_ENGLISH is the English name of the species'
                                                            ' or taxa listed on SARA Schedule 1; e.g., Sage Thrasher.'),
        sa.Column('COMMON_NAME_FRENCH', sa.String,
                  comment='COMMON_NAME_FRENCH is the French name of the species or taxa'
                          ' listed on SARA Schedule 1; e.g., Moqueur des armoises.'),
        sa.Column('COSEWIC_POPULATION', sa.String, comment='COSEWIC_POPULATION is the population name of the species'
                                                           ' or taxa assessed by the Committee on '
                                                           'the Status of Endangered'
                                                           ' Wildlife in Canada (COSEWIC) and currently listed on SARA'
                                                           ' Schedule 1; e.g., Southern Mountain population.'),
        sa.Column('CRITICAL_HABITAT_STATUS', sa.String, comment='CRITICAL_HABITAT_STATUS is the stage of development'
                                                                ' of the critical habitat polygon; '
                                                                'e.g., Final or Candidate'),
        sa.Column('CRITICAL_HABITAT_REGION', sa.String, comment='CRITICAL_HABITAT_REGION is a regional identifier '
                                                                'optionally used to group critical habitat polygons;'
                                                                ' e.g. "Southeastern BC".'),
        sa.Column('CRITICAL_HABITAT_SITE_ID', sa.String,
                  comment='CRITICAL_HABITAT_SITE_ID is the alphanumeric code of a '
                          'critical habitat site as defined in the federal '
                          'recovery document; e.g., 937_5.'),
        sa.Column('CRITICAL_HABITAT_SITE_NAME', sa.String,
                  comment='CRITICAL_HABITAT_SITE_NAME is the name of a critical '
                          'habitat site as defined in the federal recovery document; '
                          'e.g., Kilpoola.'),
        sa.Column('CRITICAL_HABITAT_DETAIL', sa.String,
                  comment='CRITICAL_HABITAT_DETAIL is the level of detail of critical'
                          ' habitat polygon; e.g., Detailed polygon or Grid square. '
                          'Grid squares are used when detailed polygons contain '
                          'sensitive information that cannot be released.'),
        sa.Column('CRITICAL_HABITAT_VARIANT', sa.String, comment='CRITICAL_HABITAT_VARIANT is the sub-type of critical'
                                                                 ' habitat, if applicable; e.g. Regeneration.'),
        sa.Column('CRITICAL_HABITAT_APPROACH', sa.String, comment='CRITICAL_HABITAT_APPROACH is the scale at which the '
                                                                  'polygons were defined and refers'
                                                                  ' to processes within '
                                                                  'the Critical Habitat Toolbox policy; e.g.,'
                                                                  ' Landscape, Area or Site.'),
        sa.Column('CRITICAL_HABITAT_METHOD', sa.String, comment='CRITICAL_HABITAT_METHOD is a broad description of how '
                                                                'the critical habitat was identified and'
                                                                ' refers to processes '
                                                                'within the Critical Habitat Toolbox policy; e.g.,'
                                                                ' Critical Function Zone.'),
        sa.Column('AREA_HECTARES', sa.Float, comment='AREA_HECTARES is the area calculated in hectares at source data'
                                                     ' which is in Lambert Conic Conformal. E.g., 14430833.7926'),
        sa.Column('LAND_TENURE', sa.String, comment='LAND_TENURE is the status of federal crown ownership of the land;'
                                                    ' e.g., Federal or Non-federal.'),
        sa.Column('CRITICAL_HABITAT_COMMENTS', sa.String,
                  comment='CRITICAL_HABITAT_COMMENTS are notes about the critical'
                          ' habitat or specific polygon; e.g., Polygons were '
                          'identified as part of a multispecies recovery plan.'),
        sa.Column('CRITICAL_HABITAT_DATE_EDITED', sa.DateTime, comment='CRITICAL_HABITAT_DATE_EDITED is the date that '
                                                                       'the polygon was last edited; e.g., 8/21/2014.'),
        sa.Column('PROVINCE_TERRITORY', sa.String, comment='PROVINCE_TERRITORY is the province or territory in which'
                                                           ' the critical habitat occurs; e.g., British Columbia.'),
        sa.Column('FEDERAL_DEPARTMENT_NAME', sa.String, comment='FEDERAL_DEPARTMENT_NAME is the Federal department or '
                                                                'agency that published the recovery strategy or action'
                                                                ' plan in which the critical habitat is identified,'
                                                                ' and maintains the data; e.g., '
                                                                'Canadian Wildlife Service, '
                                                                '‘Parks Canada Agency’.'),
        sa.Column('UTM_ZONE', sa.Float, comment='UTM_ZONE is a segment of the Earths surface 6 degrees of longitude '
                                                'in width. The zones are numbered eastward starting at the meridian '
                                                '180 degrees from the prime meridian at Greenwich. There are five zones'
                                                ' numbered 7 through 11 that cover British Columbia,'
                                                ' e.g., Zone 10 with '
                                                'a central meridian at -123 degrees.'),
        sa.Column('UTM_EASTING', sa.Float, comment='UTM EASTING is the distance in meters of the polygon centroid '
                                                   'eastward to or from the central meridian of a UTM zone with a '
                                                   'false easting of 500000 meters. E.g., 532538'),
        sa.Column('UTM_NORTHING', sa.Float, comment='UTM NORTHING is the distance in meters of the polygon '
                                                    'centroidnorthward from the equator. e.g., 5747966'),
        sa.Column('LATITUDE', sa.Float, comment='LATITUDE is the geographic coordinate, in decimal degrees '
                                                '(dd.dddddd), of the location of the feature as measured from '
                                                'the equator, e.g., 55.323653'),
        sa.Column('LONGITUDE', sa.Float, comment='LONGITUDE is the geographic coordinate, in decimal degrees'
                                                 ' (ddd.dddddd), of the location of the feature as measured from '
                                                 'the prime meridian, e.g., -123.093544'),
        sa.Column('SHAPE', Geometry, comment='SHAPE is the sa.column used to reference the spatial coordinates'
                                             ' defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, comment='OBJECTID is a sa.column required by spatial layers that interact'
                                                  ' with ESRI ArcSDE. It is populated with unique '
                                                  'values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE ANNO CAD DATA is a binary sa.column used by spatial tools '
                                                     'to store annotation, curve features and CAD data when using the '
                                                     'SDO_GEOMETRY storage data type.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment=''),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='')
    )


def downgrade():
    pass
