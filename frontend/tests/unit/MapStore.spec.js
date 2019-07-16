import {mount, shallowMount, createLocalVue} from "@vue/test-utils";
import Sidebar from '../../src/components/Sidebar'
import {MAP_LAYERS} from "../../src/utils/mapUtils";
import Vuex from 'vuex'
import Vue from "vue";
import * as map from '../../src/store/mapStore'
import * as wms from '../../src/store/wmsStore'
import * as data from '../../src/store/dataStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Store', () => {
  let store
  beforeEach(() => {
    store = map.default
  })

  it('adds a new map layer to active map layers', () => {
    const payload = MAP_LAYERS[0].id
    store.mutations.addMapLayer(store.state, payload)
    expect(store.state.activeMapLayers[0]).toBe(MAP_LAYERS[0])
  })

  it('removes a map layer from active map layers', () => {
    store.state = {
      activeMapLayers: [
        MAP_LAYERS[0]
      ]
    }
    const payload = MAP_LAYERS[0].id
    store.mutations.removeMapLayer(store.state, payload)
    expect(store.state.activeMapLayers.length).toBe(0)
  })

  it('returns map layer is active', () => {
    store.state = {
      activeMapLayers: [
        MAP_LAYERS[0]
      ]
    }
    const payload = MAP_LAYERS[0].id
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(true)
  })

  it('returns map layer is not active', () => {
    store.state = {
      activeMapLayers: [
        MAP_LAYERS[0]
      ]
    }
    const payload = MAP_LAYERS[1].id
    expect(store.getters.isMapLayerActive(store.state)(payload)).toBe(false)
  })
})
