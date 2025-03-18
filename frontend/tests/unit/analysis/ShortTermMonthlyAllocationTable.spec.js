import { createLocalVue, mount } from '@vue/test-utils'
import ShortTermMonthlyAllocationTable
  from '../../../src/components/analysis/surface_water/watershed_demand/ShortTermMonthlyAllocationTable.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
Vue.filter('formatNumber', () => 'foo')

const vuetify = new Vuetify()

describe('Short Term Monthly Allocation Table Test', () => {
  let wrapper
  let store
  let propsData

  beforeEach(() => {
    const surfaceWater = {
      namespaced: true,
      getters: {
        allocationValues: () => {
          return { 'test 1': [] }
        }
      },
      mutations: {
      },
      actions: {
        loadAllocationItemsFromStorage: jest.fn()
      }
    }

    propsData = {
      allocationItems: [
        { testKey: 'test 1' },
        { testKey: 'test 2' },
        { testKey: 'test 3' }
      ],
      keyField: 'testKey'
    }

    store = new Vuex.Store({ modules: { surfaceWater } })
    wrapper = mount(ShortTermMonthlyAllocationTable, {
      vuetify,
      store,
      localVue,
      propsData
    })
  })

  it('Show allocation table', () => {
    const allocationCard = wrapper.findAll('div#allocationTable')
    expect(allocationCard.length).toBe(1)
  })

  it('Rows for each allocation item', () => {
    const tableRows = wrapper.findAll('table tbody tr')
    expect(tableRows.length).toBe(propsData.allocationItems.length)
  })

  it('Input text fields for each alloc item for each month', () => {
    const inputTextFields = wrapper.findAll('input[type=text]')
    expect(inputTextFields.length).toBe(propsData.allocationItems.length * 12)
  })
})
