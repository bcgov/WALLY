import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import Map from '../../src/components/map/Map.vue'
import { DATA_MARTS, WMS_WATER_RIGHTS_LICENSES } from '../../src/utils/metadataUtils'
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
      allMapLayers: () => DATA_MARTS
    }
    store = new Vuex.Store({ getters })
    wrapper = shallowMount(Map, {
      store,
      localVue
    })
  })

  it('adding layer by id adds to activeLayers', () => {
    wrapper.vm.handleAddWMSLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(false)
  })

  it('remove layer by id decreases activeLayers', () => {
    wrapper.vm.handleAddWMSLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(false)
    wrapper.vm.handleRemoveWMSLayer(WMS_WATER_RIGHTS_LICENSES)
    expect(wrapper.vm.activeLayers.WATER_RIGHTS_LICENSES == null).toBe(true)
  })
})
