import EventBus from '../services/EventBus.js'
import * as utils from '../utils/dataUtils'
import ApiService from '../services/ApiService'

export default {
  state: {
    activeDataMarts: [],
    dataMartInfo: { content: { properties: {} } },
    dataMartLayers: []
  },
  actions: {
    getDataMart ({ commit }, payload) {
      const { id, url } = payload
      ApiService.getRaw(url).then((res) => {
        commit('addDataMart', {
          id: id,
          data: res.data
        })
        EventBus.$emit(`dataMart:updated`, payload)
      }).catch((error) => {
        console.error(error) // TODO create error state item and mutation
      })
    },
    getDataMartInfo ({ commit }, payload) {
      // TODO: Complete this request
      // ApiService.getRaw(payload.url).then( (res) => {
      //   commit('setDataMartInfo', {
      //
      //   })
      // })
    },
    getDataMartFeatures ({ commit }, payload) {
      // TODO: ApiService call to hydat data, send in payload.id
      let feature = payload.feature
      ApiService.getRaw(utils.API_URL + feature.properties.url).then((res) => {
        console.log('response', res)
        // TODO: setLayerFeatures,w
        let points = feature.points
        commit('setDataMartFeatures', { [payload.layer]: points })
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mutations: {
    addDataMart (state, payload) {
      state.activeDataMarts.push(payload)
      EventBus.$emit(`dataMart:added`, payload)
    },
    removeDataMart (state, payload) {
      state.activeDataMarts = state.activeDataMarts.filter(function (datamart) {
        return datamart.id !== payload
      })
      EventBus.$emit(`dataMart:removed`, payload)
    },
    setDataMartFeatures: (state, payload) => { state.dataMartLayers.push(payload) }
    // TODO: setFeatureInfo state.featureInfo =?
    // TODO: setLayerFeatures state.featureLayer.push(payload)
  },
  getters: {
    activeDataMarts: state => state.activeDataMarts,
    isDataMartActive: state => id => !!state.activeDataMarts.find((x) => x && x.id === id),
    allDataMarts: () => utils.DATA_LAYERS,
    dataMartLayers: state => state.dataMartLayers
  }
}
