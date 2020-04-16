import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'
import circle from '@turf/circle'

import WellsNearby from '@/components/analysis/wells_nearby/WellsNearby.vue'

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
      removeMapLayer: jest.fn(),
      addShape: jest.fn()
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
    let map = {
      namespaced: true,
      getters,
      mutations
    }
    store = new Vuex.Store({ modules: { map } })
    store.commit = jest.fn()
    wrapper = shallowMount(WellsNearby, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: { geometry: { 'coordinates': [-127.57192816676897, 50.53235018962306], 'type': 'Point' } }
      }
    })
  })

  it('Redraws circle on map', () => {
    wrapper.vm.showCircle()
    expect(store.commit).toHaveBeenCalledWith('map/removeShapes')
    const options = {
      steps: 32,
      units: 'kilometers',
      properties: { display_data_name: 'user_search_radius' }
    }
    const radius = wrapper.vm.radius / 1000
    const shape = circle(wrapper.vm.coordinates, radius, options)
    shape.id = 'user_search_radius'

    expect(store.commit).toHaveBeenCalledWith('map/addShape', shape)
  })

  it('Is hidden when there\'s no data', () => {
    wrapper.setData({ wells: [] })
    expect(wrapper.findAll('#wells_nearby .charts').length).toEqual(0)
  })

  it('Shows a chart when there\'s data', async () => {
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
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('#wells_nearby .charts').length).toEqual(1)
  })

  it('Shows all three charts when there\'s data', async () => {
    // const wrapper = mount(WellsNearby, {
    //   Plotly: Component
    // })
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
    wrapper.setData({ wells: [well], loading: false })
    // await wrapper.vm.$nextTick()
    setTimeout(() => {
      expect(wrapper.find('#wells_charts').findAll('.chart').length).toEqual(3)
    })
  })
})
