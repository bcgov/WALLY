# coding: utf-8
from sqlalchemy import Integer, String, Column, Float
from app.db.base_class import BaseTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class GroundWaterAquifers(BaseTable):
    __tablename__ = 'ground_water_aquifers'

    AQ_TAG = Column(String, primary_key=True, comment='The AQ TAG is an alpha-numeric code assigned to the aquifer to '
                                                      'uniquely identify it.')
    FCODE = Column(String, comment='10	FCODE is a feature code is most importantly a means of linking a feature to '
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
                                   'to the same definition.')
    PERIMETER = Column(Float, comment='PERIMETER is the outside perimeter of the aquifer measured in metres.')
    AQNAME = Column(String, comment='AQNAME is the name of the aquifer.')
    AREA = Column(Float, comment='AREA is the area of the aquifer measured in square metres.')
    AQUIFER_NUMBER = Column(String, comment='AQUIFER NUMBER is a text field created from the AQUIFER_ID corresponding '
                                            'to the Aquifer Tag in GW_AQUIFERS.')
    AQUIFER_MATERIALS = Column(String, comment='AQUIFER MATERIALS is a broad grouping of '
                                               'geologic material found in the '
                                               'aquifer. Acceptable values are "Sand and Gravel", "Sand", '
                                               '"Gravel" or "Bedrock".')
    PRODUCTIVITY = Column(String, comment='PRODUCTIVITY represents an aquifers ability to transmit '
                                          'and yield groundwater '
                                          'and is inferred from any combination of: the aquifer’s '
                                          'transmissivity values, '
                                          'specific capacity of wells, well yields, description of aquifer materials, '
                                          'and sources of recharge (such as rivers or lakes), or a combination. '
                                          'Acceptable values are "Low", "Moderate", "High".')
    VULNERABILITY = Column(String, comment='VVULNERABILITY of an aquifer to contamination indicates the aquifer’s '
                                           'relative intrinsic vulnerability to impacts from human activities at the '
                                           'land surface. Vulnerability is based on: the type, '
                                           'thickness, and extent of '
                                           'geologic materials above the aquifer, depth to water table (or to top of '
                                           'confined aquifer), and type of aquifer materials. Acceptable values are '
                                           '"Low", "Moderate", and "High".')
    DEMAND = Column(String, comment='DEMAND describes the level of groundwater use and represents '
                                    'the level of reliance '
                                    'on the resource for supply at the time of mapping. Demand may be '
                                    '"Low", "Moderate", or "High".')
    AQUIFER_CLASSIFICATION = Column(String, comment='AQUIFER CLASSIFICATION categorizes an aquifer based on its level '
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
                                                    'a IIIC would be lightly developed with low vulnerability.')
    ADJOINING_MAPSHEET = Column(String, comment='ADJOINING MAPSHEET denotes if the spatial '
                                                'extent of the aquifer extends '
                                                'over more than one BC Geographic Series '
                                                '(BCGS) 1:20,000 scale mapsheet. '
                                                'Acceptable values are "Yes" and "No".')
    AQUIFER_NAME = Column(String, comment='AQUIFER NAME for a specific aquifer is typically '
                                          'derived from geographic names'
                                          ' or names in common use, but may also be lithologic or litho-stratigraphic '
                                          'units, e.g., ''Abbotsford-Sumas'', ''McDougall Creek Deltaic''.')
    AQUIFER_RANKING_VALUE = Column(Float, comment='AQUIFER RANKING VALUE is a points based numerical value used to '
                                                  'determine an aquifers priority in terms of the level of development '
                                                  'of ground water use. For more information '
                                                  'see J. Berardinucci and K. '
                                                  'Ronneseth. 2002: Guide to Using The BC Aquifer Classification Maps '
                                                  'For The Protection And Management Of Groundwater. The ranking is '
                                                  'the sum of the point values for each of the following physical '
                                                  'criteria: productivity, size, vulnerability, demand, type of use, '
                                                  'and documented quality concerns and quantity '
                                                  'concerns. Ranking scores '
                                                  'range from "Low" (5) to "High" (21).')
    DESCRIPTIVE_LOCATION = Column(String, comment='DESCRIPTIVE LOCATION is a brief description of the geographic '
                                                  'location of the aquifer. The description is usually referenced to a '
                                                  'nearby major natural geographic area or '
                                                  'community, e.g., "Grand Forks".')
    LITHO_STRATOGRAPHIC_UNIT = Column(String, comment='LITHO STRATOGRAPHIC UNIT is the named permeable geologic unit '
                                                      '(where available) that comprises the aquifer. It is typically '
                                                      'either; the era of deposition, the name of a specific formation '
                                                      'and or the broad material types, '
                                                      'e.g., "Paleozoic to Mesozoic Era"'
                                                      ', "Cache Creek Complex", "Intrusive Rock".')
    QUALITY_CONCERNS = Column(String, comment='QUALITY CONCERNS is the extent of documented '
                                              'concerns within the aquifer '
                                              'at the time of mapping. Quality concerns such as contaminants may be '
                                              '"Isolated", "Local", or "Regional" in extent. It is possible to have no '
                                              'quality concerns documented for a given aquifer.')
    AQUIFER_DESCRIPTION_RPT_URL = Column(String, comment='AQUIFER DESCRIPTION RPT URL is the Uniform Resource Locator '
                                                         '(URL) for the Aquifer Description '
                                                         'report available in Portable '
                                                         'Document Format (PDF). The date-stamped report describes '
                                                         'characteristics of the aquifer such '
                                                         'as: location, vulnerability, '
                                                         'lithology and hydrological parameters.')
    AQUIFER_STATISTICS_RPT_URL = Column(String, comment='AQUIFER STATISTICS RPT URL is the Uniform Resource Locator '
                                                        '(URL) for the Aquifer Summary Statistics report available in '
                                                        'Comma Separated Value (CSV) format. The date-stamped report '
                                                        'provides a statistical summary outlining the characteristics '
                                                        'of all wells associated within the aquifer, including average '
                                                        'well depth and maximum rate of flow.')
    AQUIFER_SUBTYPE_CODE = Column(String, comment='AQUIFER SUBTYPE CODE specifies a '
                                                  'standardized code which categorizes '
                                                  'an aquifer based on how it was formed geologically (depositional '
                                                  'description). Understanding of how aquifers were formed governs '
                                                  'important attributes such as their productivity, vulnerability to '
                                                  'contamination as well as proximity and likelihood of hydraulic '
                                                  'connection to streams. Aquifer sub-type differs from '
                                                  'AQUIFER CLASSIFICATION in that the later system classifies aquifers '
                                                  'based on their level of development and vulnerability. Further '
                                                  'details on aquifer sub-types can be found in Wei et al., 2009: '
                                                  'Streamline Watershed Management Bulletin Vol. 13/No. 1.The code '
                                                  'value is a combination of an aquifer type represented by a '
                                                  'number and an optional letter representing a more specific aquifer '
                                                  'sub-type. For example aquifer sub-type code 6b is a comprised of '
                                                  'the aquifer type number (6: Crystalline bedrock aquifers) and '
                                                  'subtype letter (b) specifically described as: Fractured crystalline '
                                                  '(igneous intrusive or metamorphic, meta-sedimentary, meta-volcanic, '
                                                  'volcanic) rock aquifers. Initial code values range from 1a to 6b.')
    QUANTITY_CONCERNS = Column(String, comment='QUANTITY CONCERNS is the extent of documented concerns '
                                               'within the aquifer '
                                               'at the time of mapping. Quantity concerns such as dry wells may be '
                                               '"Isolated", "Local", or "Regional" in extent. It is possible to have '
                                               'no quantity concerns documented for a given aquifer.')
    SIZE_KM2 = Column(Float, comment='SIZE KM2 is the approximate size of the aquifer in square kilometers.')
    TYPE_OF_WATER_USE = Column(String, comment='TYPE OF WATER USE describes the type of known water use at the '
                                               'time of mapping which indicates the variability or diversity of the '
                                               'resource as a supply source. Water use categories include: 1) '
                                               '"Potential Domestic" may not be primarily used as a source of '
                                               'drinking water but has the potential to be in the future and should '
                                               'be protected for such use; 2) "Domestic" used primarily as a '
                                               'source of drinking water; and 3) "Multiple" used as a source of '
                                               'drinking water, plus extensively for other uses such as irrigation.')
    PRODUCTIVITY_CODE = Column(String, comment='PRODUCTIVITY CODE is a description of the relative volume of water '
                                               'being produced by the aquifer.')
    DEMAND_CODE = Column(String, comment='DEMAND CODE is a code used to classify the demand.')
    VULNERABILITY_CODE = Column(String, comment='VULNERABILITY CODE is a code used to identify the vulnerability.')
    CLASSIFICATION_CODE = Column(String, comment='CLASSIFICATION CODE is the aquifer classification system has two '
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
                                                 'IIIC would be lightly developed with low vulnerability.')
    GEOMETRY = Column(Geometry, comment='GEOMETRY is a ArcSDE spatial column.')
    FEATURE_AREA_SQM = Column(Float, comment='')
    FEATURE_LENGTH_M = Column(Float, comment='')
    OBJECTID = Column(Integer, comment='OBJECTID is a required attribute of feature classes and object classes in a '
                                       'GeoDatabase. This attribute is added to a SDE layer that was not previously '
                                       'created as part of a GeoDatabase but is now '
                                       'being registered with a GeoDatabase.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='')
