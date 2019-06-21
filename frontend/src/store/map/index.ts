import Vue from 'vue';
import Vuex from 'vuex';

import {
    SEARCH_LOCATIONS,
    SEARCH_WELLS
} from './actions.types'

import {
    SET_SEARCH_BOUNDS,
    SET_SEARCH_PARAMS,
    SET_SEARCH_RESULT_FILTERS
} from './mutations.types'

Vue.use(Vuex);

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

export default new Vuex.Store({
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
        [SET_SEARCH_BOUNDS] (state, payload) {
            state.searchBounds = payload
        },
        [SET_SEARCH_PARAMS] (state, payload) {
            state.searchParams = cleanParams(payload)
        },
    },
    actions: {

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
        // locationSearchResults (state) {
        //     return state.locationSearchResults
        // },
        // pendingLocationSearch (state) {
        //     return state.pendingLocationSearch
        // },
    }
});
