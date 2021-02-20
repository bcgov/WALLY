import { createLocalVue, mount } from '@vue/test-utils'
import CrossSectionContainer
  from '../../../../src/components/analysis/cross_section/CrossSectionContainer.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('Wells Cross Section Container Test', () => {
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
      isMapReady: jest.fn(),
      sectionLine: jest.fn(),
      draw: () => {
        return {
          getMode: () => 'draw_line_string'
        }
      },
      map: () => {
        return {
          on: jest.fn(),
          off: jest.fn()
        }
      }
    }
    mapActions = {
      setDrawMode: jest.fn(),
      clearSelections: () => jest.fn(),
      addSelectedFeature: jest.fn(),
      addMapLayer: jest.fn()
    }
    let mapMutations = {
      setMode: jest.fn(),
      replaceOldFeatures: jest.fn(),
      setInfoPanelVisibility: jest.fn(),
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

    let crossSection = {
      getters: {
        sectionLine: jest.fn()
      }
    }

    store = new Vuex.Store({
      getters,
      mutations: {
        setInfoPanelVisibility: jest.fn()
      },
      modules: {
        map,
        crossSection
      }
    })

    store.dispatch = jest.fn()
    wrapper = mount(CrossSectionContainer, {
      vuetify,
      store,
      localVue,
      mocks: {
        $route: {
          query: {
            section_line_A: [-122.77476863552691, 58.81570794611142],
            section_line_B: [-122.76112174608627, 58.808128813596966]
          }
        }
      }
    })
  })

  it('increments drawclick and calls set draw mode', () => {
    wrapper.vm.mapClick({})
    expect(wrapper.vm.drawClickCount).toBe(1)
    wrapper.vm.mapClick({})
    expect(wrapper.vm.drawClickCount).toBe(0)
  })

  it('sets drawmode correctly after second click', () => {
    wrapper.vm.mapClick({})
    wrapper.vm.mapClick({})
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/setDrawMode', 'simple_select')
  })

  it('resets drawClickCount on destroy', () => {
    wrapper.destroy()
    expect(wrapper.vm.drawClickCount).toBe(0)
  })

  it('Loads default layers', () => {
    expect(wrapper.vm.wellsLayerAutomaticallyEnabled).toBeTruthy()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'groundwater_wells')
  })

  it('Deactivate automatically activated layers', () => {
    expect(wrapper.vm.wellsLayerAutomaticallyEnabled).toBeTruthy()
    wrapper.destroy()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'groundwater_wells')
  })

  it('Loads feature from section line coordinates', () => {
    const linestring =
    {
      id: 'user_defined_line',
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: [
          [-122.77476863552691, 58.81570794611142],
          [-122.76112174608627, 58.808128813596966]
        ]
      },
      properties: {
      }
    }

    wrapper.vm.loadFeature()

    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addSelectedFeature',
      linestring
    )
  })
})
