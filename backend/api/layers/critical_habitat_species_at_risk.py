# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, Float
from api.db.base_class import BaseLayerTable
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA


class CriticalHabitatSpeciesAtRisk(BaseLayerTable):
    __tablename__ = 'critical_habitat_species_at_risk'

    CRITICAL_HABITAT_ID = Column(Integer, primary_key=True, autoincrement=False, comment='CRITICAL_HABITAT_ID: is a system generated '
                                                                    'unique identification number. This is the '
                                                                    'primary key of this table. e.g., 1')
    COSEWIC_SPECIES_ID = Column(String, comment='COSEWIC_SPECIES_ID is a unique identification number assigned to '
                                                'the species or taxa (including, if applicable, sub species and'
                                                ' population) assessed by the Committee on the Status of Endangered '
                                                'Wildlife in Canada (COSEWIC) and currently listed on SARA '
                                                'Schedule 1; e.g., 1086.')
    SCIENTIFIC_NAME = Column(String, comment='SCIENTIFIC_NAME is the standard scientific name for the'
                                             ' SARA-listed species or taxa, and can include subspecies;'
                                             ' e.g., Oreoscoptes montanus.')
    COMMON_NAME_ENGLISH = Column(String, comment='COMMON_NAME_ENGLISH is the English name of the species'
                                                 ' or taxa listed on SARA Schedule 1; e.g., Sage Thrasher.')
    COMMON_NAME_FRENCH = Column(String, comment='COMMON_NAME_FRENCH is the French name of the species or taxa'
                                                ' listed on SARA Schedule 1; e.g., Moqueur des armoises.')
    COSEWIC_POPULATION = Column(String, comment='COSEWIC_POPULATION is the population name of the species'
                                                ' or taxa assessed by the Committee on the Status of Endangered'
                                                ' Wildlife in Canada (COSEWIC) and currently listed on SARA'
                                                ' Schedule 1; e.g., Southern Mountain population.')
    CRITICAL_HABITAT_STATUS = Column(String, comment='CRITICAL_HABITAT_STATUS is the stage of development'
                                                     ' of the critical habitat polygon; e.g., Final or Candidate')
    CRITICAL_HABITAT_REGION = Column(String, comment='CRITICAL_HABITAT_REGION is a regional identifier '
                                                     'optionally used to group critical habitat polygons;'
                                                     ' e.g. "Southeastern BC".')
    CRITICAL_HABITAT_SITE_ID = Column(String, comment='CRITICAL_HABITAT_SITE_ID is the alphanumeric code of a '
                                                      'critical habitat site as defined in the federal '
                                                      'recovery document; e.g., 937_5.')
    CRITICAL_HABITAT_SITE_NAME = Column(String, comment='CRITICAL_HABITAT_SITE_NAME is the name of a critical '
                                                        'habitat site as defined in the federal recovery document; '
                                                        'e.g., Kilpoola.')
    CRITICAL_HABITAT_DETAIL = Column(String, comment='CRITICAL_HABITAT_DETAIL is the level of detail of critical'
                                                     ' habitat polygon; e.g., Detailed polygon or Grid square. '
                                                     'Grid squares are used when detailed polygons contain '
                                                     'sensitive information that cannot be released.')
    CRITICAL_HABITAT_VARIANT = Column(String, comment='CRITICAL_HABITAT_VARIANT is the sub-type of critical'
                                                      ' habitat, if applicable; e.g. Regeneration.')
    CRITICAL_HABITAT_APPROACH = Column(String, comment='CRITICAL_HABITAT_APPROACH is the scale at which the '
                                                       'polygons were defined and refers to processes within '
                                                       'the Critical Habitat Toolbox policy; e.g.,'
                                                       ' Landscape, Area or Site.')
    CRITICAL_HABITAT_METHOD = Column(String, comment='CRITICAL_HABITAT_METHOD is a broad description of how '
                                                     'the critical habitat was identified and refers to processes '
                                                     'within the Critical Habitat Toolbox policy; e.g.,'
                                                     ' Critical Function Zone.')
    AREA_HECTARES = Column(Float, comment='AREA_HECTARES is the area calculated in hectares at source data'
                                          ' which is in Lambert Conic Conformal. E.g., 14430833.7926')
    LAND_TENURE = Column(String, comment='LAND_TENURE is the status of federal crown ownership of the land;'
                                         ' e.g., Federal or Non-federal.')
    CRITICAL_HABITAT_COMMENTS = Column(String, comment='CRITICAL_HABITAT_COMMENTS are notes about the critical'
                                                       ' habitat or specific polygon; e.g., Polygons were '
                                                       'identified as part of a multispecies recovery plan.')
    CRITICAL_HABITAT_DATE_EDITED = Column(DateTime, comment='CRITICAL_HABITAT_DATE_EDITED is the date that '
                                                            'the polygon was last edited; e.g., 8/21/2014.')
    PROVINCE_TERRITORY = Column(String, comment='PROVINCE_TERRITORY is the province or territory in which'
                                                ' the critical habitat occurs; e.g., British Columbia.')
    FEDERAL_DEPARTMENT_NAME = Column(String, comment='FEDERAL_DEPARTMENT_NAME is the Federal department or '
                                                     'agency that published the recovery strategy or action'
                                                     ' plan in which the critical habitat is identified,'
                                                     ' and maintains the data; e.g., Canadian Wildlife Service, '
                                                     '‘Parks Canada Agency’.')
    UTM_ZONE = Column(Float, comment='UTM_ZONE is a segment of the Earths surface 6 degrees of longitude '
                                     'in width. The zones are numbered eastward starting at the meridian '
                                     '180 degrees from the prime meridian at Greenwich. There are five zones'
                                     ' numbered 7 through 11 that cover British Columbia, e.g., Zone 10 with '
                                     'a central meridian at -123 degrees.')
    UTM_EASTING = Column(Float, comment='UTM EASTING is the distance in meters of the polygon centroid '
                                        'eastward to or from the central meridian of a UTM zone with a '
                                        'false easting of 500000 meters. E.g., 532538')
    UTM_NORTHING = Column(Float, comment='UTM NORTHING is the distance in meters of the polygon '
                                         'centroidnorthward from the equator. e.g., 5747966')
    LATITUDE = Column(Float, comment='LATITUDE is the geographic coordinate, in decimal degrees '
                                     '(dd.dddddd), of the location of the feature as measured from '
                                     'the equator, e.g., 55.323653')
    LONGITUDE = Column(Float, comment='LONGITUDE is the geographic coordinate, in decimal degrees'
                                      ' (ddd.dddddd), of the location of the feature as measured from '
                                      'the prime meridian, e.g., -123.093544')
    SHAPE = Column(Geometry(srid=4326), comment='SHAPE is the column used to reference the spatial coordinates'
                   ' defining the feature.')
    OBJECTID = Column(Integer, comment='OBJECTID is a column required by spatial layers that interact'
                                       ' with ESRI ArcSDE. It is populated with unique values automatically by SDE.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE ANNO CAD DATA is a binary column used by spatial tools '
                                             'to store annotation, curve features and CAD data when using the '
                                             'SDO_GEOMETRY storage data type.')
    FEATURE_AREA_SQM = Column(Float, comment='')
    FEATURE_LENGTH_M = Column(Float, comment='')
