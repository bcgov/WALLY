export const DATA_CAN_CLIMATE_NORMALS_1980_2010 = 'DATA_CAN_CLIMATE_NORMALS_1980_2010'
export const HYDROMETRIC_STREAM_FLOW = 'HYDROMETRIC_STREAM_FLOW'
export const API_DATASOURCE = 'API_DATASOURCE'

export const API_URL = process.env.VUE_APP_AXIOS_BASE_URL

export const DATA_LAYERS = [
  {
    id: HYDROMETRIC_STREAM_FLOW,
    name: 'Hydrometric Stream Flow',
    type: API_DATASOURCE,
    url: `${API_URL}/api/v1/hydat`
  },
  {
    id: DATA_CAN_CLIMATE_NORMALS_1980_2010, // TODO possibly wrap this above the geojson object
    name: 'Canadian Climate Normals 1980-2010',
    type: API_DATASOURCE,
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
    ]
  }
]
