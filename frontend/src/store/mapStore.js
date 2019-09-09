import EventBus from '../services/EventBus.js'
// TODO: change to api call, or create new array just for map layers
import * as metadataUtils from '../utils/metadataUtils'
import ApiService from '../services/ApiService'

export default {
  state: {
    activeMapLayers: [],
    mapLayers: []
  },
  actions: {
    getMapLayers ({ commit }) {
      // We only fetch maplayers if we don't have a copy cached
      if (this.state.mapLayers === undefined) {
        return new Promise((resolve, reject) => {
          console.log('Getting map layers')
          ApiService.getApi('/catalogue')
            .then((response) => {
              commit('setMapLayers', response.data)
              EventBus.$emit(`layers:loaded`)
            })
            .catch((error) => {
              reject(error)
            })
        })
      }
    }
  },
  mutations: {
    addMapLayer (state, payload) {
      state.activeMapLayers.push(
        state.mapLayers.find((layer) => {
          return layer.display_data_name === payload
        })
      )
      EventBus.$emit(`layer:added`, payload)
    },
    removeMapLayer (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter((layer) => {
        return layer.display_data_name !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    },
    setMapLayers (state, payload) {
      state.mapLayers = payload
    }
  },
  getters: {
    activeMapLayers: state => state.activeMapLayers,
    isMapLayerActive: state => displayDataName => !!state.activeMapLayers.find((x) => x && x.display_data_name === displayDataName),
    mapLayerName: (state) => (wmsName) => {
      let layer = state.mapLayers.find(e => e.wms_name === wmsName)
      return layer ? layer.display_name : ''
    },
    getMapLayer: (state) => (displayDataName) => {
      let layer = state.mapLayers.find(e => e.display_data_name === displayDataName)
      return layer || null
    },
    allMapLayers: state => state.mapLayers
  }
}
