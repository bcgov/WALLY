import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import StreamApportionment from '../../../src/components/analysis/StreamApportionment.vue'

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
  let mutations

  beforeEach(() => {
    getters = {
      isMapLayerActive: state => layerId => false
    }
    mutations = {
      addMapLayer: jest.fn()
    }
    let map = {
      namespaced: true,
      getters,
      mutations
    }
    let methods = {
      fetchStreams: jest.fn()
    }
    // store = new Vuex.Store({ getters, mutations })
    store = new Vuex.Store({ modules: { map } })

    wrapper = shallowMount(StreamApportionment, {
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
    wrapper.vm.highlightStreams = jest.fn()
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
    wrapper.vm.highlightStreams = jest.fn()
    wrapper.vm.calculateApportionment()
    wrapper.vm.removeStreamsWithLowApportionment(10)
    expect(wrapper.vm.streams).toEqual(result)
  })
})
