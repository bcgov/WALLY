import Vue from 'vue';
import Vuex from 'vuex';
import { Feature, Point, FeatureCollection } from 'geojson';

import {
    FETCH_WELL_LOCATIONS,
    FETCH_DATA_SOURCES
} from './actions.types'

import {
    SET_SEARCH_BOUNDS,
    SET_SEARCH_PARAMS,
    SET_LOCATION_SEARCH_RESULTS,
    SET_DATA_SOURCES,
    SET_MAP_LAYER_STATE,
    SET_MAP_OBJECT_SELECTIONS,
    ADD_LAYER,
    REMOVE_LAYER
} from './mutations.types'

// @ts-ignore
import EventBus from '@/services/EventBus.js'

// @ts-ignore
import ApiService from '../../services/ApiService'
import { IDataSource } from '@/interfaces';

const cleanParams = (payload: { [s: string]: unknown; } | ArrayLike<unknown>) => {
    // Clear any null or empty string values, to keep URLs clean.
    return Object.entries(payload).filter(([key, value]) => {
        return !(value === undefined || value === '' || value === null)
    }).reduce((cleanedParams, [key, value]) => {
        // @ts-ignore
        cleanedParams[key] = value
        return cleanedParams
    }, {})
}

const WMS_ARTESIAN = 'WMS_ARTESIAN'
const WMS_CADASTRAL = 'WMS_CADASTRAL'
const WMS_ECOCAT = 'WMS_ECOCAT'
const WMS_GWLIC = 'WMS_GWLIC'
const WMS_OBS_ACTIVE = 'WMS_OBS_ACTIVE'
const WMS_OBS_INACTIVE = 'WMS_OBS_INACTIVE'
const WMS_WELLS = 'WMS_WELLS'
const DATA_CAN_CLIMATE_NORMALS_1980_2010 = 'DATA_CAN_CLIMATE_NORMALS_1980_2010'

// @ts-ignore
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
                id: DATA_CAN_CLIMATE_NORMALS_1980_2010,
                name: 'Canadian Climate Normals 1980-2010',
                uri: '',
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
                            web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0',
                        }
                    },
                    {
                        id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de11',
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: [-123.19, 49.13]
                        },
                        properties: {
                            name: 'Canadian Climate Normals 1981-2010 Station Data - STEVESTON',
                            web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=869&dispBack=0',
                        }
                    }
                ]
            }
        ],
        mapLayers: [
            {   
                id: WMS_ARTESIAN,
                name: 'Artesian wells', // FIXME: artesian wells may be "covered" by the same well from the well layer.
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                wms_cfg: {
                    format: 'image/png',
                    layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                    styles: 'Water_Wells_Artesian',
                    transparent: true,
                    name: 'Artesian wells',
                    overlay: true
                }
            },
            {
                id: WMS_CADASTRAL,
                name: 'Cadastral',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows?',
                wms_cfg: {
                        format: 'image/png',
                        layers: 'pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW',
                        transparent: true,
                        name: 'Cadastral',
                        overlay: true
                    }
            },
            {
                id: WMS_ECOCAT,
                name: 'Ecocat - Water related reports',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW/ows?',
                wms_cfg: {
                        format: 'image/png',
                        layers: 'pub:WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
                        transparent: true,
                        name: 'Ecocat - Water related reports',
                        overlay: true
                    }
            },
            {
                id: WMS_GWLIC,
                name: 'Groundwater licences',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW/ows?',
                wms_cfg: {
                    format: 'image/png',
                    layers: 'pub:WHSE_WATER_MANAGEMENT.WLS_PWD_LICENCES_SVW',
                    transparent: true,
                    name: 'Groundwater licences',
                    overlay: true
                }
            },
            {
                id: WMS_OBS_ACTIVE,
                name: 'Observation wells - active',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                wms_cfg: {
                        format: 'image/png',
                        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                        styles: 'Provincial_Groundwater_Observation_Wells_Active',
                        transparent: true,
                        name: 'Observation wells - active',
                        overlay: true
                    }
            },
            {
                id: WMS_OBS_INACTIVE,
                name: 'Observation wells - inactive',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                wms_cfg: {
                        format: 'image/png',
                        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                        styles: 'Provincial_Groundwater_Observation_Wells_Inactive',
                        transparent: true,
                        name: 'Observation wells - inactive',
                        overlay: true
                    }
            },
            {
                id: WMS_WELLS,
                name: 'Wells - All',
                wms_url: 'https://openmaps.gov.bc.ca/geo/pub/WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW/ows?',
                wms_cfg: {
                        format: 'image/png',
                        layers: 'pub:WHSE_WATER_MANAGEMENT.GW_WATER_WELLS_WRBC_SVW',
                        transparent: true,
                        name: 'Wells - All',
                        overlay: true
                    }
            }
        ],
        activeMapLayers: {
            [WMS_ARTESIAN]: false,
            [WMS_CADASTRAL]: false,
            [WMS_ECOCAT]: false,
            [WMS_GWLIC]: false,
            [WMS_OBS_ACTIVE]: false,
            [WMS_OBS_INACTIVE]: false,
            [WMS_WELLS]: false,
            [DATA_CAN_CLIMATE_NORMALS_1980_2010]: false
        },
        mapLayerSelections: {
            [WMS_ARTESIAN]: [],
            [WMS_CADASTRAL]: [],
            [WMS_ECOCAT]: [],
            [WMS_GWLIC]: [],
            [WMS_OBS_ACTIVE]: [],
            [WMS_OBS_INACTIVE]: [],
            [WMS_WELLS]: [],
            [DATA_CAN_CLIMATE_NORMALS_1980_2010]: [
                {
                    id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de18',
                    name: 'Canadian Climate Normals 1981-2010 Station Data - N VANCOUVER WHARVES',
                    web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0',
                    coordinates: [-123.12, 49.31]
                }
            ]
        }
    },
    mutations: {
        [SET_SEARCH_BOUNDS] (state: { searchBounds: any; }, payload: any) {
            state.searchBounds = payload
        },
        [SET_SEARCH_PARAMS] (state: { searchParams: {}; }, payload: ArrayLike<unknown> | { [s: string]: unknown; }) {
            state.searchParams = cleanParams(payload)
        },
        [SET_LOCATION_SEARCH_RESULTS] (state: { locationSearchResults: any; }, payload: any) {
            state.locationSearchResults = payload
        },
        [SET_DATA_SOURCES] (state: { externalDataSources: any; }, payload: any) {
            state.externalDataSources = payload
        },
        [SET_MAP_LAYER_STATE] (state: { activeMapLayers: any; }, payload: { id: string, status: boolean }) {
            state.activeMapLayers[payload.id] = payload.status
            const action = payload.status ? 'added' : 'removed'
            EventBus.$emit(`layer:${action}`, payload.id) // Map.vue will listen for this event to add layers
        },
        [SET_MAP_OBJECT_SELECTIONS] (state: { mapLayerSelections: any; }, payload: any) {
            state.mapLayerSelections = payload;
        }
    },
    actions: {
        // @ts-ignore
        [FETCH_WELL_LOCATIONS] ({ commit }) {
            return new Promise((resolve, reject) => {
                ApiService.getRaw("https://gwells-staging.pathfinder.gov.bc.ca/gwells/api/v1/locations")
                .then((response: { data: any; }) => {
                    commit(SET_LOCATION_SEARCH_RESULTS, response.data)
                }).catch((error: any) => {
                    reject(error)
                })
            })
        },
        // @ts-ignore
        [FETCH_DATA_SOURCES] ({ commit }) {

            const demoData: Array<IDataSource> = [
                {
                    id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de18',
                    name: 'Canadian Climate Normals 1981-2010 Station Data - N VANCOUVER WHARVES',
                    web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0',
                    coordinates: [-123.12, 49.31]
                },
                {
                    id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de11',
                    name: 'Canadian Climate Normals 1981-2010 Station Data - STEVESTON',
                    web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=869&dispBack=0',
                    coordinates: [-123.19, 49.13]
                }
            ]

            const demoDataGeoJSON: FeatureCollection = {
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
                            web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=833&dispBack=0',
                        }
                    },
                    {
                        id: 'cb7d1bf2-66ec-4ff0-8e95-9af7b6a1de11',
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: [-123.19, 49.13]
                        },
                        properties: {
                            name: 'Canadian Climate Normals 1981-2010 Station Data - STEVESTON',
                            web_uri: 'http://climate.weather.gc.ca/climate_normals/results_1981_2010_e.html?searchType=stnProv&lstProvince=BC&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0&stnID=869&dispBack=0',
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
        // lastSearchTrigger (state) {
        //     return state.lastSearchTrigger
        // },
        // pendingSearch (state) {
        //     return state.pendingSearch
        // },
        // searchParams (state) {
        //     return state.searchParams
        // },
        // searchResultFilters (state) {
        //     return state.searchResultFilters
        // },
        locationSearchResults (state: { locationSearchResults: any; }) {
            return state.locationSearchResults
        },
        // pendingLocationSearch (state) {
        //     return state.pendingLocationSearch
        // },
        externalDataSources (state: { externalDataSources: any }) {
            return state.externalDataSources
        },
        activeMapLayers (state: { activeMapLayers: any }) {
            return state.activeMapLayers
        },
        mapLayerSelections (state: { mapLayerSelections: any }) {
            return state.mapLayerSelections
        },
        mapLayers (state: { mapLayers: any }) {
            return state.mapLayers
        },
        dataLayers (state: { dataLayers: any }) {
            return state.dataLayers
        },
        allLayers (state: { dataLayers: any, mapLayers: any }) {
            return [...state.dataLayers, ...state.mapLayers]
        }
    }
}
