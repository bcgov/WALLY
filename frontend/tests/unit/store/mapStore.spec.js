import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import router from '../../../src/router'
import * as map from '../../../src/store/mapStore'

const localVue = createLocalVue()
localVue.use(Vuex)

global.config = {
  debug: false
}

describe('Map Store', () => {
  let store

  window._paq = {
    push: jest.fn()
  }
  beforeEach(() => {
    store = map.default
  })

  it('adds a new map layer to active map layers', () => {
    store.state = {
      mapLayers: [{
        display_data_name: 'water_rights_licenses'
      }],
      activeMapLayers: []
    }
    store.commit = jest.fn()
    let payload = 'water_rights_licenses'
    store.actions.addMapLayer(store, payload)
    expect(store.state.activeMapLayers[0]).toEqual({
      display_data_name: 'water_rights_licenses'
    })
  })

  it('removes a map layer from active map layers', () => {
    store.state = {
      mapLayers: [
        { display_data_name: 'water_rights_licenses' }
      ],
      activeMapLayers: [
        { display_data_name: 'water_rights_licenses' }
      ]
    }
    store.dispatch = jest.fn()
    store.commit = jest.fn()
    let payload = 'water_rights_licenses'
    store.actions.removeMapLayer(store, payload)
    expect(store.state.activeMapLayers.length).toBe(0)
  })

  it('returns map layer is active', () => {
    store.state = {
      activeMapLayers: [
        { display_data_name: 'water_rights_licenses' }
      ]
    }
    const payload = 'water_rights_licenses'
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(true)
  })

  it('returns map layer is not active', () => {
    store.state = {
      activeMapLayers: [
        { display_data_name: 'ground_water_wells' }
      ]
    }
    const payload = 'water_rights_licenses'
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(false)
  })

  it('updates active base map layers (remove a layer)', async () => {
    const startingLayers = [
      'national-park',
      'landuse',
      'contour-line',
      'hillshade'
    ]

    const payload = [
      'national-park',
      'landuse',
      'contour-line'
    ]

    store.state.selectedBaseLayers = startingLayers

    store.commit = jest.fn()

    store.actions.setActiveBaseMapLayers(store, payload)
    await localVue.nextTick()
    expect(store.state.selectedBaseLayers.length).toBe(3)
    expect(store.commit).toHaveBeenCalledWith('deactivateBaseLayer', 'hillshade')
  })

  it('updates active base map layers (add a layer)', async () => {
    const startingLayers = [
      'national-park',
      'landuse',
      'contour-line'
    ]

    const payload = [
      'national-park',
      'landuse',
      'contour-line',
      'hillshade'
    ]

    store.state.selectedBaseLayers = startingLayers

    store.commit = jest.fn()

    store.actions.setActiveBaseMapLayers(store, payload)
    await localVue.nextTick()
    expect(store.state.selectedBaseLayers.length).toBe(4)
    expect(store.commit).toHaveBeenCalledWith('activateBaseLayer', 'hillshade')
  })

  it('getMapLayer returns a map layer', () => {
    const testMapLayers = [
      { display_data_name: 'test1' },
      { display_data_name: 'test2' }
    ]

    store.state.mapLayers = testMapLayers

    // test that getMapLayer('test1') returns the object that has
    // display_data_name = test1.
    expect(store.getters.getMapLayer(store.state)('test1').display_data_name).toBe('test1')
  })

  it('updateActiveMapLayers with 1 new layer triggers the mutation to add a new layer', () => {
    store.commit = jest.fn()
    store.state.activeMapLayers = [
      { display_data_name: 'test1', display_name: 'Test 1' },
      { display_data_name: 'test2', display_name: 'Test 2' }
    ]

    store.state.mapLayers = [
      { display_data_name: 'test3', display_name: 'Test3' }
    ]
    store.state.draw = {
      getAll: jest.fn()
    }
    store.actions.updateActiveMapLayers(store, ['test3'])
    expect(store.commit).toHaveBeenCalledWith('activateLayer', 'test3')
  })

  it('addActiveSelection commits the new feature to state', () => {
    const testFeatureCollection = { features: [
      {
        id: 'testFeature',
        geometry: {
          type: 'Polygon' // mimic a drawn rectangle
        }
      }
    ] }

    store.commit = jest.fn()

    store.actions.addActiveSelection(store, { featureCollection: testFeatureCollection })
    expect(store.commit).toHaveBeenCalledWith('replaceOldFeatures', testFeatureCollection.features[0].id)
    expect(store.commit).toHaveBeenCalledWith('setSelectionBoundingBox', testFeatureCollection.features[0], { root: true })
  })

  it('addActiveSelection called with a Point creates new Point of Interest object', () => {
    const testFeatureCollection = { features: [
      {
        id: 'testFeature',
        geometry: {
          type: 'Point'
        }
      }
    ] }

    store.commit = jest.fn()

    store.actions.addActiveSelection(store, { featureCollection: testFeatureCollection })
    expect(store.commit).toHaveBeenCalledWith('setPointOfInterest', testFeatureCollection.features[0], { root: true })
  })

  it('addActiveSelection called with a LineString creates a new cross section line', () => {
    const testFeatureCollection = { features: [
      {
        id: 'testFeature',
        geometry: {
          type: 'LineString'
        }
      }
    ] }

    store.commit = jest.fn()

    store.actions.addActiveSelection(store, { featureCollection: testFeatureCollection })
    expect(testFeatureCollection.features[0].display_data_name).toBe('user_defined_line')
    expect(store.commit).toHaveBeenCalledWith('setSectionLine', testFeatureCollection.features[0], { root: true })
  })

  // note: these getter tests don't test much code,
  // but our app depends on these key map resources being accessible
  // through the store getters.
  it('[getters] map returns the map object', () => {
    store.state.map = { test: 'test map mock' }
    expect(store.getters.map(store.state) === store.state.map).toBe(true)
  })
  it('[getters] draw returns the draw object', () => {
    expect(store.getters.draw(store.state) === store.state.draw).toBe(true)
  })
  it('[getters] geocoder returns the geocoder object', () => {
    expect(store.getters.geocoder(store.state) === store.state.geocoder).toBe(true)
  })
  it('[getters] baseMapLayers returns the baseMapLayers list', () => {
    expect(store.getters.baseMapLayers(store.state) === store.state.baseMapLayers).toBe(true)
  })
  it('[getters] allMapLayers returns the mapLayers list', () => {
    expect(store.getters.allMapLayers(store.state) === store.state.mapLayers).toBe(true)
  })
  it('[getters] highlightFeatureData returns the highlightFeatureData object', () => {
    expect(store.getters.highlightFeatureData(store.state) === store.state.highlightFeatureData).toBe(true)
  })
  it('[getters] highlightFeatureCollectionData returns the highlightFeatureCollectionData object', () => {
    expect(store.getters.highlightFeatureCollectionData(store.state) === store.state.highlightFeatureCollectionData).toBe(true)
  })
  it('[getters] layerSelectionActive returns the layerSelectionActive object', () => {
    expect(store.getters.layerSelectionActive(store.state) === store.state.layerSelectionActive).toBe(true)
  })
})
