import { createLocalVue, shallowMount, mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import WatershedDetails
  from '../../../../src/components/analysis/surface_water/WatershedDetails'

const localVue = createLocalVue()
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
localVue.use(Vuex)

// Fix issue with error: [Vuetify] Unable to locate target [data-app]
// https://forum.vuejs.org/t/vuetify-data-app-true-and-problems-rendering-v-dialog-in-unit-tests/27495/7
document.body.setAttribute('data-app', true)

Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Watershed Details tests', () => {
  let wrapper
  let store
  let getters

  const map = {
    namespaced: true
  }

  getters = {
    isMapLayerActive: state => layerId => false,
    watershedDetails: () => {
      return {
        drainage_area: ''
      }
    },
    customModelInputsActive: () => false,
    scsb2016ModelInputs: () => true
  }
  const surfaceWater = {
    namespaced: true,
    getters
  }

  const initStore = (map, surfaceWater) => {
    store = new Vuex.Store({ modules: { map, surfaceWater } })

    store.dispatch = jest.fn()

    return store
  }

  beforeEach(() => {
    console.error = jest.fn()
  })

  it('Shows all headers of each detail', () => {
    store = initStore(map, surfaceWater)
    wrapper = shallowMount(WatershedDetails, {
      vuetify,
      store,
      localVue,
      propsData: {
        modelOutputs: '',
        watershedName: 'Test Watershed'
      }
    })
    const headers = [
      'Drainage area',
      'Mean Annual Discharge',
      'Total Annual Quantity',
      'Mean Annual Runoff',
      'Low7Q2',
      'Dry7Q10',
      'Annual Precipitation',
      'Glacial Coverage',
      'Median Elevation'
    ]
    const cards = wrapper.findAll('v-card-title-stub')
    cards.wrappers.forEach(card => {
      expect(headers).toContain(card.text())
    })
  })

  it('Shows no value text', async () => {
    store = initStore(map, surfaceWater)
    wrapper = shallowMount(WatershedDetails, {
      vuetify,
      store,
      localVue,
      propsData: {
        modelOutputs: '',
        watershedName: 'Test Watershed'
      }
    })
    const textValues = wrapper.findAll('v-card-title-stub + v-card-text-stub')
    await wrapper.setData({ noValueText: 'No Value Text' })

    textValues.wrappers.forEach((textValue, i) => {
      expect(textValue.text()).toBe(wrapper.vm.noValueText)
    })
  })

  it('Displays a formatted Mean Annual Discharge value', () => {
    surfaceWater.getters.watershedDetails = () => {
      return {
        drainage_area: 123
      }
    }
    store = initStore(map, surfaceWater)
    wrapper = shallowMount(WatershedDetails, {
      vuetify,
      store,
      localVue,
      propsData: {
        modelOutputs: '',
        watershedName: 'Test Watershed'
      }
    })
    const cards = wrapper.findAll('v-card-title-stub')
    const textValues = wrapper.findAll('v-card-text-stub')

    expect(cards.at(1).text()).toBe('Mean Annual Discharge')
    expect(textValues.at(1).text()).toContain('123.00')
    expect(textValues.at(1).text()).toContain('km²')
  })

  it('Opens Model Inputs', async () => {
    store = initStore(map, surfaceWater)
    wrapper = mount(WatershedDetails, {
      vuetify,
      store,
      localVue,
      propsData: {
        modelOutputs: '',
        watershedName: 'Test Watershed'
      }
    })
    const modelInputsButton = wrapper.find('.v-card__actions button')
    await modelInputsButton.trigger('click')
    expect(modelInputsButton.text()).toContain('Model Inputs')
    expect(wrapper.vm.show.editingModelInputs).toBeTruthy()
  })

  it('Shows warning about custom model inputs', () => {
    surfaceWater.getters.customModelInputsActive = () => {
      return true
    }
    store = initStore(map, surfaceWater)
    wrapper = shallowMount(WatershedDetails, {
      vuetify,
      store,
      localVue,
      propsData: {
        modelOutputs: '',
        watershedName: 'Test Watershed'
      }
    })

    expect(wrapper.find('v-alert-stub p').text()
      .replace(/ +(?= )|\n/g, ''))
      .toContain(
        'You are using custom model inputs and not the values supplied ' +
      'by the Wally API.')
  })
})
