import {mount, shallowMount, createLocalVue} from "@vue/test-utils";
import Sidebar from '../../src/components/Sidebar'
import {MAP_LAYERS} from "../../src/utils/mapUtils";
import Vuex from 'vuex'
import Vuetify from "vuetify";
import Vue from "vue";

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)

describe('Sidebar', () => {

  describe('Tabs', () => {
    let store
    let getters
    let wrapper

    beforeEach(() => {
      getters = {
        isMapLayerActive: state => layerId => false,
        featureInfo: () => {
        },
        featureLayers: () => []
      }
      store = new Vuex.Store({getters})
      wrapper = mount(Sidebar, {
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
  })

  describe('Mutations', () => {
    let store
    let mutations
    let getters
    beforeEach(() => {
      mutations = {
        addMapLayer: jest.fn(),
        removeMapLayer: jest.fn()
      }
      getters = {
        isMapLayerActive: state => layerId => false,
        featureInfo: () => {
        },
        featureLayers: () => []
      }
      store = new Vuex.Store({
        mutations, getters
      })
    })

    it('calls handleSelectLayer and commits correct mutation', () => {
      const wrapper = shallowMount(Sidebar, {
        store,
        localVue
      })
      let fakeLayerName = 'fake'
      wrapper.vm.handleSelectLayer(fakeLayerName) // Will fail isMapLayerActive anyway
      expect(mutations.addMapLayer.mock.calls).toHaveLength(1)
      expect(mutations.addMapLayer.mock.calls[0][1])
        .toEqual(fakeLayerName)
    })
  })

})
