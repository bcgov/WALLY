import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import FishObservations
  from '../../../../src/components/analysis/surface_water/FishObservations'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Fish Observation tests', () => {
  let wrapper
  let store

  beforeEach(() => {
    console.error = jest.fn()
    let map = {
      namespaced: true
    }

    store = new Vuex.Store({ modules: { map } })

    store.dispatch = jest.fn()
    wrapper = shallowMount(FishObservations, {
      vuetify,
      store,
      localVue,
      propsData: {
        watershedID: '',
        surface_water_design_v2: true
      }
    })
  })
  it('Toggles layer visibility', () => {
    wrapper.vm.isFishLayerVisible = true
    wrapper.vm.toggleLayerVisibility()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer',
      'fish_observations')
  })
})
