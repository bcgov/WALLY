import EventBus from '../services/EventBus.js'
// TODO: change to api call, or create new array just for map layers
import ApiService from '../services/ApiService'
import baseMapDescriptions from '../utils/baseMapDescriptions'
import router from '../router'

export default {
  state: {
    map: null,
    draw: {},
    geocoder: {},
    layerSelectTriggered: false,
    selectedMapLayerNames: [],
    activeMapLayers: [],
    mapLayers: [],
    highlightFeatureData: {},
    highlightFeaturesData: [],
    layerCategories: [],
    layerSelectionActive: true,
    selectedBaseLayers: [
      'national-park',
      'landuse',
      'contour-line',
      'hillshade'
    ],
    baseMapLayers: [{
      id: 'base-map-layers',
      name: 'Base Map Layers',
      children: baseMapDescriptions
    }]
  },
  actions: {
    async addPointOfInterest ({ state, dispatch }, feature) {
      if (!state.map.loaded()) {
        return
      }

      state.draw.add(feature)
      dispatch('handleSelect', { features: [feature] })
    },
    handleAddPointSelection ({ commit, dispatch, state }, feature) {
      feature.display_data_name = 'point_of_interest'
      commit('setDataMartFeatureInfo', feature)
    },
    handleSelect ({ commit, dispatch, state }, feature, options) {
      // default options when calling this handler.
      //
      // showFeatureList: whether features selected by the user should be immediately shown in
      // a panel.  This might be false if the user is selecting layers and may want to select
      // several before being "bumped" to the selected features list.
      //
      // example: EventBus.$emit('draw:redraw', { showFeatureList: false })
      const defaultOptions = {
        showFeatureList: true
      }

      options = Object.assign({}, defaultOptions, options)

      if (!feature || !feature.features || !feature.features.length) return

      if (options.showFeatureList) {
        commit('setLayerSelectionActiveState', false)
      }

      const newFeature = feature.features[0]
      commit('replaceOldFeatures', newFeature.id)

      if (newFeature.geometry.type === 'Point') {
        return dispatch('handleAddPointSelection', newFeature)
      }
      // for drawn rectangular regions, the polygon describing the rectangle is the first
      // element in the array of drawn features.
      // note: this is what might break if extending the selection tools to draw more objects.
      dispatch('getMapObjects', newFeature)
      commit('setSelectionBoundingBox', newFeature)
    },
    getMapLayers ({ commit }) {
      // We only fetch maplayers if we don't have a copy cached
      if (this.state.mapLayers === undefined) {
        return new Promise((resolve, reject) => {
          console.log('Getting map layers')
          ApiService.getApi('/catalogue/all')
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
    },
    async getMapObjects ({ commit, dispatch, state, getters }, bounds) {
      // TODO: Separate activeMaplayers by activeWMSLayers and activeDataMartLayers

      const canvas = await state.map.getCanvas()
      const size = { x: canvas.width, y: canvas.height }

      commit('clearDataMartFeatures')
      dispatch('getDataMartFeatures', {
        bounds: bounds,
        size: size,
        layers: state.activeMapLayers
      })
    }
  },
  mutations: {
    replaceOldFeatures (state, newFeature = null) {
      // replace all previously drawn features with the new one.
      // this has the effect of only allowing one selection box to be drawn at a time.
      const old = state.draw.getAll().features.filter((f) => f.id !== newFeature)
      state.draw.delete(old.map((feature) => feature.id))
    },
    setMap (state, payload) {
      state.map = payload
    },
    setDraw (state, payload) {
      state.draw = payload
    },
    setGeocoder (state, payload) {
      state.geocoder = payload
    },
    setLayerSelectTriggered (state, payload) {
      state.layerSelectTriggered = payload
    },
    setLayerSelectionActiveState (state, payload) {
      state.layerSelectionActive = payload
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
    setActiveBaseMapLayers (state, payload) {
      let prev = state.selectedBaseLayers
      prev.filter((l) => !payload.includes(l)).forEach((l) => EventBus.$emit(`baseLayer:removed`, l))
      payload.filter((l) => !prev.includes(l)).forEach((l) => EventBus.$emit(`baseLayer:added`, l))
      state.selectedBaseLayers = payload
    },
    setMapLayers (state, payload) {
      state.mapLayers = payload
    },
    updateHighlightFeatureData (state, payload) {
      state.highlightFeatureData = payload
    },
    updateHighlightFeaturesData (state, payload) {
      state.highlightFeaturesData = payload
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
    highlightFeaturesData: state => state.highlightFeaturesData,
    getCategories: state => state.layerCategories,
    layerSelectionActive: state => state.layerSelectionActive,
    selectedBaseLayers: state => state.selectedBaseLayers,
    baseMapLayers: state => state.baseMapLayers,
    map: state => state.map,
    draw: state => state.draw,
    geocoder: state => state.geocoder,
    layerSelectTriggered: state => state.layerSelectTriggered
  }
}
