import { createLocalVue, mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import flushPromises from 'flush-promises'
import Vuex from 'vuex'

import StreamApportionment from '../../../src/components/analysis/StreamApportionment.vue'
import testStreams from './testStreams.json'

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
  let propsData

  beforeEach(() => {
    getters = {
      isMapLayerActive: state => layerId => false
    }
    mutations = {
      addMapLayer: jest.fn()
    }
    store = new Vuex.Store({ getters, mutations })
    wrapper = mount(StreamApportionment, {
      vuetify,
      store,
      localVue,
      /* Issue with the sync mode in vue-test-utils
      https://github.com/vuejs/vue-test-utils/issues/1130
      Getting the error(s)
        - TypeError: Cannot read property '$scopedSlots' of undefined
        - TypeError: Cannot read property '$options' of undefined
      */
      sync: false
    })
  })

  propsData = {
    record: {
      'type': 'Feature',
      'properties': {},
      'geometry': {
        'coordinates': [-122.9769538778261, 50.10578278124623],
        'type': 'Point'
      },
      'display_data_name': 'user_defined_point'
    }
  }

  it('Displays streams in a table', async () => {
    expect(wrapper.findAll('tbody tr.v-data-table__empty-wrapper').length)
      .toEqual(1)
    wrapper.setData({ streams: testStreams })
    await flushPromises()
    expect(wrapper.findAll('tbody tr').length).toEqual(3)
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
    wrapper.vm.calculateApportionment()
    wrapper.vm.removeStreamsWithLowApportionment(10)
    expect(wrapper.vm.streams).toEqual(result)
  })
})
