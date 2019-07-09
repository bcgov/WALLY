import L from 'leaflet'

import {
  FETCH_DATA_SOURCES,
  FETCH_MAP_OBJECT,
  FETCH_MAP_OBJECTS,
  CLEAR_MAP_SELECTIONS,
  SELECT_SINGLE_MAP_OBJECT,
  ADD_ACTIVE_MAP_LAYER,
  REMOVE_ACTIVE_MAP_LAYER
} from './actions.types'

import {
  SET_DATA_SOURCES,
  SET_MAP_OBJECT_SELECTIONS,
  SET_SINGLE_MAP_OBJECT_SELECTION,
  SET_MAP_SELECTION_OBJECTS_EMPTY,
  SET_SINGLE_MAP_SELECTION_OBJECT_EMPTY
} from './mutations.types'

import Vue from 'vue'
import Vuex from 'vuex'
import ApiService from '../../services/ApiService'
import EventBus from '../../services/EventBus.js'
import * as CONFIG from './mapConfig'

Vue.use(Vuex)

export default {
  state: {
    searchBounds: {},
    searchParams: {},
    // lastSearchTrigger: null,
    locationSearchResults: [],
    pendingSearch: null,
    searchResultFilters: {},
    pendingLocationSearch: null,
    externalDataSources: { features: [] },
    dataLayers: [
      {
        id: CONFIG.DATA_CAN_CLIMATE_NORMALS_1980_2010,
        name: 'Canadian Climate Normals 1980-2010',
        uri: '',
        geojson: ''
      }
    ],
    activeMapLayers: [],
    mapLayerSelections: [],
    mapLayerSingleSelection: { content: { properties: {} } }
  },
  mutations: {
    [SET_DATA_SOURCES] (state, payload) {
      state.externalDataSources = payload
    },
    [SET_SINGLE_MAP_OBJECT_SELECTION] (state, payload) {
      state.mapLayerSingleSelection = payload
    },
    [SET_SINGLE_MAP_SELECTION_OBJECT_EMPTY] (state, payload) {
      state.mapLayerSingleSelection = {}
    },
    [SET_MAP_OBJECT_SELECTIONS] (state, payload) {
      state.mapLayerSelections.push(payload)
    },
    [SET_MAP_SELECTION_OBJECTS_EMPTY] (state, payload) {
      state.mapLayerSelections = []
    },
    [ADD_ACTIVE_MAP_LAYER] (state, payload) {
      state.activeMapLayers.push(
        CONFIG.MAP_LAYERS.find(function (obj) {
          return obj.id === payload
        })
      )
      EventBus.$emit(`layer:added`, payload)
    },
    [REMOVE_ACTIVE_MAP_LAYER] (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter(function (obj) {
        return obj.id !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    }
  },
  actions: {
    [SELECT_SINGLE_MAP_OBJECT] ({ commit }, payload) {
      commit(SET_SINGLE_MAP_OBJECT_SELECTION, payload)
    },
    [CLEAR_MAP_SELECTIONS] ({ commit }) {
      commit(SET_MAP_SELECTION_OBJECTS_EMPTY)
    },
    [FETCH_MAP_OBJECT] ({ commit }, payload) {
      let params = {
        service: 'WFS',
        version: '2.0.0',
        request: 'GetFeature',
        typeNames: 'namespace:featuretype',
        featureID: payload,
        info_format: 'application/json'
      }
      commit(SET_SINGLE_MAP_SELECTION_OBJECT_EMPTY)
      ApiService.getRaw('https://openmaps.gov.bc.ca/geo/pub/' + payload.layer + '/ows' + L.Util.getParamString(params))
        .then((response) => {
          console.log(response.data)
          commit(SET_SINGLE_MAP_OBJECT_SELECTION, response.data)
        }).catch((error) => {
        console.log(error)
      })
    },
    [FETCH_MAP_OBJECTS] ({ commit }, payload) {
      let params = {
        request: 'GetMap',
        service: 'WMS',
        srs: 'EPSG:4326',
        version: '1.1.1',
        format: 'application/json;type=topojson',
        bbox: payload.bounds,
        height: payload.size.y,
        width: payload.size.x,
        layers: payload.layer
      }
      commit(SET_MAP_SELECTION_OBJECTS_EMPTY)
      ApiService.getRaw('https://openmaps.gov.bc.ca/geo/pub/' + payload.layer + '/ows' + L.Util.getParamString(params))
        .then((response) => {
          console.log(response.data)
          let points = response.data.objects[params.layers].geometries
          console.log(points)
          commit(SET_MAP_OBJECT_SELECTIONS, { [payload.layer]: points })
        }).catch((error) => {
          console.log(error)
        })
    },
    // [FETCH_WELL_LOCATIONS] ({ commit }) {
    //     return new Promise((resolve, reject) => {
    //         ApiService.getRaw("https://gwells-staging.pathfinder.gov.bc.ca/gwells/api/v1/locations")
    //             .then((response: { data: any; }) => {
    //                 commit(SET_LOCATION_SEARCH_RESULTS, response.data)
    //             }).catch((error: any) => {
    //             reject(error)
    //         })
    //     })
    // },
    [FETCH_DATA_SOURCES] ({ commit }) {
      // const demoData = [
      //   {
      //     id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de18',
      //     name: 'Canadian Climate Normals 1981-2010 Station Data - N VANCOUVER WHARVES',
      //     web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0',
      //     coordinates: [-123.12, 49.31]
      //   }
      // ]

      const demoDataGeoJSON = {
        type: 'FeatureCollection',
        features: [
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

      return new Promise((resolve, reject) => {
        commit(SET_DATA_SOURCES, demoDataGeoJSON)
      })
    }
  },
  getters: {
    // mapLayerIsActive (state) {
    //   return (layerId) => state.activeMapLayers.filter((e) => e.id === layerId).length > 0
    // },
    mapLayerSingleSelection (state) {
      return state.mapLayerSingleSelection
    },
    mapLayerSelections (state) {
      return state.mapLayerSelections
    },
    activeMapLayers (state) {
      return state.activeMapLayers
    },
    allLayers () {
      return CONFIG.MAP_LAYERS
    }
  }
}
