export const streamDataHeaders = {
  groundwater_wells: [
    { text: 'Well Tag No.', value: 'WELL_TAG_NUMBER' },
    { text: 'Plate number', value: 'WELL_IDENTIFICATION_PLATE_NO' },
    { text: 'Well use', value: 'WELL_USE_NAME' },
    { text: 'Depth drilled', value: 'DEPTH_WELL_DRILLED' },
    { text: 'Yield', value: 'YIELD_VALUE' },
    { text: 'Yield Units', value: 'YIELD_UNIT_DESCRIPTION' }
  ],
  water_rights_licences: [
    { text: 'Licence number', value: 'LICENCE_NUMBER' },
    { text: 'POD number', value: 'POD_NUMBER' },
    { text: 'POD subtype', value: 'POD_SUBTYPE' },
    { text: 'Purpose use', value: 'PURPOSE_USE' },
    { text: 'Quantity', value: 'QUANTITY' }
  ],
  water_rights_applications: [
    { text: 'Job Number', value: 'APPLICATION_JOB_NUMBER' },
    { text: 'Status', value: 'APPLICATION_STATUS' },
    { text: 'File number', value: 'FILE_NUMBER' },
    { text: 'POD subtype', value: 'POD_SUBTYPE' },
    { text: 'Quantity Max', value: 'QTY_DIVERSION_MAX_RATE' },
    { text: 'Quantity Units', value: 'QTY_UNITS_DIVERSION_MAX_RATE' }
  ],
  ecocat_water_related_reports: [
    { text: 'Report Id', value: 'REPORT_ID' },
    { text: 'Title', value: 'TITLE' },
    { text: 'Description', value: 'SHORT_DESCRIPTION' },
    { text: 'Author', value: 'AUTHOR' },
    { text: 'Date Published', value: 'DATE_PUBLISHED' }
  ],
  aquifers: [
    { text: 'Aquifer Tag', value: 'AQ_TAG' },
    { text: 'Name', value: 'AQUIFER_NAME' },
    { text: 'Area', value: 'AREA' },
    { text: 'Demand', value: 'DEMAND' }
  ],
  critical_habitat_species_at_risk: [
    { text: 'Scientific Name', value: 'SCIENTIFIC_NAME' },
    { text: 'Common Name', value: 'COMMON_NAME_ENGLISH' },
    { text: 'Habitat Name', value: 'CRITICAL_HABITAT_SITE_NAME' },
    { text: 'Habitat Status', value: 'CRITICAL_HABITAT_STATUS' },
    { text: 'Area Hectares', value: 'AREA_HECTARES' }
  ],
  water_allocation_restrictions: [
    { text: 'Primary Res. Code', value: 'PRIMARY_RESTRICTION_CODE' },
    { text: 'Gnis Name', value: 'GNIS_NAME' }
  ],
  hydrometric_stream_stations: [
    { text: 'Station Number', value: 'station_number' }
  ]
}
