import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Sidebar from '../../src/components/sidebar/Sidebar.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import testLayers from '../testLayers'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('Sidebar', () => {
  describe('Tabs', () => {
    let store
    let getters
    let wrapper

    beforeEach(() => {
      getters = {
        isMapLayerActive: state => layerId => false,
        dataMartFeatureInfo: () => {
        },
        dataMartFeatures: () => [],
        allMapLayers: () => testLayers.layers,
        getCategories: () => testLayers.categories
      }
      store = new Vuex.Store({ getters })
      wrapper = shallowMount(Sidebar, {
        vuetify,
        store,
        localVue
      })
    })

    it('setTabById changes the active tab', () => {
      wrapper.vm.setTabById(2)
      expect(wrapper.vm.active_tab).toBe(2)
    })

    it('sidebar tabs exist', () => {
      expect(wrapper.vm.tabs.length).toBe(3)
    })

    it('created layer categories and children (layers) to be rendered by v-treeview', () => {
      // see test data in ../testLayers.js
      // Test data is loaded into the mocked store getters above. This test is for the computed
      // data that v-treenode uses to render the grouped layers.
      // The first category has one child node.
      expect(wrapper.vm.categories.length).toBe(6)
      expect(wrapper.vm.categories[0].children.length).toBe(1)
    })
  })

  describe('Mutations', () => {
    let store
    let mutations
    let getters
    beforeEach(() => {
      mutations = {
        setActiveMapLayers: jest.fn(),
        removeMapLayer: jest.fn()
      }
      getters = {
        isMapLayerActive: state => layerId => false,
        dataMartFeatureInfo: () => {
        },
        dataMartFeatures: () => [],
        allMapLayers: () => testLayers.layers,
        getCategories: () => testLayers.categories
      }
      store = new Vuex.Store({
        mutations, getters
      })
    })

    it('calls handleSelectLayer and commits correct mutation', () => {
      const wrapper = shallowMount(Sidebar, {
        vuetify,
        store,
        localVue
      })
      let fakeLayerName = 'fake'
      wrapper.vm.handleSelectLayer([fakeLayerName]) // Will fail isMapLayerActive anyway
      expect(mutations.setActiveMapLayers.mock.calls).toHaveLength(1)
      expect(mutations.setActiveMapLayers.mock.calls[0][1])
        .toEqual([fakeLayerName])
    })
  })
})
