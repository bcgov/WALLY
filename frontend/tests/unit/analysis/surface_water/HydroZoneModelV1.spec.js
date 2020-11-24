import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import HydroZoneModelV1
  from '../../../../src/components/analysis/surface_water/ComparitiveRunoffModels/HydroZoneModelV1'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('HydroZoneModelV1', () => {
  let wrapper
  let store

  beforeEach(() => {
    console.error = jest.fn()
    console.log = jest.fn()
    let map = {
      namespaced: true
    }

    store = new Vuex.Store({ modules: { map } })

    store.dispatch = jest.fn()
  })

  it('does not display Wally model if feature flag off', () => {
    let getters = {
      app: () => ({
        config: {
          wally_model: false
        }
      })
    }
    let map = {
      namespaced: true
    }
    let surfaceWater = {
      namespaced: true,
      getters: {
        watershedDetails: () => ({})
      }
    }
    store = new Vuex.Store({ modules: { map, surfaceWater }, getters })
    wrapper = shallowMount(HydroZoneModelV1, {
      vuetify,
      store,
      localVue,
      propsData: {
        watershedDetails: {}
      }
    })
    const v1 = wrapper.find('#hydroZoneModelV1')

    expect(v1.exists()).toBeFalsy()
  })
  it('displays Wally model if feature flag off', () => {
    let getters = {
      app: () => ({
        config: {
          wally_model: true
        }
      })
    }
    let map = {
      namespaced: true
    }
    let surfaceWater = {
      namespaced: true,
      getters: {
        watershedDetails: () => ({})
      }
    }
    store = new Vuex.Store({ modules: { map, surfaceWater }, getters })
    wrapper = shallowMount(HydroZoneModelV1, {
      vuetify,
      store,
      localVue,
      propsData: {
        watershedDetails: {}
      }
    })
    const v1 = wrapper.find('#hydroZoneModelV1')

    expect(v1.exists()).toBeTruthy()
  })
})
