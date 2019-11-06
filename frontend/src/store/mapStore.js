import EventBus from '../services/EventBus.js'
// TODO: change to api call, or create new array just for map layers
import ApiService from '../services/ApiService'

export default {
  state: {
    selectedMapLayerNames: [],
    activeMapLayers: [],
    mapLayers: [],
    highlightFeatureData: {},
    layerCategories: [],
    layerSelectionActive: true,
    mapFeatureSelectionSingleActive: false
  },
  actions: {
    getMapLayers ({ commit }) {
      // We only fetch maplayers if we don't have a copy cached
      if (this.state.mapLayers === undefined) {
        return new Promise((resolve, reject) => {
          console.log('Getting map layers')
          ApiService.getApi('/catalogue')
            .then((response) => {
              commit('setMapLayers', response.data.layers)
              commit('setLayerCategories', response.data.categories)
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
    setLayerSelectionActive (state, payload) {
      state.layerSelectionActive = payload
    },
    setMapFeatureSelectionSingleActive (state, payload) {
      state.mapFeatureSelectionSingleActive = payload
    },
    setLayerCategories (state, payload) {
      state.layerCategories = payload
    },
    addMapLayer (state, payload) {
      let mapLayer = state.mapLayers.find((layer) => {
        return layer.display_data_name === payload
      })
      if (!state.activeMapLayers.includes(mapLayer)) {
        state.activeMapLayers.push(mapLayer)
        EventBus.$emit(`layer:added`, payload)
      }
    },
    removeMapLayer (state, payload) {
      state.activeMapLayers = state.activeMapLayers.filter((layer) => {
        return layer.display_data_name !== payload
      })
      EventBus.$emit(`layer:removed`, payload)
    },
    setActiveMapLayers (state, payload) {
      // accepts an array of layer names and sets the active map layers accordingly

      state.selectedMapLayerNames = payload

      // list of prev layers.  the payload is the new list of layers about to be active.
      const prev = state.activeMapLayers.map(l => l.display_data_name)

      // get list of layers that were deselected (they were in `prev`, but are not in payload),
      // and sent an event to remove them.
      prev.filter((l) => !payload.includes(l)).forEach((l) => EventBus.$emit(`layer:removed`, l))

      // similarly, now get a list of layers that are in payload but weren't in the previous active layers.
      payload.filter((l) => !prev.includes(l)).forEach((l) => EventBus.$emit(`layer:added`, l))

      // reset the list of active layers
      state.activeMapLayers = state.mapLayers.filter((l) => {
        return payload.includes(l.display_data_name)
      })

      // send an event to redraw any current features and update selection.
      EventBus.$emit('draw:redraw', { showFeatureList: false })
    },
    setMapLayers (state, payload) {
      state.mapLayers = payload
    },
    updateHighlightFeatureData (state, payload) {
      state.highlightFeatureData = payload
    }
  },
  getters: {
    selectedMapLayerNames: state => state.selectedMapLayerNames,
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
    allMapLayers: state => state.mapLayers,
    highlightFeatureData: state => state.highlightFeatureData,
    getCategories: state => state.layerCategories,
    layerSelectionActive: state => state.layerSelectionActive,
    mapFeatureSelectionSingleActive: state => state.mapFeatureSelectionSingleActive
  }
}
