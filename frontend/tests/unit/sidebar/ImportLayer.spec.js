import { shallowMount, createLocalVue } from '@vue/test-utils'
import ImportLayer from '../../../src/components/sidepanel/cards/ImportLayer.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('ImportLayer', () => {
  let store
  let getters, mapGetters, customLayersGetters
  let wrapper
  let map
  let customLayers

  beforeEach(() => {
    mapGetters = {
      map: () => ({})
    }
    customLayersGetters = {
      selectedCustomLayers: () => ([]),
      customLayers: () => {}
    }
    map = {
      namespaced: true,
      getters: mapGetters
    }
    customLayers = {
      namespaced: true,
      getters: customLayersGetters
    }

    getters = {
      app: () => ({
        config: {
          'test prop': 'test value'
        }
      })

    }

    store = new Vuex.Store({ modules: { map, customLayers }, getters })

    store.dispatch = jest.fn()
    wrapper = shallowMount(ImportLayer, {
      vuetify,
      store,
      localVue
    })
  })

  it('determines filetype by extension', () => {
    expect(wrapper.vm.determineFileType('test.geojson')).toBe('geojson')
    expect(wrapper.vm.determineFileType('test.csv')).toBe('csv')
    expect(wrapper.vm.determineFileType('test.test.shp')).toBe('shp')
    expect(wrapper.vm.determineFileType('test.zip')).toBe('shp')
    expect(wrapper.vm.determineFileType('test.json')).toBe('geojson')
  })
})
