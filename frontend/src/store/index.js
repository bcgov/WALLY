import Vue from 'vue'
import Vuex from 'vuex'
import store from './store'
import map from './mapStore'
import report from './reportStore'
import dataMart from './dataMartStore'
import stream from './streamStore'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    store,
    map,
    dataMart,
    report,
    stream
  }
})
