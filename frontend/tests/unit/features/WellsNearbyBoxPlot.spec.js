import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WellsNearbyBoxPlot from '@/components/analysis/wells_nearby/WellsNearbyBoxPlot.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()
let wrapper

describe('Wells Nearby', () => {
  let mutations, getters, store
  const well = {
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
  beforeEach(() => {
    mutations = {
      setActiveMapLayers: jest.fn(),
      removeMapLayer: jest.fn(),
      addShape: jest.fn(),
      clearHighlightLayer: jest.fn()
    }
    getters = {
      isMapLayerActive: state => layerId => false,
      activeMapLayers: () => ([]),
      pointOfInterest: () => {
      },
      dataMartFeatures: () => [],
      allMapLayers: () => [],
      getCategories: () => [],
      featureSelectionExists: () => null,
      isMapReady: jest.fn()
    }
    const map = {
      namespaced: true,
      getters,
      mutations
    }
    store = new Vuex.Store({ modules: { map } })
    store.commit = jest.fn()
    wrapper = shallowMount(WellsNearbyBoxPlot, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: {
          geometry: {
            coordinates: [-127.57192816676897, 50.53235018962306],
            type: 'Point'
          }
        },
        wells: [well]
      }
    })
  })

  it('Shows a chart when there\'s data', async () => {
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('.charts').length).toEqual(1)
  })

  it('Shows all three charts when there\'s data', async () => {
    // await wrapper.vm.$nextTick() doesn't work since we need to wait a few
    // secs for the module to be loaded
    setTimeout(() => {
      expect(wrapper.find('.charts').findAll('.chart').length).toEqual(3)
    })
  })
})
