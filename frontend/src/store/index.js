import Vue from 'vue'
import Vuex from 'vuex'
import map from './mapStore'
import wms from './wmsStore'
import data from './dataStore'
import report from './reportStore'
import dataMart from './dataMartStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    map,
    wms,
    data,
    dataMart,
    report
  }
})
