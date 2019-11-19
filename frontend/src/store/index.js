import Vue from 'vue'
import Vuex from 'vuex'
import store from './store'
import map from './mapStore'
import mapBox from './mapBoxStore'
import report from './reportStore'
import dataMart from './dataMartStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    store,
    map,
    mapBox,
    dataMart,
    report
  }
})
