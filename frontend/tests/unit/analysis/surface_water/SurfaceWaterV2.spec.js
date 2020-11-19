import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'
// import Router from 'vue-router'

import SurfaceWaterV2
  from '../../../../src/components/analysis/surface_water/SurfaceWaterV2'

// import ApiService from '../../../../src/services/ApiService'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue.use(Router)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Surface water tests', () => {
  console.error = jest.fn()

  let getters
  let store
  let wrapper
  let map
  let mapGetters
  const $router = {
    push: jest.fn()
  }
  beforeEach(() => {
    getters = {
      pointOfInterest: () => {
        return {
          geometry: {
            coordinates: []
          }
        }
      }
    }

    let surfaceWater = {
      namespaced: true,
      getters: {
        watershedDetails: () => {},
        customModelInputsActive: () => {},
        scsb2016ModelInputs: () => {}
      }
    }
    mapGetters = {
      map: () => {
        return {
          addLayer: jest.fn()
        }
      }
    }
    map = {
      namespaced: true,
      getters: mapGetters,
      mutations: {
        setMode: jest.fn()
      }
    }
    store = new Vuex.Store({ getters, modules: { surfaceWater, map } })
    store.commit = jest.fn()
  })

  it('Add Single Watershed', () => {
    wrapper = shallowMount(SurfaceWaterV2, {
      vuetify,
      store,
      localVue,
      mocks: {
        $router
      }
    })
    wrapper.vm.addSingleWatershedLayer({}, 'new_watershed')

    expect(wrapper.vm.map.addLayer).toHaveBeenCalledTimes(1)
  })

  it('Shows modelling warning', () => {
    wrapper = shallowMount(SurfaceWaterV2, {
      vuetify,
      store,
      localVue,
      mocks: {
        $router
      }
    })
    const modellingAlert = wrapper.find('v-alert-stub')
    expect(modellingAlert.text()).toContain('This modelling output has not been peer reviewed')
  })

  it('Lists all the tabs', async () => {
    wrapper = shallowMount(SurfaceWaterV2, {
      vuetify,
      store,
      localVue,
      mocks: {
        $router
      }
    })
    const watershedName = 'My Watershed'
    await wrapper.setData({
      selectedWatershed: 1,
      watersheds: [
        {
          id: 1,
          properties: {
            name: watershedName
          }
        }
      ]
    })
    await wrapper.setData({
      watershedDetailsLoading: false
    })

    const tabsWrappers = wrapper.findAll('.watershedInfo v-tab-stub')

    const tabs = [
      'Watershed',
      'Monthly Discharge',
      'Hydrometric Stations',
      'Licenced Quantity',
      'Streamflow Report',
      'Runoff Models',
      'Fish Observations'
    ]
    tabsWrappers.wrappers.forEach(tab => {
      expect(tabs).toContain(tab.text())
    })
  })
})
