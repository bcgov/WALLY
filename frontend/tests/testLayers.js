const testLayers = {
  layers: [{
    display_name: 'Freshwater Atlas Watersheds',
    display_data_name: 'freshwater_atlas_watersheds',
    label: 'Watershed Name',
    label_column: 'GNIS_NAME_1',
    highlight_columns: ['GNIS_NAME_1', 'GNIS_NAME_2', 'WATERSHED_TYPE', 'AREA_HA', 'RIVER_AREA', 'LAKE_AREA', 'WETLAND_AREA', 'MANMADE_AREA', 'GLACIER_AREA', 'AVERAGE_ELEVATION', 'AVERAGE_SLOPE'],
    wms_name: 'WHSE_BASEMAPPING.FWA_WATERSHEDS_POLY',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'BC Major Watersheds',
    display_data_name: 'bc_major_watersheds',
    label: 'Watershed',
    label_column: 'MAJOR_WATERSHED_SYSTEM',
    highlight_columns: ['AREA', 'PERIMETER', 'MAJOR_WATERSHED_SYSTEM', 'GEOMETRY', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M'],
    wms_name: 'WHSE_BASEMAPPING.BC_MAJOR_WATERSHEDS',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Automated Snow Weather Station Locations',
    display_data_name: 'automated_snow_weather_station_locations',
    label: 'Location',
    label_column: 'LOCATION_NAME',
    highlight_columns: ['ELEVATION', 'LATITUDE', 'LONGITUDE', 'LOCATION_NAME', 'STATUS'],
    wms_name: 'WHSE_WATER_MANAGEMENT.SSL_SNOW_ASWS_STNS_SP',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Freshwater Atlas Stream Directions',
    display_data_name: 'freshwater_atlas_stream_directions',
    label: 'Downstream Direction',
    label_column: 'DOWNSTREAM_DIRECTION',
    highlight_columns: ['LINEAR_FEATURE_ID', 'DOWNSTREAM_DIRECTION', 'FEATURE_CODE'],
    wms_name: 'WHSE_BASEMAPPING.FWA_STREAM_DIRECTIONS_SP',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'BC Wildfire Active Weather Stations',
    display_data_name: 'bc_wildfire_active_weather_stations',
    label: 'Station Name',
    label_column: 'STATION_NAME',
    highlight_columns: ['STATION_NAME', 'STATION_ACRONYM', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'INSTALL_DATE'],
    wms_name: 'WHSE_LAND_AND_NATURAL_RESOURCE.PROT_WEATHER_STATIONS_SP',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FORESTS',
    url: ''
  }, {
    display_name: 'Ecocat - Water related reports',
    display_data_name: 'ecocat_water_related_reports',
    label: 'Title',
    label_column: 'TITLE',
    highlight_columns: ['REPORT_ID', 'TITLE', 'SHORT_DESCRIPTION', 'AUTHOR', 'DATE_PUBLISHED', 'REPORT_AUDIENCE', 'LONG_DESCRIPTION'],
    wms_name: 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'REPORTS',
    url: ''
  }, {
    display_name: 'Water Allocation Restrictions',
    display_data_name: 'water_allocation_restrictions',
    label: 'Feature Id',
    label_column: 'LINEAR_FEATURE_ID',
    highlight_columns: ['PRIMARY_RESTRICTION_CODE', 'SECONDARY_RESTRICTION_CODES', 'GNIS_NAME', 'RESTRICTION_ID_LIST'],
    wms_name: 'WHSE_WATER_MANAGEMENT.WLS_STREAM_RESTRICTIONS_SP',
    wms_style: '1851',
    vector_name: '',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Critical Habitat for federally-listed species at risk (posted)',
    display_data_name: 'critical_habitat_species_at_risk',
    label: 'Habitat',
    label_column: 'CRITICAL_HABITAT_SITE_NAME',
    highlight_columns: ['SCIENTIFIC_NAME', 'COMMON_NAME_ENGLISH', 'COMMON_NAME_FRENCH', 'COSEWIC_POPULATION', 'CRITICAL_HABITAT_STATUS', 'CRITICAL_HABITAT_REGION', 'CRITICAL_HABITAT_SITE_NAME', 'CRITICAL_HABITAT_DETAIL', 'CRITICAL_HABITAT_VARIANT', 'CRITICAL_HABITAT_APPROACH', 'CRITICAL_HABITAT_METHOD', 'AREA_HECTARES', 'CRITICAL_HABITAT_COMMENTS', 'CRITICAL_HABITAT_DATE_EDITED', 'FEDERAL_DEPARTMENT_NAME'],
    wms_name: 'WHSE_WILDLIFE_MANAGEMENT.WCP_CRITICAL_HABITAT_SP',
    wms_style: '',
    vector_name: '',
    layer_category_code: 'FISH_WILDLIFE_PLANTS',
    url: ''
  }, {
    display_name: 'Hydrometric Stream Flow',
    display_data_name: 'hydrometric_stream_flow',
    label: 'Name',
    label_column: 'name',
    highlight_columns: ['', ''],
    wms_name: '',
    wms_style: '',
    vector_name: 'hydrometric_stream_flow',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Groundwater Wells',
    display_data_name: 'groundwater_wells',
    label: 'Well tag number',
    label_column: 'WELL_TAG_NUMBER',
    highlight_columns: ['WELL_TAG_NUMBER', 'WELL_IDENTIFICATION_PLATE_NO', 'WELL_LICENCE_GENERAL_STATUS', 'WELL_LOCATION', 'SITE_AREA', 'SITE_STREET', 'WELL_USE_NAME', 'YIELD_VALUE', 'YIELD_UNIT_DESCRIPTION', 'DEPTH_WELL_DRILLED', 'WELL_DETAIL_URL'],
    wms_name: '',
    wms_style: '',
    vector_name: 'groundwater_wells',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Aquifers',
    display_data_name: 'aquifers',
    label: 'Aquifer name',
    label_column: 'AQNAME',
    highlight_columns: ['AQUIFER_NUMBER', 'AQNAME', 'PERIMETER', 'AREA', 'SIZE_KM2', 'AQUIFER_MATERIALS', 'PRODUCTIVITY', 'VULNERABILITY', 'DEMAND', 'AQUIFER_CLASSIFICATION', 'AQUIFER_NAME', 'AQUIFER_RANKING_VALUE', 'DESCRIPTIVE_LOCATION', 'AQUIFER_DESCRIPTION_RPT_URL', 'AQUIFER_STATISTICS_RPT_URL', 'TYPE_OF_WATER_USE'],
    wms_name: '',
    wms_style: '',
    vector_name: 'aquifers',
    layer_category_code: 'FRESHWATER_MARINE',
    url: ''
  }, {
    display_name: 'Cadastral Parcel Information',
    display_data_name: 'cadastral',
    label: 'Pid',
    label_column: 'PID',
    highlight_columns: ['PARCEL_NAME', 'PLAN_NUMBER', 'PIN', 'PID', 'PARCEL_STATUS', 'PARCEL_CLASS', 'OWNER_TYPE', 'PARCEL_START_DATE', 'REGIONAL_DISTRICT', 'FEATURE_AREA_SQM', 'FEATURE_LENGTH_M', 'WHEN_UPDATED'],
    wms_name: '',
    wms_style: '',
    vector_name: 'cadastral',
    layer_category_code: 'LAND_TENURE',
    url: ''
  }, {
    display_name: 'Water Rights Licenses',
    display_data_name: 'water_rights_licences',
    label: 'License Number',
    label_column: 'LICENCE_NUMBER',
    highlight_columns: ['POD_STATUS', 'LICENCE_NUMBER', 'LICENCE_STATUS', 'LICENCE_STATUS_DATE', 'WELL_TAG_NUMBER', 'FILE_NUMBER', 'PURPOSE_USE', 'REDIVERSION_IND', 'QUANTITY', 'QUANTITY_UNITS', 'QTY_DIVERSION_MAX_RATE', 'HYDRAULIC_CONNECTIVITY', 'PRIMARY_LICENSEE_NAME', 'SOURCE_NAME'],
    wms_name: '',
    wms_style: '',
    vector_name: 'water_rights_licences',
    layer_category_code: 'WATER_ADMINISTRATION',
    url: ''
  }],
  categories: [{
    layer_category_code: 'LAND_TENURE',
    description: 'Land Tenure and Administrative Boundaries',
    display_order: 10
  }, {
    layer_category_code: 'FISH_WILDLIFE_PLANTS',
    description: 'Fish, Wildlife, and Plant Species',
    display_order: 20
  }, {
    layer_category_code: 'FRESHWATER_MARINE',
    description: 'Freshwater and Marine',
    display_order: 30
  }, {
    layer_category_code: 'WATER_ADMINISTRATION',
    description: 'Water Administration',
    display_order: 40
  }, {
    layer_category_code: 'REPORTS',
    description: 'Reports',
    display_order: 50
  }, {
    layer_category_code: 'FORESTS',
    description: 'Forests, Grasslands and Wetlands',
    display_order: 60
  }, {
    layer_category_code: 'AIR_CLIMATE',
    description: 'Air and Climate',
    display_order: 70
  }]
}
export default testLayers
