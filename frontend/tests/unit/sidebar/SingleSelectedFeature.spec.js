import { shallowMount, createLocalVue } from '@vue/test-utils'
import SingleSelectedFeature from '../../../src/components/sidebar/SingleSelectedFeature.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import testLayers from '../../testLayers'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('SingleSelectedFeature', () => {
  let store
  let getters
  let wrapper
  let mutations

  beforeEach(() => {
    mutations = {
      setActiveMapLayers: jest.fn(),
      removeMapLayer: jest.fn(),
      resetDataMartFeatureInfo: jest.fn()
    }
    getters = {
      isMapLayerActive: state => layerId => false,
      dataMartFeatureInfo: () => ({
        display_data_name: 'Test title',
        properties: {
          'test prop': 'test value'
        }
      }),
      dataMartFeatures: () => [],
      allMapLayers: () => testLayers.layers,
      getCategories: () => testLayers.categories,
      featureSelectionExists: () => null,
      getMapLayer: () => () => ({
        display_data_name: 'test',
        highlight_columns: []
      }),
      layerSelectionActive: () => null,
      featureError: () => null,
      loadingFeature: () => null
    }
    store = new Vuex.Store({ getters, mutations })
  })

  it('Single feature card renders title of the feature', () => {
    wrapper = shallowMount(SingleSelectedFeature, {
      vuetify,
      store,
      localVue
    })
    expect(wrapper.text()).toContain('Test title')
  })
})
