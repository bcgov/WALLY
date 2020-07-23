"""Added wms db layer tables

Revision ID: fc2537bad3fa
Revises: ce8988852432
Create Date: 2019-09-10 10:54:51.047665

"""
from alembic import op
from geoalchemy2 import Geometry
import sqlalchemy as sa
import logging
from sqlalchemy.dialects.postgresql import BYTEA

logger = logging.getLogger("alembic")

# revision identifiers, used by Alembic.
revision = 'fc2537bad3fa'
down_revision = 'ce8988852432'
branch_labels = None
depends_on = None


def upgrade():
    logger.info("creating wms data tables")

    op.create_table(
        'automated_snow_weather_station_locations',

        sa.Column('SNOW_ASWS_STN_ID', sa.Integer, primary_key=True,
                  comment='SNOW_ASWS_STN_ID is a system generated unique '
                          'identification number.'),
        sa.Column('LOCATION_ID', sa.String, comment='LOCATION_ID is the unique identifier of the snow weather station, '
                                                    'e.g. 1C41P.'),
        sa.Column('LOCATION_NAME', sa.String,
                  comment='LOCATION_NAME is the name of the snow weather station, e.g. Yanks Peak.'),
        sa.Column('ELEVATION', sa.Float,
                  comment='ELEVATION the elevation of the snow weather station in metres, e.g. 1670.'),
        sa.Column('STATUS', sa.String,
                  comment='STATUS is the operational status of the snow station, e.g. Active, Inactive.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                          'location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='	LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), of '
                          'the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates defining '
                          'the feature.'),
        sa.Column('OBJECTID', sa.Integer, comment='OBJECTID is a column required by spatial layers that '
                                                  'interact with ESRI ArcSDE. It is populated with unique '
                                                  'values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'bc_major_watersheds',

        sa.Column('AREA', sa.Float, comment=''),
        sa.Column('PERIMETER', sa.Float, comment=''),
        sa.Column('MAJOR_WATERSHED_CODE', sa.String, comment=''),
        sa.Column('MAJOR_WATERSHED_SYSTEM', sa.String, comment=''),
        sa.Column('FCODE', sa.String, comment=''),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is the column used to reference the spatial coordinates '
                                                'defining the feature.'),
        sa.Column('OBJECTID', sa.String, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float,
                  comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional '
                          'polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a '
                          'geometry in meters'),
    )

    op.create_table(
        'bc_wildfire_active_weather_stations',

        sa.Column('WEATHER_STATIONS_ID', sa.Integer, primary_key=True,
                  comment='WEATHER STATION ID is a system generated '
                          'unique identifier number.'),
        sa.Column('STATION_CODE', sa.Integer,
                  comment='STATION_CODE is the internal unique number assigned to this weather '
                          'station, e.g., 67 .'),
        sa.Column('STATION_NAME', sa.String,
                  comment='STATION_NAME is a derived name of a weather station based on geographic '
                          'significance, e.g. HAIG CAMP.'),
        sa.Column('STATION_ACRONYM', sa.String,
                  comment='STATION_ACRONYM is a 4 character airport code for the closest airport to '
                          'the station. This is used for weather forecasting software. This is not '
                          'populated for all weather stations. The leading "C" may be dropped from '
                          'most of the values, e.g.,CYYJ, YVR.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), of the '
                          'location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                          'of the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('ELEVATION', sa.Float,
                  comment='ELEVATION is the elevation of the weather station in metres above sea level as '
                          'derived from the TRIM DEM.'),
        sa.Column('INSTALL_DATE', sa.DateTime, comment='INSTALL_DATE is the date when the weather station was '
                                                       'physically installed.'),
        sa.Column('SHAPE', Geometry, comment='SHAPE is the column used to reference the spatial coordinates '
                                             'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, comment='OBJECTID is a column required by spatial layers that interact with '
                                                  'ESRI ArcSDE. It is populated with '
                                                  'unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'cadastral',

        sa.Column('PARCEL_FABRIC_POLY_ID', sa.Integer, primary_key=True,
                  comment='PARCEL_FABRIC_POLY_ID is a system generated '
                          'unique identification number.'),
        sa.Column('PARCEL_NAME', sa.String,
                  comment='PARCEL_NAME is the same as the PID, if there is one. If there is a '
                          'PIN but no PID, then PARCEL_NAME is the PIN. If there is no PID nor '
                          'PIN, then PARCEL_NAME is the parcel class value, e.g., COMMON OWNERSHIP, '
                          'BUILDING STRATA, AIR SPACE, ROAD, PARK.'),
        sa.Column('PLAN_NUMBER', sa.String,
                  comment='PLAN_NUMBER is the Land Act, Land Title Act, or Strata Property Act Plan '
                          'Number for the land survey plan that corresponds to this parcel, e.g., '
                          'VIP1632, NO_PLAN.'),
        sa.Column('PIN', sa.Integer, comment='PIN is the Crown Land Registry Parcel Identifier, if applicable.'),
        sa.Column('PID', sa.String,
                  comment='PID is the Land Title Register parcel identifier, an up-to nine-digit text number '
                          'with leading zeros that uniquely identifies a parcel in the land title register '
                          'of in British Columbia. The registrar assigns PID numbers to parcels for which a '
                          'title is being entered as a registered title. The Land Title Act refers to the '
                          'PID as the permanent parcel identifier.'),
        sa.Column('PID_NUMBER', sa.Integer,
                  comment='PID_NUMBER is the Land Title Register parcel identifier, an up-to nine-digit '
                          'number without leading zeros that uniquely identifies a parcel in the land '
                          'title register of in British Columbia. The registrar assigns PID numbers '
                          'to parcels for which a title is being entered as a registered title. The '
                          'Land Title Act refers to the PID as the permanent parcel identifier.'),
        sa.Column('PARCEL_STATUS', sa.String,
                  comment='PARCEL_STATUS is the status of the parcel, according to the Land Title '
                          'Register or Crown Land Registry, as appropriate, '
                          'i.e., ACTIVE, CANCELLED, INACTIVE, PENDING.'),
        sa.Column('PARCEL_CLASS', sa.String,
                  comment='PARCEL_CLASS is the Parcel classification for maintenance, mapping, '
                          'publishing and analysis, i.e., PRIMARY, SUBDIVISION, PART OF PRIMARY, '
                          'BUILDING STRATA, BARE LAND STRATA, AIR SPACE, ROAD, HIGHWAY, PARK, '
                          'INTEREST, COMMON OWNERSHIP, ABSOLUTE FEE BOOK, CROWN SUBDIVISION, '
                          'RETURN TO CROWN.'),
        sa.Column('OWNER_TYPE', sa.String, comment='OWNER_TYPE is the general ownership category, e.g., PRIVATE, CROWN '
                                                   'PROVINCIAL, MUNICIPAL. For more information, '
                                                   'see https://help.ltsa.ca/parcelmap-bc/owner-types-parcelmap-bc'),
        sa.Column('PARCEL_START_DATE', sa.DateTime,
                  comment='PARCEL_START_DATE is the date of the legal event that created '
                          'the parcel, i.e., the date the plan was filed.'),
        sa.Column('MUNICIPALITY', sa.String,
                  comment='MUNICIPALITY is the municipal area within which the parcel is located. '
                          'The value is either RURAL (for parcels in unincorporated regions) or '
                          'the name of a BC municipality.'),
        sa.Column('REGIONAL_DISTRICT', sa.String,
                  comment='REGIONAL_DISTRICT is the name of the regional district in which '
                          'the parcel is located, e.g., CAPITAL REGIONAL DISTRICT.'),
        sa.Column('WHEN_UPDATED', sa.DateTime,
                  comment='WHEN_UPDATED is the date and time the record was last modified.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float,
                  comment='FEATURE_AREA_SQM is the system calculated area of a two-dimensional '
                          'polygon in square meters.'),
        sa.Column('FEATURE_LENGTH_M', sa.Float,
                  comment='FEATURE_LENGTH_M is the system calculated length or perimeter of a '
                          'geometry in meters.'),
        sa.Column('SHAPE', Geometry,
                  comment='SHAPE is the column used to reference the spatial coordinates defining '
                          'the feature.'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a column required by spatial layers that interact with ESRI '
                          'ArcSDE. It is populated with unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA,
                  comment='	SE_ANNO_CAD_DATA is a binary column used by spatial tools to store '
                          'annotation, curve features and CAD data when using the SDO_GEOMETRY '
                          'storage data type.'),
    )

    op.create_table(
        'ecocat_water_related_reports',

        sa.Column('REPORT_POINT_ID', sa.Integer, primary_key=True, comment=''),
        sa.Column('FEATURE_CODE', sa.String, comment=''),
        sa.Column('REPORT_ID', sa.Integer, comment=''),
        sa.Column('TITLE', sa.String, comment=''),
        sa.Column('SHORT_DESCRIPTION', sa.String, comment=''),
        sa.Column('AUTHOR', sa.String, comment=''),
        sa.Column('DATE_PUBLISHED', sa.DateTime, comment=''),
        sa.Column('WATERSHED_CODE', sa.String, comment=''),
        sa.Column('WATERBODY_IDENTIFIER', sa.String, comment=''),
        sa.Column('LONG_DESCRIPTION', sa.String, comment=''),
        sa.Column('REPORT_AUDIENCE', sa.String, comment=''),
        sa.Column('GEOMETRY', Geometry, comment=''),
        sa.Column('OBJECTID', sa.Integer, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
    )

    op.create_table(
        'freshwater_atlas_stream_directions',

        sa.Column('STREAM_DIRECTION_ID', sa.Integer, comment='STREAM DIRECTION ID is a surrogate key for the'
                                                             ' STREAM DIRECTION SP record. i.e. 1'),
        sa.Column('LINEAR_FEATURE_ID', sa.Integer,
                  comment='The LINEAR FEATURE ID is a unique numeric identifier used to '
                          'identify the STREAM NETWORKS SP spatial line that this '
                          'STREAM DIRECTION provides direction for. i.e 7209923'),
        sa.Column('DOWNSTREAM_DIRECTION', sa.Float, comment='DOWNSTREAM DIRECTION is the direction in decimal degrees, '
                                                            'counterclockwise from east, where east is 0, north is '
                                                            '90, west is 180, and south is 270, e.g., 179.227053, '
                                                            'which indicates almost due west.'),
        sa.Column('FEATURE_CODE', sa.String,
                  comment='FEATURE CODE contains a value based on the Canadian Council of Surveys'
                          ' and Mappings (CCSM) system for classification of geographic features.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is the column used to reference the spatial coordinates '
                                                'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools '
                                                     'to store annotation, curve features and CAD data when using '
                                                     'the SDO_GEOMETRY storage data type.'),
    )

    op.create_table(
        'freshwater_atlas_watersheds',

        sa.Column('WATERSHED_FEATURE_ID', sa.Integer, primary_key=True,
                  comment='A unique identifier for each watershed '
                          'in the layer.'),
        sa.Column('WATERSHED_GROUP_ID', sa.Integer, comment='An automatically generate id that uniquely identifies '
                                                            'the watershed group feature.'),
        sa.Column('WATERSHED_TYPE', sa.String, comment='The type of watershed. This has yet to be determined for FWA '
                                                       'version 2.0.0, but possible values may include: R - real '
                                                       'watershed, F - face unit watershed, '
                                                       'W - waterbody watershed, etc.'),
        sa.Column('GNIS_ID_1', sa.Integer,
                  comment='The first BCGNIS (BC Geographical Names Information System) feature id '
                          'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_1', sa.String, comment='The first BCGNIS (BC Geographical Names Information System) name '
                                                    'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_ID_2', sa.Integer,
                  comment='The second BCGNIS (BC Geographical Names Information System) feature '
                          'id associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_2', sa.String, comment='The second BCGNIS (BC Geographical Names Information System) name '
                                                    'associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_ID_3', sa.Integer,
                  comment='The third BCGNIS (BC Geographical Names Information System) feature '
                          'id associated with the watershed key of the principal watershed.'),
        sa.Column('GNIS_NAME_3', sa.String, comment='The third BCGNIS (BC Geographical Names Information System) name '
                                                    'associated with the watershed key of the principal watershed.'),
        sa.Column('WATERBODY_ID', sa.Integer, comment='If the principal watershed is made up of a lake or river, this '
                                                      'field will contain the waterbody id associated with that '
                                                      'waterbody, otherwise it will be null.'),
        sa.Column('WATERBODY_KEY', sa.Integer, comment='If the principal watershed is made up of a lake or river, this '
                                                       'field will contain the waterbody key associated with that '
                                                       'waterbody, otherwise it will be null.'),
        sa.Column('WATERSHED_KEY', sa.Integer, comment='The watershed key associated with the watershed polygon '
                                                       '(and watershed code).'),
        sa.Column('FWA_WATERSHED_CODE', sa.String, comment='The 143 character watershed code associated with '
                                                           'the watershed polygon.'),
        sa.Column('LOCAL_WATERSHED_CODE', sa.String, comment='A 143 character code similar to the fwa watershed code '
                                                             'that further subdivides remnant polygons to provide an '
                                                             'approximate location along the mainstem.'),
        sa.Column('WATERSHED_GROUP_CODE', sa.String, comment='The watershed group code associated with the polygon.'),
        sa.Column('LEFT_RIGHT_TRIBUTARY', sa.String,
                  comment='A value attributed via the watershed code to all watersheds '
                          'indicating on what side of the watershed they drain into.'),
        sa.Column('WATERSHED_ORDER', sa.Integer, comment='The maximum order of the watershed key associated with the '
                                                         'principal watershed polygon.'),
        sa.Column('WATERSHED_MAGNITUDE', sa.Integer,
                  comment='The maximum magnitude of the watershed key associated with '
                          'the principal watershed.'),
        sa.Column('LOCAL_WATERSHED_ORDER', sa.Integer, comment='The order associated with the local watershed code.'),
        sa.Column('LOCAL_WATERSHED_MAGNITUDE', sa.Integer,
                  comment='The magnitude associated with the local watershed code.'),
        sa.Column('AREA_HA', sa.Float, comment='Area of the watershed, in hectares.'),
        sa.Column('RIVER_AREA', sa.Float, comment='Area of double line rivers within the watershed, in hectares.'),
        sa.Column('LAKE_AREA', sa.Float, comment='Area of lakes within the watershed, in hectares.'),
        sa.Column('WETLAND_AREA', sa.Float, comment='Area of wetland features within the watershed, in hectares.'),
        sa.Column('MANMADE_AREA', sa.Float, comment='Area of manmade features within the watershed, in hectares.'),
        sa.Column('GLACIER_AREA', sa.Float, comment='Area of glacier features within the watershed, in hectares.'),
        sa.Column('AVERAGE_ELEVATION', sa.Float, comment='The average elevation of the watershed, in meters.'),
        sa.Column('AVERAGE_SLOPE', sa.Float, comment='The average slope of the watershed.'),
        sa.Column('ASPECT_NORTH', sa.Float, comment='The percentage of the watershed that has an aspect within '
                                                    '45 degrees of north, ie. an aspect between 315 and 45 degrees.'),
        sa.Column('ASPECT_SOUTH', sa.Float, comment='The percentage of the watershed that has an aspect within '
                                                    '45 degrees of south, ie. an aspect between 135 and 225 degrees.'),
        sa.Column('ASPECT_WEST', sa.Float, comment='The percentage of the watershed that has an aspect within '
                                                   '45 degrees of west, ie. an aspect between 225 and 315 degrees.'),
        sa.Column('ASPECT_EAST', sa.Float, comment='The percentage of the watershed that has an aspect within '
                                                   '45 degrees of east, ie. an aspect between 45 and 135 degrees.'),
        sa.Column('ASPECT_FLAT', sa.Float, comment='The percentage of the watershed with no discernable aspect, '
                                                   'ie. the flat land.'),
        sa.Column('FEATURE_CODE', sa.String, comment='FEATURE CODE contains a value based on the Canadian Council '
                                                     'of Surveys and Mappings (CCSM) system for classification of '
                                                     'geographic features.'),
        sa.Column('GEOMETRY', Geometry, comment=''),
        sa.Column('OBJECTID', sa.Integer, comment=''),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment='FEATURE_AREA_SQM is the system calculated area of a '
                                                        'two-dimensional polygon in square meters'),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                                                        'of a geometry in meters'),
    )

    op.create_table(
        'ground_water_aquifers',

        sa.Column('AQ_TAG', sa.String, primary_key=True,
                  comment='The AQ TAG is an alpha-numeric code assigned to the aquifer to '
                          'uniquely identify it.'),
        sa.Column('FCODE', sa.String,
                  comment='10	FCODE is a feature code is most importantly a means of linking a feature to '
                          'its name and definition. For example, the code GB15300120 on a digital geographic '
                          'feature links it to the name "Lake - Dry" with the definition '
                          '"A lake bed from which '
                          'all water has drained or evaporated." The feature code does NOT mark when it was '
                          'digitized, what dataset it belongs to, how accurate it is, what it should look '
                          'like when plotted, or who is responsible for updating it. It only says what it '
                          'represents in the real world. It also doesnt even matter how the lake is '
                          'represented. If it is a very small lake, it may be stored as a point feature. '
                          'If it is large enough to have a shape at the scale of data capture, it may be '
                          'stored as an outline, or a closed polygon. The same feature code still links it '
                          'to the same definition.'),
        sa.Column('PERIMETER', sa.Float,
                  comment='PERIMETER is the outside perimeter of the aquifer measured in metres.'),
        sa.Column('AQNAME', sa.String, comment='AQNAME is the name of the aquifer.'),
        sa.Column('AREA', sa.Float, comment='AREA is the area of the aquifer measured in square metres.'),
        sa.Column('AQUIFER_NUMBER', sa.String,
                  comment='AQUIFER NUMBER is a text field created from the AQUIFER_ID corresponding '
                          'to the Aquifer Tag in GW_AQUIFERS.'),
        sa.Column('AQUIFER_MATERIALS', sa.String, comment='AQUIFER MATERIALS is a broad grouping of '
                                                          'geologic material found in the '
                                                          'aquifer. Acceptable values are "Sand and Gravel", "Sand", '
                                                          '"Gravel" or "Bedrock".'),
        sa.Column('PRODUCTIVITY', sa.String, comment='PRODUCTIVITY represents an aquifers ability to transmit '
                                                     'and yield groundwater '
                                                     'and is inferred from any combination of: the aquifer’s '
                                                     'transmissivity values, '
                                                     'specific capacity of wells, well yields, description of '
                                                     'aquifer materials, '
                                                     'and sources of recharge (such as rivers or lakes), '
                                                     'or a combination. '
                                                     'Acceptable values are "Low", "Moderate", "High".'),
        sa.Column('VULNERABILITY', sa.String,
                  comment='VVULNERABILITY of an aquifer to contamination indicates the aquifer’s '
                          'relative intrinsic vulnerability to impacts from human activities at the '
                          'land surface. Vulnerability is based on: the type, '
                          'thickness, and extent of '
                          'geologic materials above the aquifer, depth to water table (or to top of '
                          'confined aquifer), and type of aquifer materials. Acceptable values are '
                          '"Low", "Moderate", and "High".'),
        sa.Column('DEMAND', sa.String, comment='DEMAND describes the level of groundwater use and represents '
                                               'the level of reliance '
                                               'on the resource for supply at the time of mapping. Demand may be '
                                               '"Low", "Moderate", or "High".'),
        sa.Column('AQUIFER_CLASSIFICATION', sa.String,
                  comment='AQUIFER CLASSIFICATION categorizes an aquifer based on its level '
                          'of development (groundwater use) and '
                          'vulnerability to contamination, '
                          'at the time of mapping. For more information see J. Berardinucci '
                          'and K. Ronneseth. 2002: Guide to Using '
                          'The BC Aquifer Classification '
                          'Maps For The Protection And Management Of Groundwater. Level of '
                          'development of an aquifer is described as: "High" (I), "Moderate" '
                          '(II), "Low" (III). Vulnerability is '
                          'coded as "High" (A), "Moderate" '
                          '(B), or "Low" (C) . For example, a class IA aquifer would be '
                          'heavily developed with high vulnerability to contamination, while '
                          'a IIIC would be lightly developed with low vulnerability.'),
        sa.Column('ADJOINING_MAPSHEET', sa.String, comment='ADJOINING MAPSHEET denotes if the spatial '
                                                           'extent of the aquifer extends '
                                                           'over more than one BC Geographic Series '
                                                           '(BCGS) 1:20,000 scale mapsheet. '
                                                           'Acceptable values are "Yes" and "No".'),
        sa.Column('AQUIFER_NAME', sa.String, comment='AQUIFER NAME for a specific aquifer is typically '
                                                     'derived from geographic names'
                                                     ' or names in common use, but may also be lithologic or '
                                                     'litho-stratigraphic '
                                                     'units, e.g., ''Abbotsford-Sumas'', ''McDougall Creek Deltaic''.'),
        sa.Column('AQUIFER_RANKING_VALUE', sa.Float,
                  comment='AQUIFER RANKING VALUE is a points based numerical value used to '
                          'determine an aquifers priority in terms of the level of development '
                          'of ground water use. For more information '
                          'see J. Berardinucci and K. '
                          'Ronneseth. 2002: Guide to Using The BC Aquifer Classification Maps '
                          'For The Protection And Management Of Groundwater. The ranking is '
                          'the sum of the point values for each of the following physical '
                          'criteria: productivity, size, vulnerability, demand, type of use, '
                          'and documented quality concerns and quantity '
                          'concerns. Ranking scores '
                          'range from "Low" (5) to "High" (21).'),
        sa.Column('DESCRIPTIVE_LOCATION', sa.String,
                  comment='DESCRIPTIVE LOCATION is a brief description of the geographic '
                          'location of the aquifer. The description is usually referenced to a '
                          'nearby major natural geographic area or '
                          'community, e.g., "Grand Forks".'),
        sa.Column('LITHO_STRATOGRAPHIC_UNIT', sa.String,
                  comment='LITHO STRATOGRAPHIC UNIT is the named permeable geologic unit '
                          '(where available) that comprises the aquifer. It is typically '
                          'either; the era of deposition, the name of a specific formation '
                          'and or the broad material types, '
                          'e.g., "Paleozoic to Mesozoic Era"'
                          ', "Cache Creek Complex", "Intrusive Rock".'),
        sa.Column('QUALITY_CONCERNS', sa.String, comment='QUALITY CONCERNS is the extent of documented '
                                                         'concerns within the aquifer '
                                                         'at the time of mapping. Quality concerns such as '
                                                         'contaminants may be '
                                                         '"Isolated", "Local", or "Regional" in extent. It is '
                                                         'possible to have no '
                                                         'quality concerns documented for a given aquifer.'),
        sa.Column('AQUIFER_DESCRIPTION_RPT_URL', sa.String,
                  comment='AQUIFER DESCRIPTION RPT URL is the Uniform Resource Locator '
                          '(URL) for the Aquifer Description '
                          'report available in Portable '
                          'Document Format (PDF). The date-stamped report describes '
                          'characteristics of the aquifer such '
                          'as: location, vulnerability, '
                          'lithology and hydrological parameters.'),
        sa.Column('AQUIFER_STATISTICS_RPT_URL', sa.String,
                  comment='AQUIFER STATISTICS RPT URL is the Uniform Resource Locator '
                          '(URL) for the Aquifer Summary Statistics report available in '
                          'Comma Separated Value (CSV) format. The date-stamped report '
                          'provides a statistical summary outlining the characteristics '
                          'of all wells associated within the aquifer, including average '
                          'well depth and maximum rate of flow.'),
        sa.Column('AQUIFER_SUBTYPE_CODE', sa.String, comment='AQUIFER SUBTYPE CODE specifies a '
                                                             'standardized code which categorizes '
                                                             'an aquifer based on how it was formed '
                                                             'geologically (depositional '
                                                             'description). Understanding of how aquifers '
                                                             'were formed governs '
                                                             'important attributes such as their productivity, '
                                                             'vulnerability to '
                                                             'contamination as well as proximity and likelihood '
                                                             'of hydraulic '
                                                             'connection to streams. Aquifer sub-type differs from '
                                                             'AQUIFER CLASSIFICATION in that the later system '
                                                             'classifies aquifers '
                                                             'based on their level of development and '
                                                             'vulnerability. Further '
                                                             'details on aquifer sub-types can '
                                                             'be found in Wei et al., 2009: '
                                                             'Streamline Watershed Management '
                                                             'Bulletin Vol. 13/No. 1.The code '
                                                             'value is a combination of an aquifer'
                                                             ' type represented by a '
                                                             'number and an optional letter '
                                                             'representing a more specific aquifer '
                                                             'sub-type. For example aquifer sub-type '
                                                             'code 6b is a comprised of '
                                                             'the aquifer type number (6: Crystalline '
                                                             'bedrock aquifers) and '
                                                             'subtype letter (b) specifically described '
                                                             'as: Fractured crystalline '
                                                             '(igneous intrusive or metamorphic,'
                                                             ' meta-sedimentary, meta-volcanic, '
                                                             'volcanic) rock aquifers. Initial code '
                                                             'values range from 1a to 6b.'),
        sa.Column('QUANTITY_CONCERNS', sa.String, comment='QUANTITY CONCERNS is the extent of documented concerns '
                                                          'within the aquifer '
                                                          'at the time of mapping. Quantity concerns such as '
                                                          'dry wells may be '
                                                          '"Isolated", "Local", or "Regional" in extent. It is '
                                                          'possible to have '
                                                          'no quantity concerns documented for a given aquifer.'),
        sa.Column('SIZE_KM2', sa.Float,
                  comment='SIZE KM2 is the approximate size of the aquifer in square kilometers.'),
        sa.Column('TYPE_OF_WATER_USE', sa.String,
                  comment='TYPE OF WATER USE describes the type of known water use at the '
                          'time of mapping which indicates the variability or diversity of the '
                          'resource as a supply source. Water use categories include: 1) '
                          '"Potential Domestic" may not be primarily used as a source of '
                          'drinking water but has the potential to be in the future and should '
                          'be protected for such use; 2) "Domestic" used primarily as a '
                          'source of drinking water; and 3) "Multiple" used as a source of '
                          'drinking water, plus extensively for other uses such as irrigation.'),
        sa.Column('PRODUCTIVITY_CODE', sa.String,
                  comment='PRODUCTIVITY CODE is a description of the relative volume of water '
                          'being produced by the aquifer.'),
        sa.Column('DEMAND_CODE', sa.String, comment='DEMAND CODE is a code used to classify the demand.'),
        sa.Column('VULNERABILITY_CODE', sa.String,
                  comment='VULNERABILITY CODE is a code used to identify the vulnerability.'),
        sa.Column('CLASSIFICATION_CODE', sa.String,
                  comment='CLASSIFICATION CODE is the aquifer classification system has two '
                          'components: 1) a classification component to categorize aquifers '
                          'based on their current level of development, (use) and vulnerability '
                          'to contamination, and 2) a ranking component to indicate '
                          'the relative '
                          'importance of an aquifer. The classification component categorizes '
                          'aquifers according to level of development and vulnerability to '
                          'contamination: Level of Development and Vulnerability subclasses '
                          'are designated. The composite of these two subclasses is the Aquifer '
                          'Class (Table 1). Development subclass: The level of development of '
                          'an aquifer is determined by assessing demand verses the aquifers '
                          'yield or productivity. A high (I), moderate (II), or low (III) '
                          'level of development can be designated. Vulnerability subclass: '
                          'The vulnerability of an aquifer to contamination '
                          'from surface sources '
                          'is assessed based on: type, thickness and extent '
                          'of geologic materials '
                          'overlying the aquifer, depth to water (or top of confined aquifers), '
                          'and the type of aquifer materials. A high '
                          '(A),moderate (B), or low (C) '
                          'vulnerability can be designated. Aquifer Class: '
                          'The combination of the '
                          'three development and three vulnerability subclasses results in nine '
                          'aquifer classes (Table 1). For example, a class IA aquifer would be '
                          'heavily developed with high vulnerability to contamination, while a '
                          'IIIC would be lightly developed with low vulnerability.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is a ArcSDE spatial column.'),
        sa.Column('FEATURE_AREA_SQM', sa.Float, comment=''),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment=''),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a required attribute of feature classes and object classes in a '
                          'GeoDatabase. This attribute is added to a SDE layer that was not previously '
                          'created as part of a GeoDatabase but is now '
                          'being registered with a GeoDatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment=''),
    )

    op.create_table(
        'ground_water_wells',

        sa.Column('WELL_TAG_NO', sa.String, primary_key=True, comment='WELL TAG NO is the unique number of the '
                                                                      'groundwater well as assigned '
                                                                      'by the Province of British Columbia'),
        sa.Column('OBJECTID', sa.Integer,
                  comment='OBJECTID is a required attribute of feature classes and object classes in '
                          'a GeoDatabase. This attribute is added to a SDE layer that was not previously '
                          'created as part of a GeoDatabase but is now being registered '
                          'with a GeoDatabase.'),
        sa.Column('SOURCE_ACCURACY', sa.String,
                  comment='SOURCE ACCURACY is a groundwater well locations are identified '
                          'onto well cards by well drillersas part of the drilling process. '
                          'There is no statutory requirement for welldrillers to submit these '
                          'records to the Government of British Columbia,therefore not all '
                          'groundwater wells are represented in this dataset. It isuncertain '
                          'the percentage of wells that are represented, but the bestestimate '
                          'is around 50%. The dataset is in a constant state of update anddoes '
                          'not stay static for any length of time. Accuracy is defined by one '
                          'offive codes, as indicated here:A - digitized from well cards with '
                          'well defined cadastre onto IntegratedCadastral Initiative mapping. '
                          'Accuracy is +/- 10 metres.B - digitized from 1:5,000 cadastral mapping. '
                          'Accuracy is +/- 20 metresC - digitized from 1:20,000 cadastral mapping. '
                          'Accuracy is +/- 50 metresD - digitized from old Lands, Forests and '
                          'Water Resources mapping (variousscales) or from well cards with no '
                          'cadastral information. Accuracy is +/-100 metres.E - digitized from '
                          '1:50,000 NTS mapping. Accuracy is +/- 200 metres.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is a ArcSDE spatial column.'),
        sa.Column('FCODE', sa.String,
                  comment='FCODE feature code is most importantly a means of linking a feature to its '
                          'name and definition. For example, the code GB15300120 on a digital geographic '
                          'feature links it to the name "Lake - Dry" with the definition "A lake bed from '
                          'which all water has drained or evaporated." The feature code does NOT mark when '
                          'it was digitized, what dataset it belongs to, how accurate it is, what it '
                          'should look like when plotted, or who is responsible for updating it. It '
                          'only says what it represents in the real world. It also doesnt even matter '
                          'how the lake is represented. If it is a very small lake, it may be stored as '
                          'a point feature. If it is large enough to have a shape at the scale of data '
                          'capture, it may be stored as an outline, or a closed polygon. The same feature '
                          'code still links it to the same definition.'),
        sa.Column('WELL_ID', sa.Integer, comment='WELL ID is a unique identifier for the table.'),
        sa.Column('WELL_LOCATION', sa.String,
                  comment='WELL LOCATION is a location description used in the MS-Access application.'),
        sa.Column('WELL_SEQUENCE_NO', sa.Integer, comment='WELL SEQUENCE NO is a number which describes the order a '
                                                          'particular well islocated in a particular BCGS grid square. '
                                                          'For example the well 082L042321 #1is the '
                                                          'first well located in '
                                                          'BCGS grid 082L042321. Before a system'
                                                          ' generatednon-intelligent '
                                                          'WELL TAG NUMBER was in use this is how'
                                                          ' particular wells werenamed.'),
        sa.Column('WELL_IDENTIFICATION_PLATE_NO', sa.Integer,
                  comment='The Groundwater Protection Regulation of the Water Act '
                          'requires a WELL IDENTIFICATION PLATE NO for water supply '
                          'system wells and new and altered water supply wells.'
                          ' WLAP produces these aluminum plates with a unique number '
                          'for each plate. These plates are attached to the pump'
                          ' house or well by the drillers. Existing wells can have '
                          'these plates attached after the fact, especially if any'
                          ' lab samples or other information is being collected '
                          'about the well.'),
        sa.Column('WATER_UTILITY_FLAG', sa.String,
                  comment='WATER UTILITY FLAG is some wells belong to water utilities for '
                          'provision of water to their.'),
        sa.Column('WATER_SUPPLY_WELL_NAME', sa.String,
                  comment='The WATER SUPPLY WELL NAME is the Utilitys name for this well. '
                          'This is used when the well is owned by a Utility under the '
                          'Water Act. The Utility has applied and been granted a licence '
                          'to be a Water Supply Purveyor. This data is only filled in '
                          'when the well is owned by a Utility. E.g. Parksville Water '
                          'Utility calls one of its wells "Roberts Road Well No. 5"'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer, comment='WELL TAG NUMBER is an unique business well identifier.'),
        sa.Column('WATER_SUPPLY_SYSTEM_NAME', sa.String,
                  comment='The WATER SUPPLY SYSTEM NAME is the name of a Utility '
                          'under the Water Act. The Utility has applied and been '
                          'granted a licence to be a Water Supply Purveyor. This data'
                          ' is only filled in when the well is owned by a Utility.'
                          ' E.g. Parksville Water Utility.'),
        sa.Column('OBSERVATION_WELL_NUMBER', sa.Integer,
                  comment='The OBSERVATION WELL NUMBER exists when a well has been '
                          'selected for monitoring. An Observation well will have water '
                          'level readings recorded to track groundwater levels.'),
        sa.Column('AQUIFER_LITHOLOGY_CODE', sa.String,
                  comment='AQUIFER LITHOLOGY CODE is an aquifer lithology identifier, '
                          'enables lithology layers to be indentified by a short reference.'),
        sa.Column('WATER_DEPTH', sa.Integer, comment='WATER DEPTH, how far down the well before water is reached.'),
        sa.Column('ARTESIAN_FLOW_VALUE', sa.Integer,
                  comment='The ARTESIAN FLOW VALUE is the Artesian water flow measurement of'
                          ' the flow that occurs naturally due to inherent water pressure'
                          ' in the WELL. The measurement is in ARTESIAN FLOW UNITS.'),
        sa.Column('BCGS_ID', sa.Integer,
                  comment='BCGS ID is an internal ID to track creation of unique business BCGS number.'),
        sa.Column('WATERSHED_CODE', sa.String, comment='WATERSHED CODE is a watershed identifier, uniquely identifies '
                                                       'a water shed.'),
        sa.Column('BCGS_NUMBER', sa.String,
                  comment='The BCGS NUMBER is used by the Mapsheets which are based on the British'
                          ' Columbia Geographic System (BCGS) number scheme. The mapsheet number '
                          'is added to the well record after the well record has been added '
                          'in the system.'),
        sa.Column('BEDROCK_DEPTH', sa.Integer, comment='The BEDROCK DEPTH captures the depth at which bedrock starts.'),
        sa.Column('CERTIFICATION', sa.String,
                  comment='CERTIFICATION can be used to collect water WELL certificate information.'
                          ' Not currently being used.'),
        sa.Column('CHEMISTRY_LAB_DATA', sa.String,
                  comment='Chemistry lab data exists. (flag), lab data exists usually tied '
                          'to chemistry site id.'),
        sa.Column('CHEMISTRY_SITE_ID', sa.String,
                  comment='Chemistry site ID number, assigned by water EMS (environmental '
                          'managment ssytem)'),
        sa.Column('CLASS_OF_WELL', sa.String,
                  comment='The CLASS OF WELL is a classification defined in the Groundwater '
                          'Protection Regulation of the Water Act. The classes are : Water Supply,'
                          ' Monitoring, Recharge / Injection, Dewatering / Drainage,'
                          ' Remediation, Geotechnical.'),
        sa.Column('UTM_NORTH', sa.Float,
                  comment='The UTM NORTH attribute stored in the spatial database and associated '
                          'with the WELL TAG NUMBER coordinated.'),
        sa.Column('CONSTRUCTION_END_DATE', sa.DateTime,
                  comment='CONSTRUCTION END DATE is the date when WELL construction'
                          ' was complete, defaults to date the well record was'
                          ' added to the system.'),
        sa.Column('CONSTRUCTION_METHOD_CODE', sa.String,
                  comment='The WELL CONSTRUCTION METHOD is the method of drilling '
                          'the Well.The construction methods are :'
                          ' DUG, DRILLED, DRIVING, JETTING, SPRING or OTHER.'),
        sa.Column('CONSTRUCTION_METHOD_NAME', sa.String, comment='The CONSTRUCTION METHOD NAME is the method of '
                                                                 'constructing the well. Example DRILLED '
                                                                 'indicates a drill'
                                                                 ' rig was used to construct the well. '
                                                                 'Indicates the industry '
                                                                 'trends in well construction methods.'),
        sa.Column('CONSTRUCTION_START_DATE', sa.DateTime, comment='CONSTRUCTION START DATE is the date when WELL'
                                                                  ' construction was started.'),
        sa.Column('CONSULTANT_COMPANY', sa.String, comment='CONSULTANT COMPANY is a description of consulting company '
                                                           'hired by owner to locate well site.'),
        sa.Column('CONTRACTOR_INFO_1', sa.String,
                  comment='CONTRACTOR_ INFO 1 is MS Access Support for information field.'),
        sa.Column('CONTRACTOR_INFO_2', sa.String,
                  comment='CONTRACTOR_ INFO 2 is MS Access Support for information field.'),
        sa.Column('CONTRACTOR_WELL_PLATE_NMBR', sa.String, comment='CONTRACTOR WELL PLATE NMBR is that the Contractor '
                                                                   'may assign well plate number to a WELL. If the'
                                                                   ' driller uses one of the WLAP identification plate,'
                                                                   ' then this number may be the same as the '
                                                                   'WELL_IDENTIFICATION_PLATE_NO. '
                                                                   'Sometimes drillers have their '
                                                                   'own plates made up and this number is different.'),
        sa.Column('COORDINATE_X', sa.String,
                  comment='COORDINATE X is an old three parameter coordinate system (arbitraty)'
                          ' supported for old maps with well data.'),
        sa.Column('COORDINATE_Y', sa.String,
                  comment='COORDINATE Y is an old three parameter coordinate system (arbitraty)'
                          ' supported for old maps with well data.'),
        sa.Column('COORDINATE_Z', sa.String,
                  comment='COORDINATE Z is an old three parameter coordinate system (arbitraty) '
                          'supported for old maps with well data.'),
        sa.Column('CREW_DRILLER_NAME', sa.String,
                  comment='The CREW DRILLER NAME is the first and last name of a certified '
                          'water well Driller.'),
        sa.Column('UTM_EAST', sa.Float,
                  comment='The UTM EAST attribute stored in the spatial database and associated with '
                          'the WELL TAG NUMBER coordinated.'),
        sa.Column('CREW_HELPER_NAME', sa.String, comment='CREW HELPER NAME is the name of Driller Helper.'),
        sa.Column('DATE_ENTERED', sa.DateTime,
                  comment='DATE ENTERED is automatically updated when a new well record is '
                          'added to the system.'),
        sa.Column('DEPTH_WELL_DRILLED', sa.Integer,
                  comment='DEPTH WELL DRILLED is the finished Well depth, represented '
                          'in units of feet bgl (below ground level).'),
        sa.Column('DEVELOPMENT_HOURS', sa.Integer,
                  comment='DEVELOPMENT HOURS is the total hours devoted to develop WELL '
                          '(develop in this means enabling production of water).'),
        sa.Column('DEVELOPMENT_NOTES', sa.String, comment='DEVELOPMENT NOTES is the additional notes regarding well'
                                                          ' development effort.'),
        sa.Column('DIAMETER', sa.String, comment='DIAMETER is a well diameter, represented in units of inches.'),
        sa.Column('DRILLER_COMPANY_CODE', sa.String, comment='DRILLER COMPANY CODE is a numeric code for identified'
                                                             ' driller company name.'),
        sa.Column('DRILLER_COMPANY_NAME', sa.String, comment='The DRILLER COMPANY NAME is the compant Drillers work'
                                                             ' for, if they work for a company.'),
        sa.Column('DRILLER_WELL_ID', sa.Integer, comment='MS-Access defined WATER WELL ID, used during upload into '
                                                         'MS-Access application'),
        sa.Column('ELEVATION', sa.Integer, comment='The ELEVATION is the elevation above sea level in feet of the'
                                                   ' ground surface at the WELL.'),
        sa.Column('FIELD_LAB_DATA', sa.String, comment='The FIELD LAB DATA indicates there is Chemistry field data '
                                                       '(flag), field chemistry information kept in a paper copy. '
                                                       'Y - yes there is field data. N - No there is no field data.'),
        sa.Column('GENERAL_REMARKS', sa.String, comment='GENERAL REMARKS is the general water well comment.'),
        sa.Column('GRAVEL_PACKED_FLAG', sa.String, comment='GRAVEL PACKED FLAG indicated whether or not a gravel pack'
                                                           ' was applied during the creation of the WELL.'),
        sa.Column('GRAVEL_PACKED_FROM', sa.Integer, comment='GRAVEL PACKED FROM indicates whether or not degree gravel'
                                                            ' dispersed around WELL site.'),
        sa.Column('GRAVEL_PACKED_TO', sa.Integer, comment='GRAVEL PACKED TO indicates whether or not degree gravel '
                                                          'dispersed around WELL site.'),
        sa.Column('GROUND_WATER_FLAG', sa.String,
                  comment='GROUND WATER FLAG indicates if a ground water report exists or not.'),
        sa.Column('INDIAN_RESERVE', sa.String, comment='INDIAN RESERVE is the additional parcels identifiers for land '
                                                       'in B.C. include Legal Indian Reserve.'),
        sa.Column('INFO_OTHER', sa.String, comment='INFO OTHER is the additional information has been captured about '
                                                   'this WELL that is significant.'),
        sa.Column('INFO_SITE', sa.String, comment='The INFO SITE is additional site information, backward compatible'
                                                  ' attribute to capture legacy site information.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='Latitude coordinate, used to locate a WELL, alternative location method to UTM.'),
        sa.Column('LEGAL_BLOCK', sa.String,
                  comment='LEGAL BLOCK is the additional parcels identifiers for land in B.C. '
                          'include Legal block.'),
        sa.Column('LEGAL_DISTRICT_LOT', sa.String, comment='The LEGAL DISTRICT LOT is part of the legal description of'
                                                           ' the land the well is located on. Example 2514S'),
        sa.Column('LEGAL_LAND_DISTRICT_CODE', sa.String,
                  comment='The LEGAL_LAND_DISTRICT_CODE represent Parcels of land '
                          'in B.C. can be identifed by the combination of Lot, Legal '
                          'Land District and Map # identifiers. This attribute consists'
                          ' of the Legal Land District to help identify the property '
                          'where the WELL is located.Code District1 Alberni 2 Barclay '
                          '3 Bright 4 Cameron 5 Cariboo 6 Cassiar 7 Cedar 8 Chemainus '
                          '9 Clayoquot 10 Coast Range 1 11 Coast Range 2 12 Coast Range '
                          '3 13 Coast Range 4 14 Coast Range 5 15 Comiaken 16 Comox 17 '
                          'Cowichan 18 Cowichan Lake 19 Cranberry 20 Douglas 21 Dunsmuir '
                          '22 Esquimalt 23 Goldstream 24 Helmcken 25 Highland 26 Kamloops '
                          '(KDYD) 27 Kootenay 28 Lake 29 Lillooet 30 Malahat 31 '
                          'Metchosin 32 Mountain 33 Nanaimo 34 Nanoose 35 Nelson 36 '
                          'Newcastle 37 New Westminster 38 Nootka 39 North Saanich 40 '
                          'Osoyoos (ODYD) 41 Otter 42 Oyster 43 Peace River 44 Quamichan '
                          '45 Queen Charlotte 46 Renfrew 47 Rupert 48 Sahtlam 49'
                          ' Sayward 50 Seymour 51 Shawnigan 52 Similkameen 53 Somenos'
                          ' 54 Sooke 55 South Saanich 56 Texada Island 57 Victoria '
                          '58 Wellington 59 Yale (YDYD).'),
        sa.Column('LEGAL_LAND_DISTRICT_NAME', sa.String,
                  comment='The LEGAL LAND DISTRICT NAME is part of the legal description'
                          ' of the land the well is located on. Example CHEMAINUS.Alberni '
                          'Barclay Bright Cameron Cariboo Cassiar Cedar Chemainus '
                          'Clayoquot Coast Range 1 Coast Range 2 Coast Range 3 Coast'
                          ' Range 4 Coast Range 5 Comiaken Comox Cowichan Cowichan Lake'
                          ' Cranberry Douglas Dunsmuir Esquimalt Goldstream Helmcken'
                          ' Highland Kamloops (KDYD) Kootenay Lake Lillooet Malahat '
                          'Metchosin Mountain Nanaimo Nanoose Nelson Newcastle New '
                          'Westminster Nootka North Saanich Osoyoos (ODYD) Otter Oyster'
                          ' Peace River Quamichan Queen Charlotte Renfrew Rupert Sahtlam '
                          'Sayward Seymour Shawnigan Similkameen Somenos Sooke South '
                          'Saanich Texada Island Victoria Wellington Yale (YDYD)'),
        sa.Column('UTM_ACCURACY_CODE', sa.String,
                  comment='UTM ACCURACY CODE is a description of how accurate the UTM coordinate '
                          'position is. Also implies scale to the coordinate.Codes are numeric '
                          '01 etc.... 01 - less than 3 metres margin of error 02 - 3-10 metres'
                          ' margin of error 03 - 10-30 metres margin of error 04 - 30-100 '
                          'metres margin of error 1:25 000 scale 05 - 100-300 metres margin '
                          'of error 1:50 000 scale 06 - 300-1000 metres margin of error '
                          '1:125 000 scale 07 - 1000-3000 metres margin of error 1:250 000 '
                          'scale 08 - 3000-10 000 metres margin of error 09 - well location '
                          'is unknown 10 - UTM Zone 10 from 1:50 000 scale 30-100 metres moe.'
                          ' 11 - UTM Zone 11 from 1:50 000 scale 30-100 metres.'),
        sa.Column('LEGAL_MISCELLANEOUS', sa.String,
                  comment='LEGAL MISCELLANEOUS is the additional legal land information.'),
        sa.Column('LEGAL_PLAN', sa.String, comment='LEGAL PLAN is the parcels of land in B.C. can be identifed by the '
                                                   'combination of Lot, Legal Land District and '
                                                   'Plan # identifiers. This '
                                                   'attribute consists of the Legal Plan to help'
                                                   ' identify the property where '
                                                   'the WELL is located.'),
        sa.Column('LEGAL_RANGE', sa.String,
                  comment='LEGAL RANGE is the additional parcels identifiers for land in B.C. '
                          'include legal range.'),
        sa.Column('LEGAL_SECTION', sa.String, comment='LEGAL SECTION is the additional parcels identifiers for land in '
                                                      'B.C. include Legal section.'),
        sa.Column('LEGAL_TOWNSHIP', sa.String,
                  comment='LEGAL TOWNSHIP is the additional parcels identifiers for land in'
                          ' B.C. include Legal township.'),
        sa.Column('LITHOLOGY_DESCRIPTION_COUNT', sa.String, comment='LITHOLOGY DESCRIPTION COUNT is the number of'
                                                                    ' Lithology layers identified.'),
        sa.Column('LITHOLOGY_FLAG', sa.String, comment='The LITHOLOGY FLAG indictates if there is Lithology data '
                                                       'available for the well. Y - yes the soil and subsurface '
                                                       'material types have been documented.N - the lithology is '
                                                       'not documented.'),
        sa.Column('LITHOLOGY_MEASURMENT_UNIT', sa.String, comment='LITHOLOGY MEASURMENT UNIT is the aquifer '
                                                                  'lithology measurement units (inches,, feet) used to '
                                                                  'refence the lithology layers '
                                                                  'associated with the WELL.'),
        sa.Column('LOCATION_ACCURACY', sa.String, comment='LOCATION ACCURACY is the estimated location accuracy. '
                                                          'The values for this field range from '
                                                          '1 through 5. The number '
                                                          '5 represents the most accurate estimate.'
                                                          ' The LOC ACCURACY CODE'
                                                          ' is a number 1 to 5 that indicates the '
                                                          'scale of map the location '
                                                          'is derived from. Example, 5 is a 1:50,000 '
                                                          'map. There is another '
                                                          'scale that is used, with values A - well '
                                                          'cards to cadastre or'
                                                          ' GPS +- 10m; B - 1:5000 maps +- 20m; '
                                                          'C - 1:20,000 maps +-50m; '
                                                          'D-old Dept of L,F WR maps or well cards without cadastre +-'
                                                          ' 100m; E - 1:50,000 maps +- 200m;'
                                                          'F - CDGPS differential GPS +- 1m.'),
        sa.Column('LOC_ACCURACY_CODE', sa.String,
                  comment='The LOC ACCURACY CODE is a number that indicates the scale of '
                          'map the location is derived from. Example, 5 is a 1:50,000 map. '
                          'There is another scale that is used, with values A - well cards '
                          'to cadastre or GPS +- 10m; B - 1:5000 maps +- 20m; C - 1:20,000 '
                          'maps +-50m; D-old Dept of L,F WR maps or well cards without'
                          ' cadastre +- 100m; E - 1:50,000 maps +- 200m;F - CDGPS '
                          'differential GPS +- 1m. Accuracy Codes for Horizontal'
                          ' Coordinates.1 < 3 metres margin of error. Differential GPS'
                          ' or location measured in field from known benchmarks.2 3-10'
                          ' metres margin of error. location measured in field from mapped '
                          'features. 3 10-30 metres margin of error. location measured in '
                          'field from mapped features. points plotted in field on topographic'
                          ' maps of 1:10 000 scale or larger single GPS measurement. '
                          '4 30-100 metres margin of error. points plotted in field on '
                          'topographic maps of 1:25 000 scale. 5 100-300 metres margin of error.'),
        sa.Column('LONGITUDE', sa.Float, comment='Longitude coordinate, used to locate a WELL, alternative '
                                                 'location method to UTM.'),
        sa.Column('LOT_NUMBER', sa.String, comment='LOT NUMBER is the parcels of land in B.C. can be identifed by the '
                                                   'combination of Lot, Legal Land District and Map # identifiers. '
                                                   'This attribute consists of the Lot to help identify the property '
                                                   'where the WELL is located.'),
        sa.Column('MERIDIAN', sa.String,
                  comment='The MERIDIAN indicates if the location of the well is east or west of '
                          'the 6th meridian which runs North-South.The meridian is part of a legal'
                          ' description for land in British Columbia. Example W6TH - the well is west '
                          'of the 6th meridian.'),
        sa.Column('MINISTRY_OBSERVATION_WELL_STAT', sa.String,
                  comment='MINISTRY OBSERVATION WELL STAT is the ministry of'
                          ' Water Land and Air Protection, formerly (Ministry '
                          'of Environment) observation.'),
        sa.Column('MS_ACCESS_NUM_OF_WELL', sa.String, comment='The MS ACCESS NUM OF WELL is the sequence of the wells '
                                                              'entered by a driller in the MS Access Drilling '
                                                              'Data Capture System.'),
        sa.Column('OLD_MAPSHEET', sa.String,
                  comment='OLD_MAPSHEET is an identifer, used to track changes to the well location.'),
        sa.Column('OLD_WELL_NUMBER', sa.String, comment='Old well number, used to track wells on old-style well maps '
                                                        'using X,,Y,Z and old three parameter arbritrary coordinate '
                                                        'system. (required to support old maps with well data)'),
        sa.Column('OTHER_CHEMISTRY_DATA', sa.String, comment='OTHER CHEMISTRY DATA is the reference for additional '
                                                             'sources of chemistry data.'),
        sa.Column('OTHER_EQUIPMENT', sa.String, comment='OTHER EQUIPMENT is the description of other equipment used '
                                                        'to create the WELL.'),
        sa.Column('OTHER_INFORMATION', sa.String, comment='OTHER INFORMATION is the brief description of other well '
                                                          'data available.'),
        sa.Column('OWNERS_WELL_NUMBER', sa.String, comment='OWNERS WELL NUMBER is the local WELL number applied by '
                                                           'owner for internal tracking.'),
        sa.Column('OWNER_ID', sa.Integer,
                  comment='OWNER ID is an owner Identification, uniqely identifies a WELL owner.'),
        sa.Column('SURNAME', sa.String, comment='SURNAME is the last Name of WELL owner.'),
        sa.Column('PERFORATION_FLAG', sa.String, comment='The PERFORATION FLAG indicates if the steel casing has been '
                                                         'perforated by a hydraulic shear.'
                                                         ' Perforations improve flow to '
                                                         'the bottom of the well. Some wells '
                                                         'have been perforated rather '
                                                         'than having a screen installed. Perforations do not consider '
                                                         'soil size. Y- yes there are holes in the casing.'
                                                         ' N- no additional holes in casing.'),
        sa.Column('PERMIT_NUMBER', sa.String,
                  comment='The PERMIT NUMBER is used if permit numbers are issued to drill a WELL.'),
        sa.Column('PID', sa.Integer, comment='PID is a parcel Identifier, identifes parcel where well is located.'),
        sa.Column('PLATE_ATTACHED_BY', sa.String,
                  comment='The PLATE ATTACHED BY is the name of the person who attached '
                          'the WELL IDENTIFICATION PLATE. The Groundwater Protection '
                          'Regulation of the Water Act requires this information for water'
                          ' supply system wells and new and altered water supply wells.'),
        sa.Column('PRODUCTION_TIDAL_FLAG', sa.String,
                  comment='PRODUCTION TIDAL FLAG indicates if production well rates are'
                          ' influenced by tidal activity or not.'),
        sa.Column('PUMP_DESCRIPTION', sa.String,
                  comment='PUMP DESCRIPTION is an information, including if a pump exists or not.'),
        sa.Column('PUMP_FLAG', sa.String, comment='PUMP FLAG indicates if a pump is being used on the WELL or not.'),
        sa.Column('REPORTS_FLAG', sa.String, comment='The REPORTS FLAG indicates if there is a report on the National '
                                                     'Topographical System (NTS) filing system '
                                                     'or the utility files(which '
                                                     'are reports submitted in support of an '
                                                     'application for a certificate '
                                                     'of PUBLIC CONVENIENCE AND NECESSITY). '
                                                     'Y yes Well Report(s) Exist . '
                                                     'N - no reports exist'),
        sa.Column('RIG_NUMBER', sa.String, comment='RIG NUMBER is the number asscociated with the drilling rig. '
                                                   'Supplied by the Driller.'),
        sa.Column('QUARTER', sa.String, comment='QUARTER is the additional parcels identifiers for land in B.C. '
                                                'include Legal quarter.'),
        sa.Column('SCREEN_FLAG', sa.String, comment='SCREEN FLAG depicts the use of a screen(s) in a WELL. Indicates '
                                                    'at least 1 SCREEN record is associated with the WELL record.'),
        sa.Column('SCREEN_INFORMATION_TEXT', sa.String, comment='SCREEN INFORMATION TEXT is the additional information '
                                                                'regarding the screen.'),
        sa.Column('SCREEN_LENGTH', sa.String, comment='The SCREEN LENGTH is the total length of the screen assembly, '
                                                      'including blanks and risers. (feet) . Most screens are '
                                                      'cylindrical in shape.'),
        sa.Column('SCREEN_MANUFACTURER', sa.String, comment='The SCREEN MANUFACTURER identifies who made the screen.'),
        sa.Column('SCREEN_WIRE', sa.String, comment='The SCREEN WIRE is the type of screen wire. The wire has different'
                                                    ' cross sections - like WIRE WOUND (round) or '
                                                    'V WIRE WOUND (triangular). '
                                                    'The wire is what some screens are made of.'),
        sa.Column('SEQUENCE_NO', sa.Float,
                  comment='SEQUENCE_NO is a number which describes the order a particular well '
                          'islocated in a particular BCGS grid square. For example the well'
                          ' 082L042321 #1is the first well located in BCGS grid 082L042321. '
                          'Before a system generatednon-intelligent WELL TAG NUMBER was in use'
                          ' this is how particular wells werenamed.'),
        sa.Column('SIEVE_FLAG', sa.String, comment='SIEVE FLAG indicates if Sieve Analysis was done or not, default was'
                                                   ' blank field for No.'),
        sa.Column('SITE_AREA', sa.String, comment='The SITE AREA is the town or nearest describable geogropahic area.'),
        sa.Column('SITE_FLAG', sa.String, comment='SITE_FLAG indicated whether site inspection was done or not.'),
        sa.Column('SITE_ISLAND', sa.String,
                  comment='The SITE ISLAND is the island name, if the well is located on an Island.'),
        sa.Column('SITE_STREET', sa.String,
                  comment='The SITE STREET is the Well location, address (well) description of '
                          'where well is outside additional well information'),
        sa.Column('SURFACE_SEAL_DEPTH', sa.Integer,
                  comment='The SURFACE SEAL DEPTH indicates depth of surface seal which '
                          'is depth in feet below ground surface to bottom of Surface Seal.'),
        sa.Column('SURFACE_SEAL_FLAG', sa.String,
                  comment='The SURFACE SEAL FLAG indicates if a surface seal was applied '
                          'upon completion of WELL.Y- yes surface seal was constructed. N- '
                          'no surface seal was applied. Blank is unknown'),
        sa.Column('SURFACE_SEAL_THICKNESS', sa.Integer, comment='The SURFACE SEAL THICKNESS is the thickness of the '
                                                                '"surface seal" which is a '
                                                                'sealant placed in the annular '
                                                                'space around the outside of '
                                                                'the outermost well casing and '
                                                                'between multiple well casings '
                                                                'and extending to or just below '
                                                                'the ground surface. Good practice '
                                                                'is a sealant with a minimum '
                                                                'thickness of 1 inch, minumum'
                                                                ' length of 15 feet and extending '
                                                                'a minimum of 3 feet into bedrock.'),
        sa.Column('TYPE_OF_RIG', sa.String,
                  comment='Type of RIG (drilling hardware) used during the creation of the WELL.'),
        sa.Column('TYPE_OF_WORK', sa.String,
                  comment='TYPE OF WORK is the legacy attribute contained in MS-Access application. '
                          'Values include NEW or DPD.'),
        sa.Column('WELL_USE_CODE', sa.String,
                  comment='WELL USE CODE is three letter character unique code to identify code.'),
        sa.Column('WELL_USE_NAME', sa.String,
                  comment='The WELL USE NAME is the long well use name. Examples may include '
                          'private, commercial, domestic.'),
        sa.Column('WHEN_CREATED', sa.DateTime, comment='WHEN CREATED is the date and time the entry was created.'),
        sa.Column('WHEN_UPDATED', sa.DateTime,
                  comment='WHEN UPDATED is the date and time the entry was last modified.'),
        sa.Column('WHERE_PLATE_ATTACHED', sa.String, comment='The WHERE PLATE ATTACHED is a description of where the '
                                                             'indentification plate has been attached. The Groundwater '
                                                             'Protection Regulation of the Water Act'
                                                             ' requires this information'
                                                             ' for water supply system wells and new and altered '
                                                             'water supply wells.'),
        sa.Column('WHO_CREATED', sa.String, comment='WHO CREATED is the unique id of the user who created this entry.'),
        sa.Column('WHO_UPDATED', sa.String,
                  comment='WHO UPDATED is the unique id of the user who last modified this entry.'),
        sa.Column('YIELD_UNIT_CODE', sa.String, comment='YIELD UNIT CODE is the yield unit of measure, unique code. '
                                                        'The MS-Access database expects flow rates to'
                                                        ' be entered as USgpm.'),
        sa.Column('YIELD_UNIT_DESCRIPTION', sa.String,
                  comment='YIELD UNIT DESCRIPTION is the yield measurement description, '
                          'if other yield units become supported or if a conversion factor '
                          'is required it could be entered in this attribute.'),
        sa.Column('YIELD_VALUE', sa.Float, comment='YIELD VALUE is the well yield value, measured water yield ammount, '
                                                   'estimate how much water flow a WELL is capable of sustaining.'),
        sa.Column('WELL_LICENCE_GENERAL_STATUS', sa.String, comment='A text value reflects the generalized status of '
                                                                    'authorizations on the given well. '
                                                                    'It value will be '
                                                                    'set based on the contents of the '
                                                                    'AUTHORIZATION STATUS '
                                                                    'attribute coming from eLicensing '
                                                                    'application via a trigger'
                                                                    ' implemented on WELL_LICENCE Table.Acceptable '
                                                                    'Values are:a) UNLICENSEDb) '
                                                                    'LICENSEDc) HISTORICAL.'),
        sa.Column('WELL_DETAIL_URL', sa.String,
                  comment='A HTTP URL link value that contains the Well Tag Number, specifying'
                          ' a direct link to the WELL record in WELLS Public application.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                                                     'store annotation, curve features and CAD data when using the '
                                                     'SDO_GEOMETRY storage data type.'),
    )

    op.create_table(
        'water_allocation_restrictions',

        sa.Column('LINEAR_FEATURE_ID', sa.Integer,
                  comment='LINEAR FEATURE ID is a primary Key to link to stream segments in '
                          'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP as a one to one join. This '
                          'is maintained by business users. E.g., 831792750'),
        sa.Column('RESTRICTION_ID_LIST', sa.String,
                  comment='RESTRICTION ID LIST is a list of one or more restriction IDs of '
                          'stream restriction points downstream from the stream segment. The '
                          'RESTRICTION_IDs correspond with RESTRICTION_IDs in '
                          'WHSE_WATER_MANAGEMENT.WLS_WATER_RESTRICTION_LOC_SVW. E.g., RS34144'),
        sa.Column('PRIMARY_RESTRICTION_CODE', sa.String,
                  comment='PRIMARY RESTRICTION CODE indicates the type of restriction '
                          'point downstream from the stream segment. E.g., FR - '
                          'Fully Recorded; FR_EXC - Fully Recorded Except; PWS - '
                          'Possible Water Shortage; RNW - Refused No Water; OR - '
                          'Office Reserve; UNSPECIFIED - type of '
                          'restriction not specified.'),
        sa.Column('SECONDARY_RESTRICTION_CODES', sa.String,
                  comment='SECONDARY RESTRICTION CODES is a list of additional '
                          'types of water restrictions downstream from the stream'
                          ' segment. E.g., FR - Fully Recorded; FR_EXC - '
                          'Fully Recorded Except; PWS - Possible Water Shortage; '
                          'RNW - Refused No Water; OR - Office Reserve; '
                          'UNSPECIFIED - type of restriction not specified.'),
        sa.Column('FWA_WATERSHED_CODE', sa.String, comment='FWA WATERSHED CODE is a 143 character code derived using a '
                                                           'hierarchy coding scheme. Approximately identifies where a '
                                                           'particular stream is located within the province.'),
        sa.Column('WATERSHED_GROUP_CODE', sa.String, comment='WATERSHED GROUP CODE is the watershed group code '
                                                             'associated with the polygon.'),
        sa.Column('GNIS_NAME', sa.String, comment='GNIS NAME is the BCGNIS (BC Geographical Names Information System) '
                                                  'name associated with the GNIS feature id (an English name was used '
                                                  'where available, otherwise another language was selected).'),
        sa.Column('STREAM_ORDER', sa.Float, comment='STREAM ORDER is the calculated modified Strahler order.'),
        sa.Column('STREAM_MAGNITUDE', sa.Float, comment='STREAM MAGNITUDE is the calculated magnitude.'),
        sa.Column('FEATURE_CODE', sa.String, comment='FEATURE CODE contains a value based on the Canadian Council of'
                                                     ' Surveys and Mappings (CCSM) system for classification of '
                                                     'geographic features.'),
        sa.Column('GEOMETRY', Geometry, comment='GEOMETRY is the column used to reference the spatial coordinates '
                                                'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, primary_key=True,
                  comment='OBJECTID is a required attribute of feature classes and '
                          'object classes in a geodatabase.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                                                     'store annotation, curve features and CAD data when using the '
                                                     'SDO_GEOMETRY storage data type.'),
        sa.Column('FEATURE_LENGTH_M', sa.Float, comment='FEATURE_LENGTH_M is the system calculated length or perimeter '
                                                        'of a geometry in meters'),
    )

    op.create_table(
        'water_rights_licenses',

        sa.Column('WLS_WRL_SYSID', sa.Integer, primary_key=True, comment='WLS WRL SYSID is a system generated unique '
                                                                         'identification number.'),
        sa.Column('POD_NUMBER', sa.String,
                  comment='POD NUMBER is the unique identifier for a Point of Diversion, e.g., PW189413. '
                          'Each POD can have multiple licences associated with it.'),
        sa.Column('POD_SUBTYPE', sa.String,
                  comment='POD SUBTYPE distinguishes the different POD types, i.e., POD (a surface '
                          'water point of diversion), PWD (a point of well diversion that diverts '
                          'groundwater), or PG (a point of groundwater diversion that diverts '
                          'groundwater such as a dugout, ditch or quarry).'),
        sa.Column('POD_DIVERSION_TYPE', sa.String, comment='POD_DIVERSION_TYPE is the type of diversion for a point of '
                                                           'groundwater diversion (PG subtype), i.e., '
                                                           'Dugout, Ditch, Quarry. '
                                                           'Since this only applies to PG subtypes,'
                                                           ' other subypes (POD or PWD)'
                                                           ' will be left blank (null value).'),
        sa.Column('POD_STATUS', sa.String,
                  comment='POD STATUS is the status of the Point of Diversion. Each POD can have '
                          'multiple licences, e.g., Active (one or more active licences associated), '
                          'Inactive (only historical inactive licences associated).'),
        sa.Column('FILE_NUMBER', sa.String,
                  comment='FILE NUMBER is the water business file number, assigned during the '
                          'application phase, e.g., 0321048. A file may hold one or more licences.'),
        sa.Column('WELL_TAG_NUMBER', sa.Integer,
                  comment='WELL TAG NUMBER is a unique well identifier for either registered '
                          'or licensed wells, e.g., 12345.'),
        sa.Column('LICENCE_NUMBER', sa.String,
                  comment='LICENCE NUMBER is the authorization number referenced in the water '
                          'licence document, e.g., 121173.'),
        sa.Column('LICENCE_STATUS', sa.String,
                  comment='LICENCE STATUS represents the existing status of licence, e.g., '
                          'Current, Cancelled, Pending.'),
        sa.Column('LICENCE_STATUS_DATE', sa.DateTime, comment='LICENCE STATUS DATE indicates the last time the '
                                                              'licence status changed.'),
        sa.Column('PRIORITY_DATE', sa.DateTime, comment='PRIORITY DATE is the date from which the precedence of the '
                                                        'licence is established within the first in time first '
                                                        'in right framework.'),
        sa.Column('EXPIRY_DATE', sa.DateTime, comment='EXPIRY DATE is the date the licence expires.'),
        sa.Column('PURPOSE_USE_CODE', sa.String,
                  comment='PURPOSE USE CODE is the use of water authorized by the licence, '
                          'identified as a code, e.g., 02I.'),
        sa.Column('PURPOSE_USE', sa.String,
                  comment='PURPOSE USE is the use of water authorized by the licence, e.g. Industrial.'),
        sa.Column('SOURCE_NAME', sa.String, comment='SOURCE NAME is the aquifer or body of surface water from which '
                                                    'the licence is authorized to extract water. A surface water body '
                                                    'can be a lake, river, creek or any other '
                                                    'surface water source e.g., '
                                                    'Skaha Lake or Kokanee Creek. For a known '
                                                    'aquifer that has been mapped, '
                                                    'the aquifer name is the BC Governments '
                                                    'Aquifer ID number, e.g., 1137. '
                                                    'For an unmapped aquifer, the aquifer '
                                                    'name is derived from water precincts '
                                                    'names in common use, and lithologic or litho-stratigraphic units,'
                                                    ' e.g., Nelson Unconsolidated; Nelson Bedrock.'),
        sa.Column('REDIVERSION_IND', sa.String, comment='REDIVERSION IND is an indicator of whether the Point of Well '
                                                        'Diversion is, for the particular '
                                                        'licence, used to divert water '
                                                        'from another water source, i.e., Y or N.'),
        sa.Column('QUANTITY', sa.Float, comment='QUANTITY is the maximum quantity of water that is authorized to be '
                                                'diverted for the purpose use, e.g., 500.'),
        sa.Column('QUANTITY_UNITS', sa.String, comment='QUANTITY UNITS is the units of measurement for the quantity of '
                                                       'water authorized in the licence, e.g., m3 / year.'),
        sa.Column('QUANTITY_FLAG', sa.String,
                  comment='QUANTITY FLAG is the code used to identify how the total quantity '
                          'is assigned across multiple Points of Well Diversion (PWD) for a '
                          'particular licence and purpose use, i.e., T, M, D, or P.'),
        sa.Column('QUANTITY_FLAG_DESCRIPTION', sa.String, comment='QUANTITY FLAG DESCRIPTION is a description of the '
                                                                  'QUANTITY FLAG code used to'
                                                                  ' identify how the total quantity '
                                                                  'is assigned across multiple '
                                                                  'Points of Well Diversion (PWD) '
                                                                  'for a particular licence and '
                                                                  'purpose use, i.e., T (Total '
                                                                  'demand for purpose, one PWD); '
                                                                  'M (Maximum licensed demand '
                                                                  'for purpose, multiple PWDs, '
                                                                  'quantity at each PWD unknown); '
                                                                  'D (Multiple PWDs for purpose, '
                                                                  'quantities at each are known, '
                                                                  'PWDs on different aquifers); '
                                                                  'P (Multiple PWDs for purpose, '
                                                                  'quantities at each are known, '
                                                                  'PWDs on same aquifer).'),
        sa.Column('QTY_DIVERSION_MAX_RATE', sa.Float,
                  comment='QTY DIVERSION MAX RATE is the maximum authorized diversion '
                          'rate of water within a second, minute or day up to the total '
                          'licensed quantity per year, e.g, 0.006, 2000'),
        sa.Column('QTY_UNITS_DIVERSION_MAX_RATE', sa.String, comment='QTY UNITS DIVERSION MAX RATE are the units of '
                                                                     'measurement for the maximum '
                                                                     'diversion rate of water '
                                                                     'authorized in the licence, e.g., m3/second, '
                                                                     'm3/minute, m3/day, m3/year.'),
        sa.Column('HYDRAULIC_CONNECTIVITY', sa.String, comment='HYDRAULIC CONNECTIVITY is an indicator of whether the '
                                                               'licensed aquifer diversion '
                                                               '(PWD or PG) may be hydraulically '
                                                               'connected to one or more surface'
                                                               ' water sources (stream or '
                                                               'lake), i.e., Likely, Unknown.'),
        sa.Column('PERMIT_OVER_CROWN_LAND_NUMBER', sa.String,
                  comment='PERMIT OVER CROWN LAND NUMBER is an Internal number'
                          ' assigned to a Permit over Crown Land '
                          '(PCL), e.g., 12345.'),
        sa.Column('PRIMARY_LICENSEE_NAME', sa.String,
                  comment='PRIMARY LICENSEE NAME is the primary contact for the licence, '
                          'co-licensees will be displayed as et al.'),
        sa.Column('ADDRESS_LINE_1', sa.String,
                  comment='ADDRESS LINE 1 is the first line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_2', sa.String,
                  comment='ADDRESS LINE 2 is the second line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_3', sa.String,
                  comment='ADDRESS LINE 3 is the third line of the licensees mailing address.'),
        sa.Column('ADDRESS_LINE_4', sa.String,
                  comment='ADDRESS LINE 4 is the fourth line of the licensees mailing address.'),
        sa.Column('COUNTRY', sa.String, comment='COUNTRY is the licensees country.'),
        sa.Column('POSTAL_CODE', sa.String, comment='POSTAL CODE is the licensees postal code.'),
        sa.Column('LATITUDE', sa.Float,
                  comment='LATITUDE is the geographic coordinate, in decimal degrees (dd.dddddd), '
                          'of the location of the feature as measured from the equator, e.g., 55.323653.'),
        sa.Column('LONGITUDE', sa.Float,
                  comment='LONGITUDE is the geographic coordinate, in decimal degrees (-ddd.dddddd), '
                          'of the location of the feature as measured from the prime meridian, '
                          'e.g., -123.093544.'),
        sa.Column('DISTRICT_PRECINCT_NAME', sa.String,
                  comment='DISTRICT PRECINCT NAME is a jurisdictional area within a '
                          'Water District. It is a combination of District and Precinct '
                          'codes and names, e.g., New Westminster / Coquitlam. Not all '
                          'Water Districts contain Precincts.'),
        sa.Column('SHAPE', Geometry, comment='SHAPE is the column used to reference the spatial coordinates '
                                             'defining the feature.'),
        sa.Column('OBJECTID', sa.Integer, comment='OBJECTID is a column required by spatial layers that interact with '
                                                  'ESRI ArcSDE. It is populated with '
                                                  'unique values automatically by SDE.'),
        sa.Column('SE_ANNO_CAD_DATA', BYTEA, comment='SE ANNO CAD DATA is a binary column used by spatial tools to '
                                                       'store annotation, curve features and CAD data when using '
                                                       'the SDO GEOMETRY storage data type.'),
    )


def downgrade():
    pass