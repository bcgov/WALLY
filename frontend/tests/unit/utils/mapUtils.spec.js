// import Vue from 'vue'
// import Vuetify from 'vuetify'
// import Vuex from 'vuex'
//
// Vue.use(Vuetify)
// const localVue = createLocalVue()
// localVue.use(Vuex)

import {
  addMapboxLayer, addMapboxVectorSource,
  findWallyLayer,
  findWallyLayerArray
} from '../../../src/common/utils/mapUtils'
import {
  SOURCE_CUSTOM_SHAPE_DATA, SOURCE_STREAM_APPORTIONMENT,
  SOURCE_WATER_LICENCES
} from '../../../src/common/mapbox/sourcesWally'
import { vectorSource } from '../../../src/common/mapbox/features'

describe('Map Utils', () => {
  beforeEach(function () {
    console.error = jest.fn()
  })

  it('Finds a layer object', () => {
    const layer = findWallyLayer(SOURCE_CUSTOM_SHAPE_DATA)
    expect(layer.id).toBe('customShape')
    expect(layer.type).toBe('fill')
  })

  it('Finds a layer factory and sets params', () => {
    const layerFn = findWallyLayer(SOURCE_WATER_LICENCES)

    expect(typeof layerFn).toBe('function')
    const data = {}
    const layer = layerFn(data, 10)

    expect(layer.id).toBe('waterLicences')
    expect(layer.paint['circle-radius'][6]).toBe(25)
    expect(layer.source.data).toEqual(data)
  })

  it('Throws an error when a single object cannot be found', () => {
    const layer = findWallyLayer(SOURCE_STREAM_APPORTIONMENT)
    expect(console.error).toHaveBeenCalled()
    expect(layer).toBeUndefined()
  })

  it('Finds an array of layers', () => {
    const layer = findWallyLayerArray(SOURCE_STREAM_APPORTIONMENT)
    expect(Array.isArray(layer)).toBeTruthy()
    expect(layer.length).toBeGreaterThan(1)

    expect(layer[0].id).toBeDefined()
  })

  it('Finds an array of one layer', () => {
    const layer = findWallyLayerArray(SOURCE_CUSTOM_SHAPE_DATA)
    expect(Array.isArray(layer)).toBeTruthy()
    expect(layer.length).toEqual(1)
    expect(layer[0].id).toBeDefined()
  })

  it('Adds a layer with style to the map', () => {
    const map = {
      addLayer: jest.fn()
    }
    addMapboxLayer(map, SOURCE_STREAM_APPORTIONMENT, {})
    const layers = findWallyLayerArray(SOURCE_STREAM_APPORTIONMENT)
    layers.forEach(layer => {
      expect(map.addLayer).toHaveBeenCalledWith(layer)
    })
  })

  it('Adds a layer before a layer with style to the map', () => {
    const map = {
      addLayer: jest.fn()
    }
    addMapboxLayer(map, SOURCE_CUSTOM_SHAPE_DATA, { before: 'test_before' })
    const layers = findWallyLayerArray(SOURCE_CUSTOM_SHAPE_DATA)
    layers.forEach(layer => {
      expect(map.addLayer).toHaveBeenCalledWith(layer, 'test_before')
    })
  })

  it('Adds a vector layer', () => {
    const map = {
      addLayer: jest.fn()
    }
    const layerID = 'water_rights_licences'
    const sourceLayer = 'sourceURL'
    addMapboxLayer(map, layerID, { sourceLayer: sourceLayer })
    const layers = findWallyLayerArray(layerID)
    layers.forEach(layer => {
      expect(layer['source-layer']).toEqual(sourceLayer)
    })
  })
})
