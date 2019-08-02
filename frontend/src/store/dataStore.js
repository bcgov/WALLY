import EventBus from '../services/EventBus.js'
import * as utils from '../utils/dataUtils'
import ApiService from '../services/ApiService'

export default {
  state: {
    activeDataSources: []
  },
  actions: {
    getDataSource ({ commit }, payload) {
      const { id, url } = payload
      ApiService.getRaw(url).then((res) => {
        commit('addDataSource', {
          id: id,
          data: res.data
        })
        EventBus.$emit(`dataSource:updated`, payload)
      }).catch((error) => {
        console.error(error) // TODO create error state item and mutation
      })
    },
    getDataSourceFeatures({ commit }, payload) {
      // TODO: ApiService call to hydat data, send in payload.id
      let feature = payload.feature
      ApiService.getRaw(utils.API_URL + feature.properties.url).then((res) => {
        console.log('response', res)
      })
    }
  },
  mutations: {
    addDataSource (state, payload) {
      state.activeDataSources.push(payload)
      EventBus.$emit(`dataSource:added`, payload)
    },
    removeDataSource (state, payload) {
      state.activeDataSources = state.activeDataSources.filter(function (source) {
        return source.id !== payload
      })
      EventBus.$emit(`dataSource:removed`, payload)
    }
  },
  getters: {
    activeDataSources: state => state.activeDataSources,
    isDataSourceActive: state => id => !!state.activeDataSources.find((x) => x && x.id === id),
    allDataSources: () => utils.DATA_LAYERS
  }
}
