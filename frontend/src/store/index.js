import Vue from 'vue'
import Vuex from 'vuex'
import store from './store'
import map from './mapStore'
import report from './reportStore'
import dataMart from './dataMartStore'
import stream from './streamStore'
import feature from './featureStore'
import crossSection from './crossSection'
import surfaceWater from './surfaceWaterStore'
import user from './userStore'
import customLayers from './customLayers'
import importer from './importerStore'
import project from './projectStore'
import savedAnalyses from './savedAnalyses'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    store,
    map,
    dataMart,
    report,
    stream,
    feature,
    crossSection,
    surfaceWater,
    user,
    customLayers,
    importer,
    project,
    savedAnalyses
  }
})
