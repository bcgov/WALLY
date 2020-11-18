import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import ComparativeRunoffModels
  from '../../../../src/components/analysis/surface_water/ComparativeRunoffModels'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Comparative Runoff Models test', () => {
  let wrapper
  let store

  beforeEach(() => {
    console.error = jest.fn()
    let map = {
      namespaced: true
    }

    store = new Vuex.Store({ modules: { map } })

    store.dispatch = jest.fn()
  })

  it('Shows annual normalized runoff if available', () => {
    const annualRunoffValue = 123
    // If a watershed has an ANNUAL_RUNOFF_IN_MM, it's from the hydrometric
    // watersheds dataset
    const allWatersheds = [{
      properties: {
        ANNUAL_RUNOFF_IN_MM: annualRunoffValue
      }
    }]

    wrapper = shallowMount(ComparativeRunoffModels, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: null,
        allWatersheds,
        surface_water_design_v2: true
      }
    })
    const cardText = wrapper.find('v-card-text-stub')

    // Annualized runoff is the first v-card-title
    expect(cardText.find('v-card-title-stub').text()).toContain(
      'Annual normalized runoff')
    expect(cardText.find('v-card-text-stub').text()).toContain(
      annualRunoffValue)
  })

  it('Hides annual normalized runoff if unavailable', () => {
    // If a watershed has an ANNUAL_RUNOFF_IN_MM, it's from the hydrometric
    // watersheds dataset
    const allWatersheds = [{
      properties: {
      }
    }]

    wrapper = shallowMount(ComparativeRunoffModels, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: null,
        allWatersheds,
        surface_water_design_v2: true
      }
    })
    const cardText = wrapper.find('v-card-text-stub')

    expect(cardText.text()).not.toContain('Annual normalized runoff')

    // Only the annualized runoff & isolines have v-card-title elementss
    expect(cardText.find('v-card-title-stub').exists()).toBeFalsy()
  })
})
