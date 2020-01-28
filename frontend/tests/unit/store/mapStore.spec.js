import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as map from '../../../src/store/mapStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Store', () => {
  let store
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
})
