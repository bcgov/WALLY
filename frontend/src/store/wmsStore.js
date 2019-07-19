import ApiService from '../services/ApiService'
import EventBus from '../services/EventBus.js'
import { wmsBaseURl, wmsParamString } from '../utils/wmsUtils'

export default {
  state: {
    featureInfo: { content: { properties: {} } },
    featureLayers: []
  },
  actions: {
    getFeatureInfo ({ commit }, payload) {
      ApiService.getRaw(payload.url).then((res) => {
        // TODO validate properties
        commit('setFeatureInfo', {
          id: res.data.features[0].id,
          coordinates: [payload.lat, payload.lng],
          properties: res.data.features[0].properties })
        EventBus.$emit(`feature:added`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
      })
    },
    getLayerFeatures ({ commit }, payload) {
      ApiService.getRaw(wmsBaseURl + payload.layer + '/ows' + wmsParamString(payload))
        .then((response) => {
          let points = response.data.objects[payload.layer].geometries // TODO Test functional
          commit('setLayerFeatures', { [payload.layer]: points })
        }).catch((error) => {
          console.log(error)
        })
    }
  },
  mutations: {
    setFeatureInfo: (state, payload) => { state.featureInfo = payload },
    setLayerFeatures: (state, payload) => { state.featureLayers.push(payload) },
    clearFeatureLayers: (state) => { state.featureLayers = [] }
  },
  getters: {
    featureInfo: state => state.featureInfo,
    featureLayers: state => state.featureLayers
  }
}
