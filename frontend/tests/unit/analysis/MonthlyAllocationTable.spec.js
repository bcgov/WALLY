import { createLocalVue, mount } from '@vue/test-utils'
import MonthlyAllocationTable
  from '../../../src/components/analysis/surface_water/watershed_demand/MonthlyAllocationTable.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)
Vue.filter('formatNumber', () => 'foo')

const vuetify = new Vuetify()

describe('MonthlyAllocationTable Test', () => {
  let wrapper
  let store

  beforeEach(() => {
    let surfaceWater = {
      namespaced: true,
      getters: {
        allocationValues: () => {}
      },
      mutations: {

      },
      actions: {
        loadAllocationItemsFromStorage: jest.fn()
      }
    }

    store = new Vuex.Store({ modules: { surfaceWater } })
    wrapper = mount(MonthlyAllocationTable, {
      vuetify,
      store,
      localVue,
      propsData: {
        'allocationItems': [
          { 'testKey': 'test 1' },
          { 'testKey': 'test 2' },
          { 'testKey': 'test 3' }
        ],
        'keyField': 'testKey'
      }
    })
  })

  it('Show allocation table', () => {
    console.log(wrapper.findAll('div'))
    expect(wrapper.findAll('div#allocationTable').length).toBe(1)
  })
})
