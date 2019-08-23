import EventBus from '../services/EventBus.js'
// TODO: change to api call, or create new array just for map layers
import * as metadataUtils from '../utils/metadataUtils'

export default {
  state: {
    activeMapLayers: []
  },
  actions: {

  },
  mutations: {
    addMapLayer (state, payload) {
      state.activeMapLayers.push(
        metadataUtils.DATA_MARTS.find((layer) => {
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
    allMapLayers: () => metadataUtils.DATA_MARTS
  }
}
