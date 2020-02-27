import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import MonthlyAllocationTable
  from '../../../src/components/analysis/surface_water/watershed_demand/MonthlyAllocationTable'
const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Stream apportionment tests', () => {
  let wrapper

  beforeEach(() => {
    let methods = {
      populateTable: jest.fn()
    }
    // store = new Vuex.Store({ modules: { map } })

    wrapper = shallowMount(MonthlyAllocationTable, {
      vuetify,
      // store,
      localVue,
      methods
    })
  })

  it('Table with editable values shows up', () => {
    expect(1).toEqual(1)
  })
})
