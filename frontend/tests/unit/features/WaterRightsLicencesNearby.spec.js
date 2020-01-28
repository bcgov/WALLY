import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WaterRightsLicencesNearby from '@/components/analysis/WaterRightsLicencesNearby.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

const testResults = JSON.parse(JSON.stringify([{ 'distance': 337.07812204, 'LICENCE_NUMBER': '500998', 'LICENCE_STATUS': 'Current', 'POD_NUMBER': 'PW195714', 'POD_SUBTYPE': 'PWD', 'PURPOSE_USE': 'WSA11 - Lawn, Fairway & Garden ', 'SOURCE_NAME': '389', 'QUANTITY': 720, 'QUANTITY_UNITS': 'm3/year ', 'QTY_DIVERSION_MAX_RATE': null, 'QTY_UNITS_DIVERSION_MAX_RATE': 'm3/sec', 'QUANTITY_FLAG': 'T', 'QUANTITY_FLAG_DESCRIPTION': 'Total demand for purpose, one POD.' }, { 'distance': 359.31633469, 'LICENCE_NUMBER': 'C126607', 'LICENCE_STATUS': 'Current', 'POD_NUMBER': 'PD183985', 'POD_SUBTYPE': 'POD', 'PURPOSE_USE': '11B - Conservation: Use of Water ', 'SOURCE_NAME': 'Fitzsimmons Creek', 'QUANTITY': 0.38, 'QUANTITY_UNITS': 'm3/sec ', 'QTY_DIVERSION_MAX_RATE': null, 'QTY_UNITS_DIVERSION_MAX_RATE': 'm3/sec', 'QUANTITY_FLAG': 'T', 'QUANTITY_FLAG_DESCRIPTION': 'Total demand for purpose, one POD.' }, { 'distance': 978.70488728, 'LICENCE_NUMBER': 'C108126', 'LICENCE_STATUS': 'Current', 'POD_NUMBER': 'PD69291', 'POD_SUBTYPE': 'POD', 'PURPOSE_USE': '02F - Lwn, Fairway & Grdn: Watering ', 'SOURCE_NAME': 'Green Lake', 'QUANTITY': 220792.92, 'QUANTITY_UNITS': 'm3/year ', 'QTY_DIVERSION_MAX_RATE': null, 'QTY_UNITS_DIVERSION_MAX_RATE': 'm3/sec', 'QUANTITY_FLAG': 'T', 'QUANTITY_FLAG_DESCRIPTION': 'Total demand for purpose, one POD.' }, { 'distance': 414.55433329, 'APPLICATION_JOB_NUMBER': 'WLA0Z116454-0001', 'APPLICATION_STATUS': 'Refused', 'LICENCE_NUMBER': null, 'LICENCE_STATUS': null, 'POD_NUMBER': 'PD76227', 'POD_SUBTYPE': 'POD', 'PURPOSE_USE': '07C - Power: General ', 'SOURCE_NAME': null, 'QUANTITY': null, 'QUANTITY_UNITS': null, 'QTY_DIVERSION_MAX_RATE': null, 'QTY_UNITS_DIVERSION_MAX_RATE': 'm3/sec', 'QUANTITY_FLAG': null, 'QUANTITY_FLAG_DESCRIPTION': null }]))

describe('WaterRightsLicencesNearby.vue', () => {
  let mutations, getters, store
  beforeEach(() => {
    mutations = {
      setActiveMapLayers: jest.fn(),
      removeMapLayer: jest.fn()
    }
    getters = {
      isMapLayerActive: state => layerId => false,
      activeMapLayers: () => ([]),
      dataMartFeatureInfo: () => {
      },
      dataMartFeatures: () => [],
      allMapLayers: () => [],
      getCategories: () => [],
      featureSelectionExists: () => null
    }
    let map = {
      namespaced: true,
      getters,
      mutations
    }
    store = new Vuex.Store({ modules: { map } })
  })

  it('filters based on POD type', () => {
    const wrapper = shallowMount(WaterRightsLicencesNearby, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: { geometry: { 'coordinates': [-127.57192816676897, 50.53235018962306], 'type': 'Point' } }
      }
    })

    wrapper.setData({
      results: testResults
    })

    expect(wrapper.vm.filteredLicences.length).toBe(4)

    wrapper.setData({
      tableOptions: { subtypes: { PWD: false } }
    })
    expect(wrapper.vm.filteredLicences.length).toBe(3)
  })
  it('filters out applications', () => {
    const wrapper = shallowMount(WaterRightsLicencesNearby, {
      vuetify,
      store,
      localVue
    })

    wrapper.setData({
      results: testResults
    })

    expect(wrapper.vm.filteredLicences.length).toBe(4)

    wrapper.setData({
      tableOptions: { applications: false }
    })
    expect(wrapper.vm.filteredLicences.length).toBe(3)
  })
})
