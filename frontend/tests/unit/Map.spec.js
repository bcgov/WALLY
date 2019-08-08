import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Map from '../../src/components/map/Map.vue'
import { MAP_LAYERS, WMS_WATER_RIGHTS_LICENSES } from '../../src/utils/mapUtils'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Object Tests', () => {
  it('has a map attribute', () => {
    const wrapper = mount(Map, {
      attachToDocument: true
    })
    expect(wrapper.attributes('id')).toBe('map')
  })

  it('has a map object that is not null', () => {
    const wrapper = mount(Map)
    expect(wrapper.vm.map == null).toBe(false)
  })
})

describe('Map Layer Tests', () => {
  let store
  let getters
  let wrapper

  beforeEach(() => {
    getters = {
      allMapLayers: () => MAP_LAYERS
    }
    store = new Vuex.Store({ getters })
    wrapper = shallowMount(Map, {
      store,
      localVue
    })
  })

  it('adding layer by id adds to activeLayers', () => {
    wrapper.vm.handleAddLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(false)
  })

  it('remove layer by id decreases activeLayers', () => {
    wrapper.vm.handleAddLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(false)
    wrapper.vm.handleRemoveLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(true)
  })
})
