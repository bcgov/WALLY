import EventBus from '../services/EventBus.js'
import * as utils from '../utils/dataUtils'

export default {
  state: {
    activeDataSources: []
  },
  actions: {

  },
  mutations: {
    addDataSource (state, payload) {
      state.activeDataSources.push(
        utils.DATA_SOURCES.find(function (source) {
          return source.id === payload
        })
      )
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
    allDataSources: () => utils.DATA_SOURCES
  }
}
