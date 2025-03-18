import EventBus from '../services/EventBus.js'
import ApiService from '../services/ApiService.js'
import router from '../router'
import centroid from '@turf/centroid'

export default {
  state: {
    activeDataMarts: [],
    activeDataMartLayers: [], // comes from 'activeLayers' on Map.js;
    selectionBoundingBox: [],
    dataMartFeatureInfo: { content: { properties: {} } },
    pointOfInterest: { content: { properties: {} } },
    dataMartFeatures: [], // selected points
    singleSelectionFeatures: [], // since features may be stacked/adjacent, a single click could return several features
    loadingFeature: false,
    loadingMultipleFeatures: false,
    featureError: ''
  },
  actions: {
    addDataMart ({ state, dispatch }, payload) {
      state.activeDataMarts.push(payload)
      dispatch('addApiLayer', payload)
    },
    getDataMartFeatures ({ commit, state }, payload) {
      if (!payload.layers || !payload.layers.length) {
        // no layers selected - stop here.
        return
      }
      commit('setLoadingFeature', true)
      commit('setFeatureError', '')
      commit('setLoadingMultipleFeatures', true)
      const layers = payload.layers.map((x) => {
        return 'layers=' + x.display_data_name + '&'
      })
      const polygon = payload.bounds
      const polygonQ = `polygon=${JSON.stringify(polygon.geometry.coordinates)}&`
      const width = 'width=' + payload.size.x + '&'
      const height = 'height=' + payload.size.y + '&'
      const srs = 'srs=EPSG:4326'
      const params = layers.join('') + polygonQ + width + height + srs
      // "layers=automated_snow_weather_station_locations&layers=ground_water_wells&bbox=-123.5&bbox=49&bbox=-123&bbox=50&width=500&height=500"
      ApiService.getApi('/aggregate/?' + params)
        .then((response) => {
          // console.log('response for aggregate', response)
          const displayData = response.data.display_data
          commit('setLoadingFeature', false)

          // end here if no layers returned any data.
          if (!displayData.some(layer => {
            return layer.geojson && layer.geojson.features.length
          })) {
            global.config.debug && console.log('[wally] no features found -' +
              ' skipping setting datamart features')
            return
          }

          // new features were found; the old features can be deleted.
          commit('resetDataMartFeatureInfo')
          commit('clearDataMartFeatures')

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

          global.config.debug && console.log('[wally] found feature(s) on' +
            ' map', featureCount)

          // Check whether there is a single feature being returned in the click area
          if (featureCount > 1) {
            // Multiple features returned
            displayData.forEach(layer => {
              commit('setDataMartFeatures', { [layer.layer]: layer.geojson.features })
            })

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
            // create a list containing only the single feature returned.
            // this allows the multiple features card to display something,
            // and enables easy exporting the single feature as an xlsx
            // using the same menu as when exporting multiple features.
            commit('setDataMartFeatures', { [displayDataName]: [feature] })
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
      commit('addGeoJSONLayer', layer)
    },
    removeDataMart ({ state, dispatch }, payload) {
      state.activeDataMarts = state.activeDataMarts.filter(function (source) {
        return source.displayDataName !== payload
      })
      dispatch('removeDataMartLayer', payload)
    },
    removeDataMartLayer ({ state, commit }, layer) {
      const displayDataName = layer.display_data_name || layer
      if (!displayDataName || !state.activeDataMartLayers[displayDataName]) {
        return
      }
      state.map.removeLayer(layer.id)
      commit('map/removeLayer', layer.id, { root: true })
      delete state.activeDataMartLayers[layer.id]
    }
  },
  mutations: {
    addGeoJSONLayer (state, layer) {
      if (!layer || !layer.data) {
        console.error('invalid format for data source/data mart')
        return
      }

      // layer.data should have a "features" or "geojson" property, which
      // must be a list of geojson Features.  For example, layer.data could be
      // a FeatureCollection format object. The 'features' list will be added to the map.
      let features
      if (layer.data.features && layer.data.features.length) {
        features = layer.data.features
      } else if (layer.data.geojson && layer.data.geojson.length) {
        features = layer.data.geojson
      }
      if (!features) {
        console.error('could not find a features list or object to add to map')
        return
      }

      // this.activeLayers[layer.display_data_name] = L.geoJSON(features, {
      //   onEachFeature: function (feature, layer) {
      //     layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + feature.properties.description + '</p>')
      //   }
      // })
      state.activeDataMartLayers[layer.display_data_name].addTo(state.map)
    },

    setLoadingMultipleFeatures (state, payload) {
      state.loadingMultipleFeatures = payload
    },
    setSingleSelectionFeatures (state, payload) {
      // sets the group of features that were selected by clicking on the map.
      // since features may be stacked and/or adjacent, one click will often return several results.
      state.singleSelectionFeatures = payload
    },
    setPointOfInterest: (state, payload) => {
      state.pointOfInterest = payload
    },
    resetPointOfInterest: (state) => {
      state.pointOfInterest = { content: { properties: {} } }
    },
    setDataMartFeatureInfo: (state, payload) => {
      state.dataMartFeatureInfo = payload

      global.config.debug && console.log('[wally] payload display name',
        payload.display_data_name)
      global.config.debug && console.log('[wally] route?',
        router.currentRoute.name)
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

      if (router.currentRoute.meta && router.currentRoute.meta.allowRedirect) {
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
    },
    setLoadingFeature: (state, payload) => { state.loadingFeature = payload },
    setFeatureError: (state, payload) => { state.featureError = payload },
    setDataMartFeatures: (state, payload) => {
      state.dataMartFeatures.push(payload)
    },
    clearDataMartFeatures: (state) => { state.dataMartFeatures = [] },
    setSelectionBoundingBox: (state, payload) => { state.selectionBoundingBox = payload }
  },
  getters: {
    pointOfInterest: state => state.pointOfInterest,
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
