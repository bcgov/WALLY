import Vue from 'vue/types'
import Vuex from 'vuex/types'
import EventBus from '../services/EventBus.js'
import * as utils from "../utils/mapUtils";

Vue.use(Vuex)

export default {
  state: {
    activeMapLayers: []
  },
  actions: {

  },
  mutations: {
    addMapLayer (state, payload) {
      state.activeMapLayers.push(
        utils.MAP_LAYERS.find(function (layer) {
          return layer.id === payload
        })
      )
      EventBus.$emit(`layer:added`, payload)
    },
    removeMapLayer (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter(function (layer) {
        return layer.id !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    }
  },
  getters: {
    activeMapLayers: state => state.activeMapLayers,
    isMapLayerActive: state => layer => !!state.activeMapLayers[layer],
    allMapLayers: () => utils.MAP_LAYERS
  }
}
