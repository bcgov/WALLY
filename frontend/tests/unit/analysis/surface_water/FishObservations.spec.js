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
  })

  const mountContainer = () => {
    wrapper = shallowMount(FishObservations, {
      vuetify,
      store,
      localVue,
      propsData: {
        watershedID: '',
        surface_water_design_v2: true
      }
    })
  }

  it('Toggles layer visibility', () => {
    mountContainer()
    wrapper.vm.isFishLayerVisible = true
    wrapper.vm.toggleLayerVisibility()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer',
      'fish_observations')
  })

  it('Shows fish data', async () => {
    mountContainer()
    await wrapper.setData({
      fishData: {
        fish_species_data: [{
          qty: 2,
          species: 'Test',
          count: 2,
          life_stages: 'test',
          observation_date_min: '',
          observation_date_max: ''
        }]
      }
    })
    const dataTable = wrapper.find('v-data-table-stub')
    expect(dataTable.exists()).toBeTruthy()
  })

  it('Doesn\'t show fish data', () => {
    mountContainer()
    const dataTable = wrapper.find('v-data-table-stub')
    expect(dataTable.exists()).toBeFalsy()
  })
})
