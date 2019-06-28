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
    SET_DATA_SOURCES
} from './mutations.types'

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
        externalDataSources: [],
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
        externalDataSources (state: { externalDataSources: any; }) {
            return state.externalDataSources
        }
    }
}
