// Layer Names
export const WMS_WATER_RIGHTS_LICENSES = 'WATER_RIGHTS_LICENSES'
export const WMS_GROUND_WATER_LICENSES = 'GROUND_WATER_LICENSES'
export const WMS_ARTESIAN = 'ARTESIAN'
export const WMS_SNOW_STATIONS = 'WMS_SNOW_STATIONS'
export const WMS_CADASTRAL = 'CADASTRAL'
export const WMS_FRESH_WATER_STREAM = 'WMS_FRESH_WATER_STREAM'
export const WMS_ECOCAT = 'ECOCAT'
export const WMS_GWLIC = 'GWLIC'
export const WMS_WILD_FIRE_WEATHER_STATIONS = 'WMS_WILD_FIRE_WEATHER_STATIONS'
export const WMS_OBS_ACTIVE = 'OBS_ACTIVE'
export const WMS_OBS_INACTIVE = 'OBS_INACTIVE'
export const WMS_WELLS = 'WELLS'
export const WMS_GROUND_WATER_AQUIFERS = 'WMS_GROUND_WATER_AQUIFERS'

// Data Object Names
export const DATA_CAN_CLIMATE_NORMALS_1980_2010 = 'DATA_CAN_CLIMATE_NORMALS_1980_2010'

// Layer Configs
export const MAP_LAYERS = [
  {
    id: WMS_WATER_RIGHTS_LICENSES,
    name: 'Water Rights Licenses',
    wmsLayer: 'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
    wmsStyle: ''
  },
  {
    id: WMS_ARTESIAN,
    name: 'Artesian Wells',
    wmsLayer: 'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    wmsStyle: 'Water_Wells_Artesian'
  },
  {
    id: WMS_CADASTRAL,
    name: 'Cadastral',
    wmsLayer: 'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_SNOW_STATIONS,
    name: 'Automated Snow Weather Station Locations',
    wmsLayer: 'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_FRESH_WATER_STREAM,
    name: 'Freshwater Atlas Stream Directions',
    wmsLayer: 'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_WILD_FIRE_WEATHER_STATIONS,
    name: 'BC Wildfire Active Weather Stations',
    wmsLayer: 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_ECOCAT,
    name: 'Ecocat - Water related reports',
    wmsLayer: 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_GROUND_WATER_LICENSES,
    name: 'Ground Water Licenses',
    wmsLayer: 'WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_GROUND_WATER_AQUIFERS,
    name: 'Ground Water Aquifers',
    wmsLayer: 'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
    wmsStyle: ''
  }
]

export const LAYER_PROPERTY_MAPPINGS =
{
  'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV': 'LICENCE_NUMBER',
  'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW': 'WELL_TAG_NO',
  'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW': 'PID',
  'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP': 'LOCATION_NAME',
  'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP': 'DOWNSTREAM_DIRECTION',
  'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP': 'STATION_NAME',
  'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW': 'REPORT_POINT_ID',
  'WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW': 'WELL_TAG_NUMBER',
  'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW': 'AQUIFER_NUMBER'
}

export const LAYER_PROPERTY_NAMES = {
  'LICENCE_NUMBER': 'License No.',
  'WELL_TAG_NO': 'Well Tag No.',
  'PID': 'Parcel Identifier',
  'LOCATION_NAME': 'Location Name',
  'DOWNSTREAM_DIRECTION': 'Downstream Direction',
  'STATION_NAME': 'Station Name',
  'REPORT_POINT_ID': 'Report Point Id',
  'WELL_TAG_NUMBER': 'Well Tag No.',
  'AQUIFER_NUMBER': 'Aquifer No.'
}
