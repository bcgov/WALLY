# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, Float, func
from app.db.base_class import BaseLayerTable
from typing import Optional, List
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Session
from geojson import Point, Feature, FeatureCollection

from logging import getLogger
logger = getLogger("groundwater_wells")


class GroundWaterWells(BaseLayerTable):
    __tablename__ = 'ground_water_wells'

    WELL_TAG_NO = Column(String, primary_key=True, comment='WELL TAG NO is the unique number of the '
                                                           'groundwater well as assigned '
                                                           'by the Province of British Columbia')
    OBJECTID = Column(Integer, comment='OBJECTID is a required attribute of feature classes and object classes in '
                                       'a GeoDatabase. This attribute is added to a SDE layer that was not previously '
                                       'created as part of a GeoDatabase but is now being registered '
                                       'with a GeoDatabase.')
    SOURCE_ACCURACY = Column(String, comment='SOURCE ACCURACY is a groundwater well locations are identified '
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
                                             '1:50,000 NTS mapping. Accuracy is +/- 200 metres.')
    GEOMETRY = Column(Geometry, comment='GEOMETRY is a ArcSDE spatial column.')
    FCODE = Column(String, comment='FCODE feature code is most importantly a means of linking a feature to its '
                                   'name and definition. For example, the code GB15300120 on a digital geographic '
                                   'feature links it to the name "Lake - Dry" with the definition "A lake bed from '
                                   'which all water has drained or evaporated." The feature code does NOT mark when '
                                   'it was digitized, what dataset it belongs to, how accurate it is, what it '
                                   'should look like when plotted, or who is responsible for updating it. It '
                                   'only says what it represents in the real world. It also doesnt even matter '
                                   'how the lake is represented. If it is a very small lake, it may be stored as '
                                   'a point feature. If it is large enough to have a shape at the scale of data '
                                   'capture, it may be stored as an outline, or a closed polygon. The same feature '
                                   'code still links it to the same definition.')
    WELL_ID = Column(Integer, comment='WELL ID is a unique identifier for the table.')
    WELL_LOCATION = Column(String, comment='WELL LOCATION is a location description used in the MS-Access application.')
    WELL_SEQUENCE_NO = Column(Integer, comment='WELL SEQUENCE NO is a number which describes the order a '
                                               'particular well islocated in a particular BCGS grid square. '
                                               'For example the well 082L042321 #1is the first well located in '
                                               'BCGS grid 082L042321. Before a system generatednon-intelligent '
                                               'WELL TAG NUMBER was in use this is how particular wells werenamed.')
    WELL_IDENTIFICATION_PLATE_NO = Column(Integer, comment='The Groundwater Protection Regulation of the Water Act '
                                                           'requires a WELL IDENTIFICATION PLATE NO for water supply '
                                                           'system wells and new and altered water supply wells.'
                                                           ' WLAP produces these aluminum plates with a unique number '
                                                           'for each plate. These plates are attached to the pump'
                                                           ' house or well by the drillers. Existing wells can have '
                                                           'these plates attached after the fact, especially if any'
                                                           ' lab samples or other information is being collected '
                                                           'about the well.')
    WATER_UTILITY_FLAG = Column(String, comment='WATER UTILITY FLAG is some wells belong to water utilities for '
                                                'provision of water to their.')
    WATER_SUPPLY_WELL_NAME = Column(String, comment='The WATER SUPPLY WELL NAME is the Utilitys name for this well. '
                                                    'This is used when the well is owned by a Utility under the '
                                                    'Water Act. The Utility has applied and been granted a licence '
                                                    'to be a Water Supply Purveyor. This data is only filled in '
                                                    'when the well is owned by a Utility. E.g. Parksville Water '
                                                    'Utility calls one of its wells "Roberts Road Well No. 5"')
    WELL_TAG_NUMBER = Column(Integer, comment='WELL TAG NUMBER is an unique business well identifier.')
    WATER_SUPPLY_SYSTEM_NAME = Column(String, comment='The WATER SUPPLY SYSTEM NAME is the name of a Utility '
                                                      'under the Water Act. The Utility has applied and been '
                                                      'granted a licence to be a Water Supply Purveyor. This data'
                                                      ' is only filled in when the well is owned by a Utility.'
                                                      ' E.g. Parksville Water Utility.')
    OBSERVATION_WELL_NUMBER = Column(Integer, comment='The OBSERVATION WELL NUMBER exists when a well has been '
                                                      'selected for monitoring. An Observation well will have water '
                                                      'level readings recorded to track groundwater levels.')
    AQUIFER_LITHOLOGY_CODE = Column(String, comment='AQUIFER LITHOLOGY CODE is an aquifer lithology identifier, '
                                                    'enables lithology layers to be indentified by a short reference.')
    WATER_DEPTH = Column(Integer, comment='WATER DEPTH, how far down the well before water is reached.')
    ARTESIAN_FLOW_VALUE = Column(Integer, comment='The ARTESIAN FLOW VALUE is the Artesian water flow measurement of'
                                                  ' the flow that occurs naturally due to inherent water pressure'
                                                  ' in the WELL. The measurement is in ARTESIAN FLOW UNITS.')
    BCGS_ID = Column(Integer, comment='BCGS ID is an internal ID to track creation of unique business BCGS number.')
    WATERSHED_CODE = Column(String, comment='WATERSHED CODE is a watershed identifier, uniquely identifies '
                                            'a water shed.')
    BCGS_NUMBER = Column(String, comment='The BCGS NUMBER is used by the Mapsheets which are based on the British'
                                         ' Columbia Geographic System (BCGS) number scheme. The mapsheet number '
                                         'is added to the well record after the well record has been added '
                                         'in the system.')
    BEDROCK_DEPTH = Column(Integer, comment='The BEDROCK DEPTH captures the depth at which bedrock starts.')
    CERTIFICATION = Column(String, comment='CERTIFICATION can be used to collect water WELL certificate information.'
                                           ' Not currently being used.')
    CHEMISTRY_LAB_DATA = Column(String, comment='Chemistry lab data exists. (flag), lab data exists usually tied '
                                                'to chemistry site id.')
    CHEMISTRY_SITE_ID = Column(String, comment='Chemistry site ID number, assigned by water EMS (environmental '
                                               'managment ssytem)')
    CLASS_OF_WELL = Column(String, comment='The CLASS OF WELL is a classification defined in the Groundwater '
                                           'Protection Regulation of the Water Act. The classes are : Water Supply,'
                                           ' Monitoring, Recharge / Injection, Dewatering / Drainage,'
                                           ' Remediation, Geotechnical.')
    UTM_NORTH = Column(Float, comment='The UTM NORTH attribute stored in the spatial database and associated '
                                      'with the WELL TAG NUMBER coordinated.')
    CONSTRUCTION_END_DATE = Column(DateTime, comment='CONSTRUCTION END DATE is the date when WELL construction'
                                                     ' was complete, defaults to date the well record was'
                                                     ' added to the system.')
    CONSTRUCTION_METHOD_CODE = Column(String, comment='The WELL CONSTRUCTION METHOD is the method of drilling '
                                                      'the Well.The construction methods are :'
                                                      ' DUG, DRILLED, DRIVING, JETTING, SPRING or OTHER.')
    CONSTRUCTION_METHOD_NAME = Column(String, comment='The CONSTRUCTION METHOD NAME is the method of '
                                                      'constructing the well. Example DRILLED indicates a drill'
                                                      ' rig was used to construct the well. Indicates the industry '
                                                      'trends in well construction methods.')
    CONSTRUCTION_START_DATE = Column(DateTime, comment='CONSTRUCTION START DATE is the date when WELL'
                                                       ' construction was started.')
    CONSULTANT_COMPANY = Column(String, comment='CONSULTANT COMPANY is a description of consulting company '
                                                'hired by owner to locate well site.')
    CONTRACTOR_INFO_1 = Column(String, comment='CONTRACTOR_ INFO 1 is MS Access Support for information field.')
    CONTRACTOR_INFO_2 = Column(String, comment='CONTRACTOR_ INFO 2 is MS Access Support for information field.')
    CONTRACTOR_WELL_PLATE_NMBR = Column(String, comment='CONTRACTOR WELL PLATE NMBR is that the Contractor '
                                                        'may assign well plate number to a WELL. If the'
                                                        ' driller uses one of the WLAP identification plate,'
                                                        ' then this number may be the same as the '
                                                        'WELL_IDENTIFICATION_PLATE_NO. Sometimes drillers have their '
                                                        'own plates made up and this number is different.')
    COORDINATE_X = Column(String, comment='COORDINATE X is an old three parameter coordinate system (arbitraty)'
                                          ' supported for old maps with well data.')
    COORDINATE_Y = Column(String, comment='COORDINATE Y is an old three parameter coordinate system (arbitraty)'
                                          ' supported for old maps with well data.')
    COORDINATE_Z = Column(String, comment='COORDINATE Z is an old three parameter coordinate system (arbitraty) '
                                          'supported for old maps with well data.')
    CREW_DRILLER_NAME = Column(String, comment='The CREW DRILLER NAME is the first and last name of a certified '
                                               'water well Driller.')
    UTM_EAST = Column(Float, comment='The UTM EAST attribute stored in the spatial database and associated with '
                                     'the WELL TAG NUMBER coordinated.')
    CREW_HELPER_NAME = Column(String, comment='CREW HELPER NAME is the name of Driller Helper.')
    DATE_ENTERED = Column(DateTime, comment='DATE ENTERED is automatically updated when a new well record is '
                                            'added to the system.')
    DEPTH_WELL_DRILLED = Column(Integer, comment='DEPTH WELL DRILLED is the finished Well depth, represented '
                                                 'in units of feet bgl (below ground level).')
    DEVELOPMENT_HOURS = Column(Integer, comment='DEVELOPMENT HOURS is the total hours devoted to develop WELL '
                                                '(develop in this means enabling production of water).')
    DEVELOPMENT_NOTES = Column(String, comment='DEVELOPMENT NOTES is the additional notes regarding well'
                                               ' development effort.')
    DIAMETER = Column(String, comment='DIAMETER is a well diameter, represented in units of inches.')
    DRILLER_COMPANY_CODE = Column(String, comment='DRILLER COMPANY CODE is a numeric code for identified'
                                                  ' driller company name.')
    DRILLER_COMPANY_NAME = Column(String, comment='The DRILLER COMPANY NAME is the compant Drillers work'
                                                  ' for, if they work for a company.')
    DRILLER_WELL_ID = Column(Integer, comment='MS-Access defined WATER WELL ID, used during upload into '
                                              'MS-Access application')
    ELEVATION = Column(Integer, comment='The ELEVATION is the elevation above sea level in feet of the'
                                        ' ground surface at the WELL.')
    FIELD_LAB_DATA = Column(String, comment='The FIELD LAB DATA indicates there is Chemistry field data '
                                            '(flag), field chemistry information kept in a paper copy. '
                                            'Y - yes there is field data. N - No there is no field data.')
    GENERAL_REMARKS = Column(String, comment='GENERAL REMARKS is the general water well comment.')
    GRAVEL_PACKED_FLAG = Column(String, comment='GRAVEL PACKED FLAG indicated whether or not a gravel pack'
                                                ' was applied during the creation of the WELL.')
    GRAVEL_PACKED_FROM = Column(Integer, comment='GRAVEL PACKED FROM indicates whether or not degree gravel'
                                                 ' dispersed around WELL site.')
    GRAVEL_PACKED_TO = Column(Integer, comment='GRAVEL PACKED TO indicates whether or not degree gravel '
                                               'dispersed around WELL site.')
    GROUND_WATER_FLAG = Column(String, comment='GROUND WATER FLAG indicates if a ground water report exists or not.')
    INDIAN_RESERVE = Column(String, comment='INDIAN RESERVE is the additional parcels identifiers for land '
                                            'in B.C. include Legal Indian Reserve.')
    INFO_OTHER = Column(String, comment='INFO OTHER is the additional information has been captured about '
                                        'this WELL that is significant.')
    INFO_SITE = Column(String, comment='The INFO SITE is additional site information, backward compatible'
                                       ' attribute to capture legacy site information.')
    LATITUDE = Column(Float, comment='Latitude coordinate, used to locate a WELL, alternative location method to UTM.')
    LEGAL_BLOCK = Column(String, comment='LEGAL BLOCK is the additional parcels identifiers for land in B.C. '
                                         'include Legal block.')
    LEGAL_DISTRICT_LOT = Column(String, comment='The LEGAL DISTRICT LOT is part of the legal description of'
                                                ' the land the well is located on. Example 2514S')
    LEGAL_LAND_DISTRICT_CODE = Column(String, comment='The LEGAL_LAND_DISTRICT_CODE represent Parcels of land '
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
                                                      '58 Wellington 59 Yale (YDYD).')
    LEGAL_LAND_DISTRICT_NAME = Column(String, comment='The LEGAL LAND DISTRICT NAME is part of the legal description'
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
                                                      'Saanich Texada Island Victoria Wellington Yale (YDYD)')
    UTM_ACCURACY_CODE = Column(String, comment='UTM ACCURACY CODE is a description of how accurate the UTM coordinate '
                                               'position is. Also implies scale to the coordinate.Codes are numeric '
                                               '01 etc.... 01 - less than 3 metres margin of error 02 - 3-10 metres'
                                               ' margin of error 03 - 10-30 metres margin of error 04 - 30-100 '
                                               'metres margin of error 1:25 000 scale 05 - 100-300 metres margin '
                                               'of error 1:50 000 scale 06 - 300-1000 metres margin of error '
                                               '1:125 000 scale 07 - 1000-3000 metres margin of error 1:250 000 '
                                               'scale 08 - 3000-10 000 metres margin of error 09 - well location '
                                               'is unknown 10 - UTM Zone 10 from 1:50 000 scale 30-100 metres moe.'
                                               ' 11 - UTM Zone 11 from 1:50 000 scale 30-100 metres.')
    LEGAL_MISCELLANEOUS = Column(String, comment='LEGAL MISCELLANEOUS is the additional legal land information.')
    LEGAL_PLAN = Column(String, comment='LEGAL PLAN is the parcels of land in B.C. can be identifed by the '
                                        'combination of Lot, Legal Land District and Plan # identifiers. This '
                                        'attribute consists of the Legal Plan to help identify the property where '
                                        'the WELL is located.')
    LEGAL_RANGE = Column(String, comment='LEGAL RANGE is the additional parcels identifiers for land in B.C. '
                                         'include legal range.')
    LEGAL_SECTION = Column(String, comment='LEGAL SECTION is the additional parcels identifiers for land in '
                                           'B.C. include Legal section.')
    LEGAL_TOWNSHIP = Column(String, comment='LEGAL TOWNSHIP is the additional parcels identifiers for land in'
                                            ' B.C. include Legal township.')
    LITHOLOGY_DESCRIPTION_COUNT = Column(String, comment='LITHOLOGY DESCRIPTION COUNT is the number of'
                                                         ' Lithology layers identified.')
    LITHOLOGY_FLAG = Column(String, comment='The LITHOLOGY FLAG indictates if there is Lithology data '
                                            'available for the well. Y - yes the soil and subsurface '
                                            'material types have been documented.N - the lithology is '
                                            'not documented.')
    LITHOLOGY_MEASURMENT_UNIT = Column(String, comment='LITHOLOGY MEASURMENT UNIT is the aquifer '
                                                       'lithology measurement units (inches,, feet) used to '
                                                       'refence the lithology layers associated with the WELL.')
    LOCATION_ACCURACY = Column(String, comment='LOCATION ACCURACY is the estimated location accuracy. '
                                               'The values for this field range from 1 through 5. The number '
                                               '5 represents the most accurate estimate. The LOC ACCURACY CODE'
                                               ' is a number 1 to 5 that indicates the scale of map the location '
                                               'is derived from. Example, 5 is a 1:50,000 map. There is another '
                                               'scale that is used, with values A - well cards to cadastre or'
                                               ' GPS +- 10m; B - 1:5000 maps +- 20m; C - 1:20,000 maps +-50m; '
                                               'D-old Dept of L,F WR maps or well cards without cadastre +-'
                                               ' 100m; E - 1:50,000 maps +- 200m;F - CDGPS differential GPS +- 1m.')
    LOC_ACCURACY_CODE = Column(String, comment='The LOC ACCURACY CODE is a number that indicates the scale of '
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
                                               'topographic maps of 1:25 000 scale. 5 100-300 metres margin of error.')
    LONGITUDE = Column(Float, comment='Longitude coordinate, used to locate a WELL, alternative '
                                      'location method to UTM.')
    LOT_NUMBER = Column(String, comment='LOT NUMBER is the parcels of land in B.C. can be identifed by the '
                                        'combination of Lot, Legal Land District and Map # identifiers. '
                                        'This attribute consists of the Lot to help identify the property '
                                        'where the WELL is located.')
    MERIDIAN = Column(String, comment='The MERIDIAN indicates if the location of the well is east or west of '
                                      'the 6th meridian which runs North-South.The meridian is part of a legal'
                                      ' description for land in British Columbia. Example W6TH - the well is west '
                                      'of the 6th meridian.')
    MINISTRY_OBSERVATION_WELL_STAT = Column(String, comment='MINISTRY OBSERVATION WELL STAT is the ministry of'
                                                            ' Water Land and Air Protection, formerly (Ministry '
                                                            'of Environment) observation.')
    MS_ACCESS_NUM_OF_WELL = Column(String, comment='The MS ACCESS NUM OF WELL is the sequence of the wells '
                                                   'entered by a driller in the MS Access Drilling '
                                                   'Data Capture System.')
    OLD_MAPSHEET = Column(String, comment='OLD_MAPSHEET is an identifer, used to track changes to the well location.')
    OLD_WELL_NUMBER = Column(String, comment='Old well number, used to track wells on old-style well maps '
                                             'using X,,Y,Z and old three parameter arbritrary coordinate '
                                             'system. (required to support old maps with well data)')
    OTHER_CHEMISTRY_DATA = Column(String, comment='OTHER CHEMISTRY DATA is the reference for additional '
                                                  'sources of chemistry data.')
    OTHER_EQUIPMENT = Column(String, comment='OTHER EQUIPMENT is the description of other equipment used '
                                             'to create the WELL.')
    OTHER_INFORMATION = Column(String, comment='OTHER INFORMATION is the brief description of other well '
                                               'data available.')
    OWNERS_WELL_NUMBER = Column(String, comment='OWNERS WELL NUMBER is the local WELL number applied by '
                                                'owner for internal tracking.')
    OWNER_ID = Column(Integer, comment='OWNER ID is an owner Identification, uniqely identifies a WELL owner.')
    SURNAME = Column(String, comment='SURNAME is the last Name of WELL owner.')
    PERFORATION_FLAG = Column(String, comment='The PERFORATION FLAG indicates if the steel casing has been '
                                              'perforated by a hydraulic shear. Perforations improve flow to '
                                              'the bottom of the well. Some wells have been perforated rather '
                                              'than having a screen installed. Perforations do not consider '
                                              'soil size. Y- yes there are holes in the casing.'
                                              ' N- no additional holes in casing.')
    PERMIT_NUMBER = Column(String, comment='The PERMIT NUMBER is used if permit numbers are issued to drill a WELL.')
    PID = Column(Integer, comment='PID is a parcel Identifier, identifes parcel where well is located.')
    PLATE_ATTACHED_BY = Column(String, comment='The PLATE ATTACHED BY is the name of the person who attached '
                                               'the WELL IDENTIFICATION PLATE. The Groundwater Protection '
                                               'Regulation of the Water Act requires this information for water'
                                               ' supply system wells and new and altered water supply wells.')
    PRODUCTION_TIDAL_FLAG = Column(String, comment='PRODUCTION TIDAL FLAG indicates if production well rates are'
                                                   ' influenced by tidal activity or not.')
    PUMP_DESCRIPTION = Column(String, comment='PUMP DESCRIPTION is an information, including if a pump exists or not.')
    PUMP_FLAG = Column(String, comment='PUMP FLAG indicates if a pump is being used on the WELL or not.')
    REPORTS_FLAG = Column(String, comment='The REPORTS FLAG indicates if there is a report on the National '
                                          'Topographical System (NTS) filing system or the utility files(which '
                                          'are reports submitted in support of an application for a certificate '
                                          'of PUBLIC CONVENIENCE AND NECESSITY). Y yes Well Report(s) Exist . '
                                          'N - no reports exist')
    RIG_NUMBER = Column(String, comment='RIG NUMBER is the number asscociated with the drilling rig. '
                                        'Supplied by the Driller.')
    QUARTER = Column(String, comment='QUARTER is the additional parcels identifiers for land in B.C. '
                                     'include Legal quarter.')
    SCREEN_FLAG = Column(String, comment='SCREEN FLAG depicts the use of a screen(s) in a WELL. Indicates '
                                         'at least 1 SCREEN record is associated with the WELL record.')
    SCREEN_INFORMATION_TEXT = Column(String, comment='SCREEN INFORMATION TEXT is the additional information '
                                                     'regarding the screen.')
    SCREEN_LENGTH = Column(String, comment='The SCREEN LENGTH is the total length of the screen assembly, '
                                           'including blanks and risers. (feet) . Most screens are '
                                           'cylindrical in shape.')
    SCREEN_MANUFACTURER = Column(String, comment='The SCREEN MANUFACTURER identifies who made the screen.')
    SCREEN_WIRE = Column(String, comment='The SCREEN WIRE is the type of screen wire. The wire has different'
                                         ' cross sections - like WIRE WOUND (round) or V WIRE WOUND (triangular). '
                                         'The wire is what some screens are made of.')
    SEQUENCE_NO = Column(Float, comment='SEQUENCE_NO is a number which describes the order a particular well '
                                        'islocated in a particular BCGS grid square. For example the well'
                                        ' 082L042321 #1is the first well located in BCGS grid 082L042321. '
                                        'Before a system generatednon-intelligent WELL TAG NUMBER was in use'
                                        ' this is how particular wells werenamed.')
    SIEVE_FLAG = Column(String, comment='SIEVE FLAG indicates if Sieve Analysis was done or not, default was'
                                        ' blank field for No.')
    SITE_AREA = Column(String, comment='The SITE AREA is the town or nearest describable geogropahic area.')
    SITE_FLAG = Column(String, comment='SITE_FLAG indicated whether site inspection was done or not.')
    SITE_ISLAND = Column(String, comment='The SITE ISLAND is the island name, if the well is located on an Island.')
    SITE_STREET = Column(String, comment='The SITE STREET is the Well location, address (well) description of '
                                         'where well is outside additional well information')
    SURFACE_SEAL_DEPTH = Column(Integer, comment='The SURFACE SEAL DEPTH indicates depth of surface seal which '
                                                 'is depth in feet below ground surface to bottom of Surface Seal.')
    SURFACE_SEAL_FLAG = Column(String, comment='The SURFACE SEAL FLAG indicates if a surface seal was applied '
                                               'upon completion of WELL.Y- yes surface seal was constructed. N- '
                                               'no surface seal was applied. Blank is unknown')
    SURFACE_SEAL_THICKNESS = Column(Integer, comment='The SURFACE SEAL THICKNESS is the thickness of the '
                                                     '"surface seal" which is a sealant placed in the annular '
                                                     'space around the outside of the outermost well casing and '
                                                     'between multiple well casings and extending to or just below '
                                                     'the ground surface. Good practice is a sealant with a minimum '
                                                     'thickness of 1 inch, minumum length of 15 feet and extending '
                                                     'a minimum of 3 feet into bedrock.')
    TYPE_OF_RIG = Column(String, comment='Type of RIG (drilling hardware) used during the creation of the WELL.')
    TYPE_OF_WORK = Column(String, comment='TYPE OF WORK is the legacy attribute contained in MS-Access application. '
                                          'Values include NEW or DPD.')
    WELL_USE_CODE = Column(String, comment='WELL USE CODE is three letter character unique code to identify code.')
    WELL_USE_NAME = Column(String, comment='The WELL USE NAME is the long well use name. Examples may include '
                                           'private, commercial, domestic.')
    WHEN_CREATED = Column(DateTime, comment='WHEN CREATED is the date and time the entry was created.')
    WHEN_UPDATED = Column(DateTime, comment='WHEN UPDATED is the date and time the entry was last modified.')
    WHERE_PLATE_ATTACHED = Column(String, comment='The WHERE PLATE ATTACHED is a description of where the '
                                                  'indentification plate has been attached. The Groundwater '
                                                  'Protection Regulation of the Water Act requires this information'
                                                  ' for water supply system wells and new and altered '
                                                  'water supply wells.')
    WHO_CREATED = Column(String, comment='WHO CREATED is the unique id of the user who created this entry.')
    WHO_UPDATED = Column(String, comment='WHO UPDATED is the unique id of the user who last modified this entry.')
    YIELD_UNIT_CODE = Column(String, comment='YIELD UNIT CODE is the yield unit of measure, unique code. '
                                             'The MS-Access database expects flow rates to be entered as USgpm.')
    YIELD_UNIT_DESCRIPTION = Column(String, comment='YIELD UNIT DESCRIPTION is the yield measurement description, '
                                                    'if other yield units become supported or if a conversion factor '
                                                    'is required it could be entered in this attribute.')
    YIELD_VALUE = Column(Float, comment='YIELD VALUE is the well yield value, measured water yield ammount, '
                                        'estimate how much water flow a WELL is capable of sustaining.')
    WELL_LICENCE_GENERAL_STATUS = Column(String, comment='A text value reflects the generalized status of '
                                                         'authorizations on the given well. It value will be '
                                                         'set based on the contents of the AUTHORIZATION STATUS '
                                                         'attribute coming from eLicensing application via a trigger'
                                                         ' implemented on WELL_LICENCE Table.Acceptable '
                                                         'Values are:a) UNLICENSEDb) LICENSEDc) HISTORICAL.')
    WELL_DETAIL_URL = Column(String, comment='A HTTP URL link value that contains the Well Tag Number, specifying'
                                             ' a direct link to the WELL record in WELLS Public application.')
    SE_ANNO_CAD_DATA = Column(BYTEA, comment='SE_ANNO_CAD_DATA is a binary column used by spatial tools to '
                                             'store annotation, curve features and CAD data when using the '
                                             'SDO_GEOMETRY storage data type.')
