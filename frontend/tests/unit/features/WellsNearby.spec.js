import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WellsNearby from '@/components/analysis/WellsNearby.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

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
  })

  it('Redraws circle on map', () => {
    const wrapper = shallowMount(WellsNearby, {
      vuetify,
      store,
      localVue
    })

    wrapper.setProps({ coordinates: [-122.94492, 50.11588] })
    wrapper.vm.showCircle()
    expect(wrapper.emitted('shapes:reset'.toBeTruthy))
    expect(wrapper.emitted('shapes:add'.toBeTruthy))
  })

  it('Populates Box Plot data', () => {

  })
})
