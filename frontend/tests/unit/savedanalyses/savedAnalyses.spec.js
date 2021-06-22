import { createLocalVue, mount } from '@vue/test-utils'
import SavedAnalysesList
  from '../../../src/components/savedanalyses/SavedAnalysesList'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('Saved Analyses List Tests', () => {
  let wrapper
  let store
  let mapActions
  let getters

  beforeEach(() => {
    getters = {
      app: () => {}
    }
    let mapGetters = {
      isMapLayerActive: state => layerId => false,
      activeMapLayers: state => [],
      isMapReady: jest.fn(),
      map: () => {
        return {
          on: jest.fn(),
          off: jest.fn(),
          fitBounds: jest.fn(),
          map: {
            fitBounds: jest.fn()
          }
        }
      }
    }
    mapActions = {
      setDrawMode: jest.fn(),
      addMapLayer: jest.fn(),
      addFeaturePOIFromCoordinates: jest.fn(),
      updateActiveMapLayers: jest.fn()
    }
    let mapMutations = {
      setMode: jest.fn(),
      setMapReady: () => true
    }
    let map = {
      state: {
        isMapReady: true
      },
      namespaced: true,
      getters: mapGetters,
      actions: mapActions,
      mutations: mapMutations
    }

    let savedAnalyses = {
      state: {
        savedAnalyses: []
      },
      getters: {
        savedAnalyses: state => savedAnalyses
      }
    }

    store = new Vuex.Store({
      getters,
      mutations: {
        setInfoPanelVisibility: jest.fn()
      },
      modules: {
        map,
        savedAnalyses
      }
    })

    store.dispatch = jest.fn()
    wrapper = mount(SavedAnalysesList, {
      vuetify,
      store,
      localVue,
      mocks: {
        $router: {
          push: jest.fn()
        },
        $route: {
          query: {
            section_line_A: [-122.77476863552691, 58.81570794611142],
            section_line_B: [-122.76112174608627, 58.808128813596966]
          }
        }
      }
    })
  })

  it('sets the map bounds', () => {
    let analysis = {
      map_bounds: [[-123, 49], [-123.1, 49.2]],
      geometry: {
        coordinates: [[-123, 49], [-123.1, 49.2]]
      },
      map_layers: [
        { map_layer: 'ground_water_wells' }
      ],
      feature_type: 'section'
    }
    // console.log(store)
    wrapper.vm.runAnalysis(analysis)
    expect(wrapper.vm.map.fitBounds).toHaveBeenCalledWith(analysis.map_bounds)
  })

  it('does not set point of interest on cross section featureType', () => {
    let analysis = {
      map_bounds: [[-123, 49], [-123.1, 49.2]],
      geometry: {
        coordinates: [[-123, 49], [-123.1, 49.2]]
      },
      map_layers: [
        { map_layer: 'ground_water_wells' }
      ],
      feature_type: 'section'
    }
    wrapper.vm.runAnalysis(analysis)
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addFeaturePOIFromCoordinates',
      {
        coordinates: analysis.geometry.coordinates[0],
        layerName: 'point-of-interest'
      })
  })

  it('sets the point of interest on featureTypes other than cross section', () => {
    let analysis = {
      map_bounds: [[-123, 49], [-123.1, 49.2]],
      geometry: {
        coordinates: [[-123.1, 49.2]]
      },
      map_layers: [
        { map_layer: 'ground_water_wells' }
      ],
      feature_type: 'upstream-downstream'
    }
    wrapper.vm.runAnalysis(analysis)
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addFeaturePOIFromCoordinates',
      {
        coordinates: analysis.geometry.coordinates[0],
        layerName: 'point-of-interest'
      })
  })

  it('sets the correct active map layers', () => {
    let analysis = {
      map_bounds: [[-123, 49], [-123.1, 49.2]],
      map_layers: [
        { map_layer: 'ground_water_wells' }
      ],
      geometry: {
        coordinates: [[-123.1, 49.2]]
      },
      feature_type: 'upstream-downstream'
    }
    wrapper.vm.runAnalysis(analysis)
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/updateActiveMapLayers',
      ['ground_water_wells'])
  })
})
