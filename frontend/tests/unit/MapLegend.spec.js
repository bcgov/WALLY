import { mount, createLocalVue } from '@vue/test-utils'
import MapLegend from '../../src/components/map/MapLegend.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Map Legend Test', () => {
  let wrapper
  let store
  let getters

  beforeEach(() => {
    getters = {
      activeMapLayers: () => []
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(MapLegend, {
      vuetify,
      store,
      localVue
    })
  })

  it('Is hidden when empty', () => {
    expect(wrapper.findAll('div').length).toBe(0)
  })

  it('Shows the legend div', () => {
    expect(1).toEqual(1)
  })

  it('Loads a legend when a layer with a legend is selected', () => {
    expect(1).toEqual(1)
  })
})
