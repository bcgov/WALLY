import Vue from 'vue'
import Vuex from 'vuex'
import map from './mapStore'
import report from './reportStore'
import dataMart from './dataMartStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    map,
    dataMart,
    report
  }
})
