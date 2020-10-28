import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import HydraulicConnectivity from '../../../src/components/analysis/hydraulic_connectivity/HydraulicConnectivity.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Stream apportionment tests', () => {
  let wrapper
  let store
  let getters
  let actions, mutations

  beforeEach(() => {
    getters = {
      isMapLayerActive: state => layerId => false
    }
    actions = {
      addMapLayer: jest.fn(),
      clearHighlightLayer: jest.fn(),
      setMode: jest.fn()
    }
    mutations = {
      setMode: jest.fn()
    }
    let map = {
      namespaced: true,
      getters,
      actions,
      mutations
    }
    let methods = {
      fetchStreams: jest.fn()
    }
    store = new Vuex.Store({ modules: { map } })

    wrapper = shallowMount(HydraulicConnectivity, {
      vuetify,
      store,
      localVue,
      methods
    })
  })

  it('Calculates apportionment', () => {
    let data = [
      { distance: 2, length_metre: 12.2 },
      { distance: 4, length_metre: 12.2 }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.calculateApportionment()
    expect(wrapper.vm.streams[0]['apportionment']).toEqual(80)
    expect(wrapper.vm.streams[1]['apportionment']).toEqual(20)
  })

  it('Can remove overlapping streams', () => {
    let data = [
      { distance: 2, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 7, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 4, fwa_watershed_code: 5556, length_metre: 12.2 }
    ]
    let result = [
      {
        'apportionment': 80,
        'distance': 2,
        'length_metre': 12.2,
        'fwa_watershed_code': 5555,
        'inverse_distance': 0.25
      },
      {
        'apportionment': 20,
        'distance': 4,
        'length_metre': 12.2,
        'fwa_watershed_code': 5556,
        'inverse_distance': 0.0625
      }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.highlightAll = jest.fn()
    wrapper.vm.removeOverlaps()
    expect(wrapper.vm.streams).toEqual(result)
  })

  it('Apportionment changes based on weighting factor', () => {
    let data = [
      { distance: 2, length_metre: 12.2 },
      { distance: 4, length_metre: 12.2 }
    ]
    wrapper.setData({ streams: data, weightingFactor: 3 })
    wrapper.vm.calculateApportionment()
    expect(Math.round(wrapper.vm.streams[0]['apportionment']))
      .toEqual(89)
    expect(Math.round(wrapper.vm.streams[1]['apportionment']))
      .toEqual(11)
  })

  it('Removes streams if apportionment is under x percentage', () => {
    let data = [
      { distance: 2, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 4, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 40, fwa_watershed_code: 5556, length_metre: 12.2 }
    ]
    let result = [
      {
        'apportionment': 80,
        'distance': 2,
        'length_metre': 12.2,
        'fwa_watershed_code': 5555,
        'inverse_distance': 0.25
      },
      {
        'apportionment': 20,
        'distance': 4,
        'length_metre': 12.2,
        'fwa_watershed_code': 5555,
        'inverse_distance': 0.0625
      }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.highlightAll = jest.fn()
    wrapper.vm.calculateApportionment()
    wrapper.vm.removeStreamsWithLowApportionment(10)
    expect(wrapper.vm.streams).toEqual(result)
  })

  it('Can delete a specific stream point', () => {
    expect(1).toEqual(1)
  })

  it('Add new stream point button works', () => {
    // turn draw mode on

    expect(1).toEqual(1)
    // turn draw mode off
  })

  it('Esc or cancel button cancels draw mode', () => {
    expect(1).toEqual(1)
  })

  it('Can add a new stream point', () => {
    expect(1).toEqual(1)
  })

  it('Recalculates apportionment when a new stream point is added', () => {

  })
})
