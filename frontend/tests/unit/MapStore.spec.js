import { createLocalVue } from '@vue/test-utils'
import { DATA_MARTS } from '../../src/utils/mapUtils'
import Vuex from 'vuex'
import * as map from '../../src/store/mapStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Store', () => {
  let store
  beforeEach(() => {
    store = map.default
  })

  it('adds a new map layer to active map layers', () => {
    const payload = DATA_MARTS[0].id
    store.mutations.addMapLayer(store.state, payload)
    expect(store.state.activeMapLayers[0]).toBe(DATA_MARTS[0])
  })

  it('removes a map layer from active map layers', () => {
    store.state = {
      activeMapLayers: [
        DATA_MARTS[0]
      ]
    }
    const payload = DATA_MARTS[0].id
    store.mutations.removeMapLayer(store.state, payload)
    expect(store.state.activeMapLayers.length).toBe(0)
  })

  it('returns map layer is active', () => {
    store.state = {
      activeMapLayers: [
        DATA_MARTS[0]
      ]
    }
    const payload = DATA_MARTS[0].id
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(true)
  })

  it('returns map layer is not active', () => {
    store.state = {
      activeMapLayers: [
        DATA_MARTS[0]
      ]
    }
    const payload = DATA_MARTS[1].id
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(false)
  })
})
