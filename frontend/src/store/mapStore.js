import EventBus from '../services/EventBus.js'
// TODO: change to api call, or create new array just for map layers
import * as metadataUtils from '../utils/metadataUtils'
import ApiService from "../services/ApiService";

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
          ApiService.getApi('/maplayers')
            .then((response) => {
              commit('setMapLayers', response.data)
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
        this.getters.allMapLayers.find((layer) => {
          return layer.layer_id === payload
        })
      )
      EventBus.$emit(`layer:added`, payload)
    },
    removeMapLayer (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter((layer) => {
        return layer.layer_id !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    },
    setMapLayers (state, payload) {
      state.mapLayers = payload
    }
  },
  getters: {
    activeMapLayers: state => state.activeMapLayers,
    isMapLayerActive: state => layerId => !!state.activeMapLayers.find((x) => x && x.layer_id === layerId),
    mapLayerName: (state) => (wmsName) => { 
      var layer = state.mapLayers.find(e => e.wms_name === wmsName)
      return layer ? layer.layer_name : ''
    },
    allMapLayers: state => state.mapLayers
  }
}
