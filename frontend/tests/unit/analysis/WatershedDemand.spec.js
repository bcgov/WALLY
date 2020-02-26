import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WatershedDemand
  from '../../../src/components/analysis/surface_water/WatershedDemand'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Watershed Demand tests', () => {
  let wrapper
  let methods = {
    fetchLicenceData: jest.fn()
  }
  beforeEach(() => {
    wrapper = shallowMount(WatershedDemand, {
      vuetify,
      localVue,
      methods
    })
  })

  it('Recomputes demand quantity per month based on allocation values', () => {
    // let totalQtyByPurpose = [
    //   2853594.306,
    //   87330.38399999999,
    //   1991187.42,
    //   159294.99360000002,
    //   30837
    // ]
    //
    // let allocValues = [
    //   [0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833, 0.833],
    //   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    //   [0, 0.01, 0.01, 0.02, 0.1, 0.14, 0.24, 0.24, 0.17, 0.06, 0.01, 0],
    //   [0, 0, 0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0, 0, 0],
    //   [0.25, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25]
    // ]

    let monthlyQty = wrapper.vm.computeQuantityPerMonth(1200, [])
    expect(monthlyQty).toEqual([
      100, 100, 100, 100,
      100, 100, 100, 100,
      100, 100, 100, 100])

    // 25% distribution for the winter months
    monthlyQty = wrapper.vm.computeQuantityPerMonth(1200, [
      3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3])
    expect(monthlyQty).toEqual([
      300, 300, 0, 0,
      0, 0, 0, 0,
      0, 0, 300, 300])

    expect(1).toEqual(1)
  })
})
