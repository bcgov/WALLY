import Vue from 'vue';
import Vuex from 'vuex';

import {
    SEARCH_LOCATIONS,
    SEARCH_WELLS,
    FETCH_WELL_LOCATIONS
} from './actions.types'

import {
    SET_SEARCH_BOUNDS,
    SET_SEARCH_PARAMS,
    SET_LOCATION_SEARCH_RESULTS,
    SET_SEARCH_RESULT_FILTERS
} from './mutations.types'

// @ts-ignore
import ApiService from '../../services/ApiService'

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
    }
}
