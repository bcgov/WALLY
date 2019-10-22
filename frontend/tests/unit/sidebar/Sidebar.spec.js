import { mount, createLocalVue } from '@vue/test-utils'
import Sidebar from '../../../src/components/sidebar/Sidebar.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import testLayers from '../../testLayers'

// for tests that check which component is loaded
import LayerSelection from '../../../src/components/sidebar/LayerSelection.vue'
import SingleSelectedFeature from '../../../src/components/sidebar/SingleSelectedFeature.vue'
import MultipleSelectedFeatures from '../../../src/components/sidebar/MultipleSelectedFeatures.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('Sidebar', () => {
  let store
  let getters
  let wrapper
  let mutations

  beforeEach(() => {
    // these store functions mimic some of the basic
    // mutations/getters provided in the mapStore and dataMartStore.
    // they are just for setting up some of the conditions that the components
    // being tested require.
    mutations = {
      resetDataMartFeatureInfo: jest.fn()
    }
    getters = {
      isMapLayerActive: state => layerId => false,
      dataMartFeatureInfo: () => {
      },
      dataMartFeatures: () => [],
      allMapLayers: () => testLayers.layers,
      activeMapLayers: () => ([]),
      getCategories: () => testLayers.categories,
      getMapLayer: () => () => ({
        display_data_name: 'test',
        highlight_columns: []
      }),
      layerSelectionActive: () => null,
      featureSelectionExists: () => null,
      featureError: () => null,
      loadingFeature: () => null
    }
  })

  it('Starting app state: Layer selection is visible', () => {
    store = new Vuex.Store({ getters, mutations })
    wrapper = mount(Sidebar, {
      sync: false,
      vuetify,
      store,
      localVue
    })

    expect(wrapper.find(LayerSelection).exists()).toBe(true)
  })

  it('Single feature selected: SingleSelectedFeature card is visible', () => {
    // set up conditions for when single feature automatically displayed
    getters.dataMartFeatureInfo = () => ({
      display_data_name: 'test'
    })
    getters.featureSelectionExists = () => true

    store = new Vuex.Store({ getters, mutations })
    wrapper = mount(Sidebar, {
      sync: false,
      vuetify,
      store,
      localVue
    })

    expect(wrapper.find(SingleSelectedFeature).exists()).toBe(true)
  })
  it('Single feature selected and multiple features selected: SingleSelectedFeature card is still visible', () => {
    getters.dataMartFeatureInfo = () => ({
      display_data_name: 'test'
    })
    getters.dataMartFeatures = () => ([
      {}
    ])
    getters.featureSelectionExists = () => true

    store = new Vuex.Store({ getters, mutations })
    wrapper = mount(Sidebar, {
      sync: false,
      vuetify,
      store,
      localVue
    })

    expect(wrapper.find(SingleSelectedFeature).exists()).toBe(true)
  })
  it('Multiple features selected: MultipleSelectedFeatures card is visible', () => {
    // set up conditions for when single feature automatically displayed

    getters.dataMartFeatures = () => ([
      {}
    ])
    getters.featureSelectionExists = () => true

    store = new Vuex.Store({ getters, mutations })
    wrapper = mount(Sidebar, {
      sync: false,
      vuetify,
      store,
      localVue
    })

    expect(wrapper.find(SingleSelectedFeature).exists()).toBe(false)
    expect(wrapper.find(MultipleSelectedFeatures).exists()).toBe(true)
  })
})
