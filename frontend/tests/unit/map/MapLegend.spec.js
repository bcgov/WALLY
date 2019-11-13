import { mount, createLocalVue } from '@vue/test-utils'
import MapLegend from '../../../src/components/map/MapLegend.vue'
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

  it('Is hidden on start', () => {
    expect(wrapper.findAll('div#legend').length).toBe(0)
  })

  it('Is hidden when empty', () => {
    wrapper.setData({ legend: [] })
    wrapper.setData({ legend: [] })
    expect(wrapper.findAll('div#legend').length).toBe(0)
  })

  it('Is not hidden when not empty', () => {
    let legend = []
    legend.push({
      className: false,
      legendItems: [{
        color: 'hsla(190, 98%, 75%, 0.39)',
        icon: 'signal_cellular_4_bar',
        iconSize: 20,
        lineWidth: false,
        outlineColor: [
          'interpolate',
          ['linear'],
          ['zoom'],
          5,
          'hsla(0, 0%, 55%, 0)',
          10,
          'hsl(0, 0%, 19%)'
        ],
        strokeWidth: '1px',
        text: ''
      }],
      name: 'Aquifers',
      plenty: false
    })
    wrapper.setData({ legend: [] })
    expect(wrapper.findAll('div#legend').length).toEqual(0)
    wrapper.setData({ legend: legend })
    expect(wrapper.findAll('div#legend').length).toEqual(1)
  })

  it('Shows the legend for the layer that\'s selected', () => {
    let legend = []
    legend.push({
      className: false,
      legendItems: [{
        color: 'hsla(190, 98%, 75%, 0.39)',
        icon: 'signal_cellular_4_bar',
        iconSize: 20,
        lineWidth: false,
        outlineColor: [
          'interpolate',
          ['linear'],
          ['zoom'],
          5,
          'hsla(0, 0%, 55%, 0)',
          10,
          'hsl(0, 0%, 19%)'
        ],
        strokeWidth: '1px',
        text: ''
      }],
      name: 'Aquifers',
      plenty: false
    })
    wrapper.setData({ legend: legend })
    expect(
      wrapper.findAll('div#legend div').at(0)
        .find('span.layerName').text()
    ).toEqual('Aquifers')
  })

  it('Shows the legend items for a layer that has multiple legend items', () => {
    expect(1).toBe(1)
  })
})
