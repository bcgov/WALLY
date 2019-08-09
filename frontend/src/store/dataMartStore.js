import EventBus from '../services/EventBus.js'
import ApiService from '../services/ApiService.js'
import { wmsBaseURl, wmsParamString } from '../utils/wmsUtils'
import * as utils from '../utils/dataUtils'

export default {
  state: {
    activeDataMarts: [],
    dataMartInfo: { content: { properties: {} } },
    dataMartFeatures: [], // selected points
    dataMartFeatureInfo: {},
    dataMartLayers: [] // map layers
  },
  actions: {
    getDataMart ({ commit }, payload) {
      // Get the datamart either via API or wms layer
      const { id, url } = payload
      ApiService.getRaw(url).then((response) => {
        commit('addDataMart', {
          id: id,
          data: response.data
        })
        EventBus.$emit(`dataMart:updated`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
      })
    },
    getDataMartInfo ({ commit }, payload) {

    },
    getDataMartFeatureInfo ({ commit }, payload) {
      // WMS info
      // TODO: Complete this request
      ApiService.getRaw(payload.url).then((res) => {
        // TODO validate properties
        commit('setDataMartInfo', {
          id: res.data.features[0].id,
          coordinates: [payload.lat, payload.lng],
          properties: res.data.features[0].properties })
        EventBus.$emit(`feature:added`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
      })
    },
    getDataMartFeatures ({ commit }, payload) {
      // Get the datamart features (points, lines etc)
      // TODO: Separate API call from WMS call
      // eslint-disable-next-line eqeqeq
      payload.type === 'wms' &&
      ApiService.getRaw(wmsBaseURl + payload.layer + '/ows' + wmsParamString(payload))
        .then((response) => {
          let points = response.data.objects[payload.layer].geometries // TODO Test functional
          commit('setLayerFeatures', { [payload.layer]: points })
        }).catch((error) => {
          console.log(error)
        })

      payload.type === 'api' &&
      ApiService.getRaw(utils.API_URL + payload.feature.properties.url).then((res) => {
        console.log('response', res)
        // TODO: setLayerFeatures
        let points = payload.feature.points
        commit('setDataMartFeatures', {[payload.layer]: points})
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mutations: {
    setDataMartInfo: (state, payload) => { state.dataMartInfo = payload },
    setDataMartFeatures: (state, payload) => { state.dataMartFeatures.push(payload) },
    clearDataMartFeatures: (state) => { state.dataMartFeatures = [] },
    addDataMart (state, payload) {
      state.activeDataMarts.push(payload)
      EventBus.$emit(`dataMart:added`, payload)
    },
    removeDataMart (state, payload) {
      state.activeDataMarts = state.activeDataMarts.filter(function (source) {
        return source.id !== payload
      })
      EventBus.$emit(`dataMart:removed`, payload)
    }
  },
  getters: {
    dataMartInfo: state => state.dataMartInfo,
    dataMartFeatureInfo: state => state.dataMartFeatureInfo,
    dataMartFeatures: state => state.dataMartFeatures,
    activeDataMarts: state => state.activeDataMarts,
    isDataMartActive: state => id => !!state.activeDataMarts.find((x) => x && x.id === id),
    allDataMarts: () => [], // ideally grab these from the meta data api
    dataMartLayers: state => state.dataMartLayers
  }
}
