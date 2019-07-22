import EventBus from '../services/EventBus.js'
import * as utils from '../utils/mapUtils'

export default {
  state: {
    activeMapLayers: []
  },
  actions: {

  },
  mutations: {
    addMapLayer (state, payload) {
      state.activeMapLayers.push(
        utils.MAP_LAYERS.find((layer) => {
          return layer.id === payload
        })
      )
      EventBus.$emit(`layer:added`, payload)
    },
    removeMapLayer (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter((layer) => {
        return layer.id !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    }
  },
  getters: {
    activeMapLayers: state => state.activeMapLayers,
    isMapLayerActive: state => layerId => !!state.activeMapLayers.find((x) => x && x.id === layerId),
    allMapLayers: () => utils.MAP_LAYERS
  }
}
