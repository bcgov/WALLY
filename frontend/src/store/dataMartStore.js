import EventBus from '../services/EventBus.js'
import ApiService from '../services/ApiService.js'
import router from '../router'
import centroid from '@turf/centroid'

export default {
  state: {
    activeDataMarts: [],
    displayTemplates: [],
    selectionBoundingBox: [],
    dataMartFeatureInfo: { content: { properties: {} } },
    dataMartFeatures: [], // selected points
    singleSelectionFeatures: [], // since features may be stacked/adjacent, a single click could return several features
    loadingFeature: false,
    loadingMultipleFeatures: false,
    featureError: ''
  },
  actions: {
    addDataMart ({ state, dispatch }, payload) {
      state.activeDataMarts.push(payload)
      // EventBus.$emit(`dataMart:added`, payload)
      dispatch('addApiLayer', payload)
    },
    getDataMartFeatures ({ commit, state }, payload) {
      if (!payload.layers || !payload.layers.length) {
        EventBus.$emit('info', 'No layers selected. Choose one or more layers and make another selection.')
        return
      }
      commit('setLoadingFeature', true)
      commit('setFeatureError', '')
      commit('setLoadingMultipleFeatures', true)
      var layers = payload.layers.map((x) => {
        return 'layers=' + x.display_data_name + '&'
      })
      let polygon = payload.bounds
      let polygonQ = `polygon=${JSON.stringify(polygon.geometry.coordinates)}&`
      var width = 'width=' + payload.size.x + '&'
      var height = 'height=' + payload.size.y
      var params = layers.join('') + polygonQ + width + height
      // "layers=automated_snow_weather_station_locations&layers=ground_water_wells&bbox=-123.5&bbox=49&bbox=-123&bbox=50&width=500&height=500"
      ApiService.getApi('/aggregate/?' + params)
        .then((response) => {
          // console.log('response for aggregate', response)
          let displayData = response.data.display_data
          let displayTemplates = response.data.display_templates
          commit('setLoadingFeature', false)

          // end here if no layers returned any data.
          if (!displayData.some(layer => {
            return layer.geojson && layer.geojson.features.length
          })) {
            return
          }

          let feature = {}
          let displayDataName = ''
          let featureCount = 0

          // If primary_key_match is in the payload then this query came from a search result
          // from our returned radius search we try and match the primary key to the specific search result
          // if there is a match we set the feature to that object
          feature = displayData[0].geojson.features.find((f) => {
            return f.id.toString() === payload.primary_key_match
          })
          displayDataName = displayData[0].layer

          // If no primary_key_match was found, then we add up the number of features returned
          // and set the feature/layer information
          if (!feature) {
            displayData.forEach(layer => {
              featureCount += layer.geojson.features.length
              if (layer.geojson.features.length === 1) {
                displayDataName = layer.layer
                feature = layer.geojson.features[0]
              }
            })
          }

          // Check whether there is a single feature being returned in the click area
          if (featureCount > 1) {
            // Multiple features returned
            displayData.forEach(layer => {
              commit('setDataMartFeatures', { [layer.layer]: layer.geojson.features })
            })
            // TODO currently we are not using displayTemplate information
            // Need to clean this up or re-purpose it
            commit('setDisplayTemplates', { displayTemplates })
            commit('setDataMartFeatureInfo', {})
            router.push({
              name: 'multiple-features'
            })
          } else {
            // Only one feature returned
            commit('setDataMartFeatureInfo',
              {
                type: 'Feature',
                display_data_name: displayDataName,
                geometry: feature.geometry,
                properties: feature.properties
              })

            commit('setDataMartFeatures', {})
          }
          commit('setLoadingFeature', false)
        }).catch((error) => {
          console.error(error)
          const msg = error.response ? error.response.data.detail : true
          EventBus.$emit('error', msg)
        }).finally(() => {
          commit('setLoadingMultipleFeatures', false)
        })
    },
    addApiLayer ({ state, commit }, payload) {
      const layer = state.activeDataMarts.find((x) => {
        return x.display_data_name === payload.displayDataName
      })
      commit('addGeoJSONLayer', layer, { root: true })
      // this.addGeoJSONLayer(layer)
    }
  },
  mutations: {
    setLoadingMultipleFeatures (state, payload) {
      state.loadingMultipleFeatures = payload
    },
    setSingleSelectionFeatures (state, payload) {
      // sets the group of features that were selected by clicking on the map.
      // since features may be stacked and/or adjacent, one click will often return several results.
      state.singleSelectionFeatures = payload
    },
    setDataMartFeatureInfo: (state, payload) => {
      state.dataMartFeatureInfo = payload

      // check if feature info is being reset. If so, stop here and don't alter route.
      if (!payload || payload === {} || !payload.geometry || !payload.display_data_name) {
        return
      }

      if (payload.display_data_name === 'user_defined_line') {
        return router.push({
          name: 'cross-section',
          query: {
            layer: 'user_defined_line',
            location: JSON.stringify(payload.geometry)
          }
        })
      }

      // todo: replace with route.meta option (e.g. "allowRedirect") to control automatically redirecting to feature cards.
      if (router.currentRoute.name === 'home' || router.currentRoute.name === 'place-poi' || router.currentRoute.name === 'multiple-features') {
        router.push({
          name: 'single-feature',
          query: {
            type: payload.geometry.type,
            layer: payload.display_data_name,
            location: payload.geometry ? centroid(payload).geometry.coordinates.join(',') : null
          }
        })
      }
    },
    resetDataMartFeatureInfo: (state) => {
      state.dataMartFeatureInfo = { content: { properties: {} } }
      state.featureError = ''
      router.push('/')
    },
    setLoadingFeature: (state, payload) => { state.loadingFeature = payload },
    setFeatureError: (state, payload) => { state.featureError = payload },
    setDataMartFeatures: (state, payload) => {
      state.dataMartFeatures.push(payload)
    },
    setDisplayTemplates: (state, payload) => { state.displayTemplates = payload },
    clearDataMartFeatures: (state) => { state.dataMartFeatures = [] },
    clearDisplayTemplates: (state) => { state.displayTemplates = [] },
    setSelectionBoundingBox: (state, payload) => { state.selectionBoundingBox = payload },
    removeDataMart (state, payload) {
      state.activeDataMarts = state.activeDataMarts.filter(function (source) {
        return source.displayDataName !== payload
      })
      EventBus.$emit(`dataMart:removed`, payload)
    }
  },
  getters: {
    displayTemplates: state => state.displayTemplates,
    dataMartFeatureInfo: state => state.dataMartFeatureInfo,
    dataMartFeatures: state => state.dataMartFeatures,
    loadingFeature: state => state.loadingFeature,
    featureError: state => state.featureError,
    selectionBoundingBox: state => state.selectionBoundingBox,
    activeDataMarts: state => state.activeDataMarts,
    isDataMartActive: state => displayDataName => !!state.activeDataMarts.find((x) => x && x.displayDataName === displayDataName),
    allDataMarts: () => [], // ideally grab these from the meta data api
    singleSelectionFeatures: state => state.singleSelectionFeatures,
    loadingMultipleFeatures: state => state.loadingMultipleFeatures,
    featureSelectionExists: state => {
      // returns a boolean indicating whether there is a selection active (either single or multiple features
      // selected)
      const singleFeatureSelected = !!(state.dataMartFeatureInfo && state.dataMartFeatureInfo.display_data_name)
      const multipleFeaturesSelected = !!(state.dataMartFeatures && state.dataMartFeatures.length)
      return singleFeatureSelected || multipleFeaturesSelected
    }
  }
}
