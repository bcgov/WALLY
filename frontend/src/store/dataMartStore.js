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
    getDataMart ({ commit }, payload) {
      // Get the datamart either via API or wms layer
      const { displayDataName, url } = payload
      ApiService.getRaw(url).then((response) => {
        commit('addDataMart', {
          displayDataName: displayDataName,
          data: response.data
        })
        EventBus.$emit(`dataMart:updated`, payload)
      }).catch(() => {
        EventBus.$emit('error', true)
      })
    },
    getDataMartFeatureInfo ({ commit }, payload) {
      const { display_data_name, pk } = payload
      commit('setLoadingFeature', true)
      commit('setFeatureError', '')
      ApiService.getApi('/feature?layer=' + display_data_name + '&pk=' + pk)
        .then((response) => {
          commit('setLoadingFeature', false)
          commit('setLayerSelectionActiveState', false)
          let feature = response.data
          commit('setDataMartFeatureInfo',
            {
              type: feature.type,
              display_data_name: display_data_name,
              geometry: feature.geometry,
              properties: feature.properties
            })
        })
        .catch((error) => {
          const msg = error.response ? error.response.data.detail : true
          commit('setLoadingFeature', false)
          commit('setFeatureError', msg)
          commit('setDataMartFeatureInfo', {})
          console.log(msg) // TODO create error state item and mutation
          EventBus.$emit('error', msg)
        })
    },
    getDataMartFeatures ({ commit }, payload) {
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
      ApiService.getApi('/aggregate?' + params)
        .then((response) => {
          // console.log('response for aggregate', response)
          let displayData = response.data.display_data
          let displayTemplates = response.data.display_templates
          commit('setLoadingFeature', false)

          if (!displayData.some(layer => {
            return layer.geojson && layer.geojson.features.length
          })) {
            EventBus.$emit('info', 'No features were found in your search area.')
            return
          }

          let feature = {}
          let layerName = ''
          let featureCount = 0

          // If primary_key_match is in the payload then this query came from a search result
          // from our returned radius search we try and match the primary key to the specific search result
          // if there is a match we set the feature to that object
          feature = displayData[0].geojson.features.find((f) => {
            return f.id.toString() === payload.primary_key_match
          })
          layerName = displayData[0].layer

          // If no primary_key_match was found, then we add up the number of features returned
          // and set the feature/layer information
          if (!feature) {
            displayData.forEach(layer => {
              featureCount += layer.geojson.features.length
              if (layer.geojson.features.length === 1) {
                layerName = layer.layer
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
          } else {
            // Only one feature returned
            commit('setDataMartFeatureInfo',
              {
                type: feature.type,
                display_data_name: layerName,
                geometry: feature.geometry,
                properties: feature.properties
              })
            commit('setDataMartFeatures', {})
          }
          commit('setLoadingFeature', false)
          commit('setLayerSelectionActiveState', false)
        }).catch((error) => {
          const msg = error.response ? error.response.data.detail : true
          EventBus.$emit('error', msg)
        }).finally(() => {
          commit('setLoadingMultipleFeatures', false)
        })
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
      router.push({
        name: 'single-feature',
        query: {
          type: payload.geometry.type,
          layer: payload.display_data_name,
          location: payload.geometry ? centroid(payload).geometry.coordinates.join(',') : null
        }
      })
    },
    resetDataMartFeatureInfo: (state) => {
      state.dataMartFeatureInfo = { content: { properties: {} } }
      state.featureError = ''
      router.push('/')
    },
    setLoadingFeature: (state, payload) => { state.loadingFeature = payload },
    setFeatureError: (state, payload) => { state.featureError = payload },
    setDataMartFeatures: (state, payload) => { state.dataMartFeatures.push(payload) },
    setDisplayTemplates: (state, payload) => { state.displayTemplates = payload },
    clearDataMartFeatures: (state) => { state.dataMartFeatures = [] },
    clearDisplayTemplates: (state) => { state.displayTemplates = [] },
    setSelectionBoundingBox: (state, payload) => { state.selectionBoundingBox = payload },
    addDataMart (state, payload) {
      state.activeDataMarts.push(payload)
      EventBus.$emit(`dataMart:added`, payload)
    },
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
      return singleFeatureSelected || multipleFeaturesSelected || !!state.loadingMultipleFeatures
    }
  }
}
