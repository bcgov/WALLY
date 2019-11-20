/*
 Start slowly refactoring the map store into this file
 */
import ApiService from '../services/ApiService'
import mapboxgl from 'mapbox-gl'
import MapboxDraw from '@mapbox/mapbox-gl-draw'

export default {
  state: {
    // infoPanelVisible: true
    map: {},
    draw: {}
  },
  actions: {
    async initMap ({ commit, dispatch }) {
      // 'use strict'
      const mapConfig = await ApiService.get('api/v1/map-config')
      mapboxgl.accessToken = mapConfig.data.mapbox_token

      const zoomConfig = {
        center: process.env.VUE_APP_MAP_CENTER ? JSON.parse(process.env.VUE_APP_MAP_CENTER) : [-124, 54.5],
        zoomLevel: process.env.VUE_APP_MAP_ZOOM_LEVEL ? process.env.VUE_APP_MAP_ZOOM_LEVEL : 4.7
      }

      let map = new mapboxgl.Map({
        container: 'map', // container id
        // style: mapConfig.data.mapbox_style, // dev or prod map style
        style: mapConfig.data.mapbox_style,
        center: zoomConfig.center, // starting position
        zoom: zoomConfig.zoomLevel // starting zoom
      })
      // End of basic map
      commit('setMap', map)

      dispatch('initMapDraw')
      // dispatch('initGeocoder')
      //
      // dispatch('addMapControls')
      // dispatch('addMapClick')
      // dispatch('addMapParcelHovers')
      // dispatch('addMapSelectionModes')
    },
    initMapDraw ({ commit }) {
      // Initialize draw & set modes
      const modes = MapboxDraw.modes
      modes.simple_select.onTrash = this.clearSelections
      modes.draw_polygon.onTrash = this.clearSelections
      modes.draw_point.onTrash = this.clearSelections
      modes.direct_select.onTrash = this.clearSelections

      let draw = new MapboxDraw({
        modes: modes,
        displayControlsDefault: false,
        controls: {
          polygon: true,
          point: true,
          trash: true
        }
      })

      commit('setDraw', draw)
    }
  },
  mutations: {
    setMap (state, payload) {
      state.map = payload
    },
    setDraw (state, payload) {
      state.draw = payload
    }
  },
  getters: {
    // infoPanelVisible: state => state.infoPanelVisible,
  }
}
