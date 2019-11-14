import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WellsNearby from '@/components/analysis/WellsNearby.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()
let wrapper

describe('Wells Nearby', () => {
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
    store = new Vuex.Store({ getters, mutations })
    wrapper = shallowMount(WellsNearby, {
      vuetify,
      store,
      localVue
    })
  })

  it('Redraws circle on map', () => {
    wrapper.setProps({ coordinates: [-122.94492, 50.11588] })
    wrapper.vm.showCircle()
    expect(wrapper.emitted('shapes:reset'.toBeTruthy))
    expect(wrapper.emitted('shapes:add'.toBeTruthy))
  })

  it('Is hidden when there\'s no data', () => {
    wrapper.setData({ wells: [] })
    expect(wrapper.findAll('#wells_nearby .charts').length).toEqual(0)
  })

  it('Shows a chart when there\'s data', () => {
    let well = {
      aquifer: null,
      aquifer_hydraulically_connected: null,
      aquifer_subtype: null,
      diameter: '10',
      distance: 431.07350877,
      finished_well_depth: 158,
      intended_water_use: 'Unknown Well Use',
      screen_set: Array[0],
      static_water_level: 13,
      street_address: '',
      swl_to_bottom_of_well: 145,
      swl_to_screen: null,
      top_of_screen: null,
      top_of_screen_type: null,
      well_tag_number: 80579,
      well_yield: 180,
      well_yield_unit: 'USGPM'
    }
    wrapper.setData({ wells: [well] })
    expect(wrapper.findAll('#wells_nearby .charts').length).toEqual(1)
  })

  it('Shows all three charts when there\'s data', () => {
    let well = {
      aquifer: null,
      aquifer_hydraulically_connected: null,
      aquifer_subtype: null,
      diameter: '10',
      distance: 431.07350877,
      finished_well_depth: 158,
      intended_water_use: 'Unknown Well Use',
      screen_set: Array[0],
      static_water_level: 13,
      street_address: '',
      swl_to_bottom_of_well: 145,
      swl_to_screen: null,
      top_of_screen: null,
      top_of_screen_type: null,
      well_tag_number: 80579,
      well_yield: 180,
      well_yield_unit: 'USGPM'
    }
    wrapper.setData({ wells: [well] })
    expect(wrapper.findAll('#wells_nearby .charts .chart').length).toEqual(3)
  })
})
