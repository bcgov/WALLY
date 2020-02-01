import { shallowMount, createLocalVue } from '@vue/test-utils'
import SingleSelectedFeature from '../../../src/components/sidepanel/SingleSelectedFeature.vue'
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
    let mapGetters = {
      isMapLayerActive: state => layerId => false,
      allMapLayers: () => testLayers.layers,
      getCategories: () => testLayers.categories,
      getMapLayer: () => () => ({
        display_data_name: 'test',
        highlight_columns: []
      }),
      map: jest.fn()
    }

    let map = {
      namespaced: true,
      getters: mapGetters,
      mutations
    }

    getters = {
      dataMartFeatureInfo: () => ({
        display_data_name: 'Test title',
        properties: {
          'test prop': 'test value'
        }
      }),
      dataMartFeatures: () => [],
      featureSelectionExists: () => null,
      layerSelectionActive: () => null,
      featureError: () => null,
      loadingFeature: () => null

    }

    store = new Vuex.Store({ modules: { map }, getters })
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
