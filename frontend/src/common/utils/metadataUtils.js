export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

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
export const WMS_GROUND_WATER_WELLS = 'GROUND_WATER_WELLS'
export const WMS_GROUND_WATER_AQUIFERS = 'WMS_GROUND_WATER_AQUIFERS'
export const WMS_FRESHWATER_WATERSHEDS = 'WMS_FRESHWATER_WATERSHEDS'
export const WMS_BC_MAJOR_WATERSHEDS = 'WMS_BC_MAJOR_WATERSHEDS'

export const DATA_CAN_CLIMATE_NORMALS_1980_2010 = 'DATA_CAN_CLIMATE_NORMALS_1980_2010'
export const HYDROMETRIC_STREAM_FLOW = 'HYDROMETRIC_STREAM_FLOW'
export const API_DATAMART = 'api'
export const WMS_DATAMART = 'wms'

// Layer Configs
export const DATA_MARTS = [
  {
    id: WMS_WATER_RIGHTS_LICENSES,
    name: 'Water Rights Licenses',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.WLS_WATER_RIGHTS_LICENCES_SV',
    wmsStyle: ''
  },
  {
    id: WMS_GROUND_WATER_WELLS,
    name: 'Groundwater Wells',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_FRESHWATER_WATERSHEDS,
    name: 'Freshwater Atlas Watersheds',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY',
    wmsStyle: ''
  },
  {
    id: WMS_BC_MAJOR_WATERSHEDS,
    name: 'BC Major Watersheds',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_BASEMAPPING.BC_MAJOR_WATERSHEDS',
    wmsStyle: ''
  },
  {
    id: WMS_ARTESIAN,
    name: 'Artesian Wells',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
    wmsStyle: 'Water_Wells_Artesian'
  },
  {
    id: WMS_CADASTRAL,
    name: 'Cadastral',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_SNOW_STATIONS,
    name: 'Automated Snow Weather Station Locations',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_FRESH_WATER_STREAM,
    name: 'Freshwater Atlas Stream Directions',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_WILD_FIRE_WEATHER_STATIONS,
    name: 'BC Wildfire Active Weather Stations',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP',
    wmsStyle: ''
  },
  {
    id: WMS_ECOCAT,
    name: 'Ecocat - Water related reports',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_GROUND_WATER_LICENSES,
    name: 'Groundwater Licenses',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW',
    wmsStyle: ''
  },
  {
    id: WMS_GROUND_WATER_AQUIFERS,
    name: 'Groundwater Aquifers',
    type: WMS_DATAMART,
    wmsLayer: 'WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW',
    wmsStyle: ''
  },
  {
    id: HYDROMETRIC_STREAM_FLOW,
    name: 'Hydrometric Stream Flow',
    type: API_DATAMART,
    url: `${API_URL}/api/v1/hydat`
  },
  {
    id: DATA_CAN_CLIMATE_NORMALS_1980_2010, // TODO possibly wrap this above the geojson object
    name: 'Canadian Climate Normals 1980-2010',
    type: API_DATAMART,
    geojson: [
      {
        id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de18',
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [-123.12, 49.31]
        },
        properties: {
          name: 'Canadian Climate Normals 1981-2010 Station Data - N VANCOUVER WHARVES',
          web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0'
        }
      }
    ],
    url: `${API_URL}/api`
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
  LICENCE_NUMBER: 'License No.',
  WELL_TAG_NO: 'Well Tag No.',
  PID: 'Parcel Identifier',
  LOCATION_NAME: 'Location Name',
  DOWNSTREAM_DIRECTION: 'Downstream Direction',
  STATION_NAME: 'Station Name',
  REPORT_POINT_ID: 'Report Point Id',
  WELL_TAG_NUMBER: 'Well Tag No.',
  AQUIFER_NUMBER: 'Aquifer No.'
}

// TODO TEMPORARY USE UNTIL VECTOR LAYERS ONLY USE PK PROPERTY OR LOOKUP TABLE CREATED
export const PRIMARY_KEYS = {
  aquifers: 'AQ_TAG',
  automated_snow_weather_station_locations: 'SNOW_ASWS_STN_ID',
  bc_major_watersheds: 'OBJECTID',
  bc_wildfire_active_weather_stations: 'WEATHER_STATIONS_ID',
  cadastral: 'PARCEL_FABRIC_POLY_ID',
  critical_habitat_species_at_risk: 'CRITICAL_HABITAT_ID',
  ecocat_water_related_reports: 'REPORT_ID',
  freshwater_atlas_stream_directions: 'OBJECTID',
  freshwater_atlas_watersheds: 'WATERSHED_FEATURE_ID',
  groundwater_wells: 'WELL_TAG_NO',
  hydrometric_stream_flow: 'station_number',
  water_allocation_restrictions: 'OBJECTID',
  water_rights_licences: 'WLS_WRL_SYSID'
}
