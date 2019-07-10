import Vue from 'vue'
import Vuex from 'vuex'
import map from './mapStore'
import wms from './wmsStore'
import data from './dataStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    map,
    wms,
    data
  }
})
