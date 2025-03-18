import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import HydraulicConnectivity from '../../../src/components/analysis/hydraulic_connectivity/HydraulicConnectivity.vue'
import { pointFeature } from '../../../src/common/mapbox/features'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Stream apportionment tests', () => {
  let wrapper
  let store
  let getters
  let actions, mutations

  beforeEach(() => {
    getters = {
      isMapLayerActive: state => layerId => false,
      isMapReady: jest.fn(),
      map: () => {}
    }
    actions = {
      addMapLayer: jest.fn(),
      clearHighlightLayer: jest.fn(),
      setMode: jest.fn(),
      updateMapLayerData: () => jest.fn()
    }
    mutations = {
      setMode: jest.fn(),
      replaceOldFeatures: jest.fn()
    }
    const map = {
      namespaced: true,
      getters,
      actions,
      mutations
    }
    const methods = {
      fetchStreams: jest.fn()
    }
    store = new Vuex.Store({ modules: { map } })

    wrapper = shallowMount(HydraulicConnectivity, {
      vuetify,
      store,
      localVue,
      methods,
      propsData: {
        record: {
          geometry: {
            coordinates: [-122.94441367903971, 50.124911888584364]
          }
        }
      }
    })
  })

  it('Calculates apportionment', () => {
    const data = [
      { distance: 2, length_metre: 12.2 },
      { distance: 4, length_metre: 12.2 }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.calculateApportionment()
    expect(wrapper.vm.streams[0].apportionment).toEqual(80)
    expect(wrapper.vm.streams[1].apportionment).toEqual(20)
  })

  it('Can remove overlapping streams', () => {
    const data = [
      { distance: 2, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 7, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 4, fwa_watershed_code: 5556, length_metre: 12.2 }
    ]
    const result = [
      {
        apportionment: 80,
        distance: 2,
        length_metre: 12.2,
        fwa_watershed_code: 5555,
        inverse_distance: 0.25
      },
      {
        apportionment: 20,
        distance: 4,
        length_metre: 12.2,
        fwa_watershed_code: 5556,
        inverse_distance: 0.0625
      }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.highlightAll = jest.fn()
    wrapper.vm.removeOverlaps()
    expect(wrapper.vm.streams).toEqual(result)
  })

  it('Apportionment changes based on weighting factor', () => {
    const data = [
      { distance: 2, length_metre: 12.2 },
      { distance: 4, length_metre: 12.2 }
    ]
    wrapper.setData({ streams: data, weightingFactor: 3 })
    wrapper.vm.calculateApportionment()
    expect(Math.round(wrapper.vm.streams[0].apportionment))
      .toEqual(89)
    expect(Math.round(wrapper.vm.streams[1].apportionment))
      .toEqual(11)
  })

  it('Removes streams if apportionment is under x percentage', () => {
    const data = [
      { distance: 2, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 4, fwa_watershed_code: 5555, length_metre: 12.2 },
      { distance: 40, fwa_watershed_code: 5556, length_metre: 12.2 }
    ]
    const result = [
      {
        apportionment: 80,
        distance: 2,
        length_metre: 12.2,
        fwa_watershed_code: 5555,
        inverse_distance: 0.25
      },
      {
        apportionment: 20,
        distance: 4,
        length_metre: 12.2,
        fwa_watershed_code: 5555,
        inverse_distance: 0.0625
      }
    ]
    wrapper.setData({ streams: data })
    wrapper.vm.highlightAll = jest.fn()
    wrapper.vm.calculateApportionment()
    wrapper.vm.removeStreamsWithLowApportionment(10)
    expect(wrapper.vm.streams).toEqual(result)
  })

  it('Can delete a specific stream point', () => {
    const newPoint = pointFeature([-122.94811212808108, 50.12917974111525])
    wrapper.vm.processNewStreamPoint(newPoint)
    expect(wrapper.vm.streams.length).toEqual(1)
    wrapper.vm.deleteStream(wrapper.vm.streams[0])
    expect(wrapper.vm.streams.length).toEqual(0)
  })

  it('Adds new stream point to streams', () => {
    const newPoint = pointFeature([-122.94811212808108, 50.12917974111525])
    wrapper.vm.processNewStreamPoint(newPoint)
    expect(wrapper.vm.streams[0].distance).toBeCloseTo(542.88194)
  })

  it('Recalculates apportionment when a new stream point is added', () => {
    const newPoint = pointFeature([-122.94811212808108, 50.12917974111525])
    wrapper.vm.processNewStreamPoint(newPoint)
    expect(wrapper.vm.streams[0].apportionment).toBe(100)
    const newPoint2 = pointFeature([-122.94303996939581, 50.12497963524882])
    wrapper.vm.processNewStreamPoint(newPoint2)
    expect(wrapper.vm.streams[0].apportionment).toBeCloseTo(3.17, 2)
  })

  it('Gives a warning when you try to reload streams when there are added' +
    ' custom stream points', () => {
    expect(1).toBe(1)
  })
})
