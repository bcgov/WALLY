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
  let actions, mutations, getters, store
  beforeEach(() => {
    actions = {
      clearHighlightLayer: jest.fn()
    }
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
    const map = {
      namespaced: true,
      actions,
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
        record: { geometry: { coordinates: [-127.57192816676897, 50.53235018962306], type: 'Point' } }
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

  it('Doesn\'t display a boxplot for Aquifer 1143', async () => {
    wrapper.setData({
      wellsByAquifer: {
        1143: [{
          well_tag_number: 111,
          latitude: 1,
          longitude: -1,
          well_yield: 1,
          diameter: '1.0',
          well_yield_unit: 'GPM',
          finished_well_depth: 111,
          street_address: '',
          intended_water_use: 'Unknown Well Use',
          aquifer_subtype: null,
          aquifer_hydraulically_connected: null,
          aquifer_id: null,
          aquifer_lithology: 'Unconsolidated',
          aquifer: {
            aquifer_id: 1143,
            subtype: null,
            subtype_desc: null,
            material: null,
            material_desc: null
          },
          screen_set: [],
          top_of_screen: null,
          top_of_screen_type: null,
          distance: 500,
          static_water_level: 10,
          swl_to_screen: null,
          swl_to_bottom_of_well: 10
        }],
        57: [{
          well_tag_number: 111,
          latitude: 1,
          longitude: -1,
          well_yield: 1,
          diameter: '1.0',
          well_yield_unit: 'GPM',
          finished_well_depth: 111,
          street_address: '',
          intended_water_use: 'Unknown Well Use',
          aquifer_subtype: null,
          aquifer_hydraulically_connected: true,
          aquifer_id: null,
          aquifer_lithology: 'Unconsolidated',
          aquifer: {
            aquifer_id: 57,
            subtype: 'aa',
            subtype_desc: 'Gravel',
            material: 'SG',
            material_desc: 'Sand and Gravel'
          },
          screen_set: [],
          top_of_screen: null,
          top_of_screen_type: null,
          distance: 500,
          static_water_level: 10,
          swl_to_screen: null,
          swl_to_bottom_of_well: 10
        }]
      }
    })
    await wrapper.vm.$nextTick()
    const wellsByAquifer = wrapper.findAll('#wells_nearby .wells-by-aquifer')

    const aquifer57 = wellsByAquifer.at(0)
    expect(aquifer57.html()).toContain('Aquifer: 57')
    expect(aquifer57.find('.alert').exists()).toBe(false)

    const aquifer1143 = wellsByAquifer.at(1)
    expect(aquifer1143.find('p').text()).toContain(
      'Wells not correlated to an aquifer at time of interpretation ' +
      'due to insufficient information.'
    )
    expect(aquifer1143.html()).toContain('Aquifer: 1143')
  })
})
