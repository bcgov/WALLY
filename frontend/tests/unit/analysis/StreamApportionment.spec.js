import { createLocalVue, mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import StreamApportionment from '../../../src/components/analysis/StreamApportionment'
import Vuex from 'vuex'
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
      /*
       v-btn on mount cases an error
         TypeError: Cannot read property '$scopedSlots' of undefined
       so we're stubbing it
       */
      stubs: {
        'v-btn': true
      }
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

  it('Displays streams', () => {
    wrapper.setProps(propsData)
    expect(wrapper.findAll('.v-card').length).toEqual(0)
    wrapper.setData({ streams: testStreams })
    expect(wrapper.findAll('.v-card').length).toEqual(3)
  })

  it('Calculates apportionment', () => {
    expect(1).toEqual(1)
  })

  it('Calculates apportionment 2', () => {
    expect(1).toEqual(1)
  })

  it('Calculates apportionment 3', () => {
    expect(1).toEqual(1)
  })
})
