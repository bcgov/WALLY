import EventBus from '../services/EventBus.js'
import * as utils from '../utils/dataUtils'
import ApiService from '../services/ApiService'

export default {
  state: {
    activeDataLayers: []
  },
  actions: {
    getDataLayer ({ commit }, payload) {
      ApiService.getRaw(payload.url).then((res) => {
        commit('addDataSource', {
          id: payload.id,
          data: res.data
        })
        EventBus.$emit(`dataLayer:added`, payload)
      }).catch((error) => {
        console.log(error) // TODO create error state item and mutation
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
    isDataSourceActive: state => source => !!state.activeDataSources[source],
    allDataSources: () => utils.DATA_LAYERS
  }
}
