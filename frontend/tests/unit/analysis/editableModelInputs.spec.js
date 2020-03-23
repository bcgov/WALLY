import { createLocalVue, mount } from '@vue/test-utils'
import EditableModelInputs
  from '../../../src/components/analysis/surface_water/EditableModelInputs.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
Vue.filter('formatNumber', () => 'foo')

const vuetify = new Vuetify()

describe('EditableModelInputs Test', () => {
  let wrapper
  let store
  let propsData

  beforeEach(() => {
    let surfaceWater = {
      namespaced: true,
      getters: {
        watershedDetails: () => { return {} },
        scsb2016ModelInputs: () => { 
          return {
            hydrological_zone: 25,
            median_elevation: 700,
            glacial_coverage: 0.2,
            annual_precipitation: 2500,
            evapo_transpiration: 0.67,
            drainage_area: 52,
            solar_exposure: 0.65,
            average_slope: 9
          }
        }
      },
      mutations: {
      },
      actions: {
      }
    }

    store = new Vuex.Store({ modules: { surfaceWater } })
    wrapper = mount(EditableModelInputs, {
      vuetify,
      store,
      localVue
    })
  })

  it('Show editableModelCard', () => {
    let modelCard = wrapper.findAll('div#editableModelCard')
    expect(modelCard.length).toBe(1)
  })

})
