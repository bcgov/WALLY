import { shallowMount, createLocalVue } from '@vue/test-utils'
import LayerSelection from '../../../src/components/sidebar/LayerSelection.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import testLayers from '../../testLayers'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('LayerSelection', () => {
  let store
  let getters
  let wrapper
  let mutations

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
      allMapLayers: () => testLayers.layers,
      getCategories: () => testLayers.categories,
      featureSelectionExists: () => null,
      baseMapLayers: () => [],
      selectedBaseLayers: () => []
    }
    store = new Vuex.Store({ getters, mutations })
    wrapper = shallowMount(LayerSelection, {
      vuetify,
      store,
      localVue
    })
  })

  it('created layer categories and children (layers) to be rendered by v-treeview', () => {
    // see test data in ../testLayers.js
    // Test data is loaded into the mocked store getters above. This test is for the computed
    // data that v-treenode uses to render the grouped layers.
    // The first category has one child node.
    expect(wrapper.vm.categories.length).toBe(6)
    expect(wrapper.vm.categories[0].children.length).toBe(1)
  })
  it('calls handleSelectLayer and commits correct mutation', () => {
    let fakeLayerName = 'fake'
    wrapper.vm.handleSelectLayer([fakeLayerName]) // Will fail isMapLayerActive anyway
    expect(mutations.setActiveMapLayers.mock.calls).toHaveLength(1)
    expect(mutations.setActiveMapLayers.mock.calls[0][1])
      .toEqual([fakeLayerName])
  })
})
