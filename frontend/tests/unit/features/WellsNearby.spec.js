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
})
