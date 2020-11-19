import { createLocalVue, shallowMount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'
// import Router from 'vue-router'

import SurfaceWaterContainer
  from '../../../../src/components/analysis/surface_water/SurfaceWaterContainer'
// import ApiService from '../../../../src/services/ApiService'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue.use(Router)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Surface water tests', () => {
  console.error = jest.fn()

  let getters, actions
  let store
  let wrapper
  let map
  let mapGetters

  beforeEach(() => {
    actions = {
      exitFeature: jest.fn()
    }
  })

  const mountContainer = (layersActive = false, poi = true,
    $route = null) => {
    getters = {
      pointOfInterest: () => {
        if (poi) {
          return {
            geometry: {
              coordinates: []
            }
          }
        } else {
          return null
        }
      },
      app: () => {}
    }

    mapGetters = {
      isMapLayerActive: () => jest.fn().mockImplementation(() => {
        return layersActive
      }),
      isMapReady: () => jest.fn()
    }
    map = {
      namespaced: true,
      getters: mapGetters,
      mutations: {
        setDrawMode: jest.fn(),
        clearSelections: jest.fn(),
        selectPointOfInterest: jest.fn()
      }
    }

    store = new Vuex.Store({
      getters,
      mutations: actions,
      modules: { map }
    })

    store.dispatch = jest.fn()
    wrapper = shallowMount(SurfaceWaterContainer, {
      vuetify,
      store,
      localVue,
      mocks: {
        $route
      }
    })
  }

  it('Loads default layers', () => {
    mountContainer()
    wrapper.vm.loadSurfaceWaterAnalysis()
    expect(wrapper.vm.hydatLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.applicationsLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.licencesLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.fishLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.approvalLayerAutomaticallyEnabled).toBeTruthy()

    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'hydrometric_stream_flow')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'water_rights_applications')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'water_rights_licences')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'fish_observations')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addMapLayer', 'water_approval_points')
  })

  it('Don\'t load layers that are already active', () => {
    mountContainer(true)
    wrapper.vm.loadSurfaceWaterAnalysis()
    expect(wrapper.vm.hydatLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.applicationsLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.licencesLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.fishLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.approvalLayerAutomaticallyEnabled).toBeFalsy()

    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addMapLayer', 'hydrometric_stream_flow')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addMapLayer', 'water_rights_applications')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addMapLayer', 'water_rights_licences')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addMapLayer', 'fish_observations')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addMapLayer', 'water_approval_points')
  })

  it('Deactivate automatically activated layers', () => {
    mountContainer()
    wrapper.vm.loadSurfaceWaterAnalysis()
    expect(wrapper.vm.hydatLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.applicationsLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.licencesLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.fishLayerAutomaticallyEnabled).toBeTruthy()
    expect(wrapper.vm.approvalLayerAutomaticallyEnabled).toBeTruthy()

    wrapper.destroy()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'hydrometric_stream_flow')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_rights_licences')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_rights_applications')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'fish_observations')
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_approval_points')
  })

  it('Don\'t deactivate automatically activated layers', () => {
    mountContainer(true)
    wrapper.vm.loadSurfaceWaterAnalysis()
    expect(wrapper.vm.hydatLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.applicationsLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.licencesLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.fishLayerAutomaticallyEnabled).toBeFalsy()
    expect(wrapper.vm.approvalLayerAutomaticallyEnabled).toBeFalsy()

    wrapper.destroy()
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/removeMapLayer', 'hydrometric_stream_flow')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_rights_licences')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_rights_applications')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/removeMapLayer', 'fish_observations')
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/removeMapLayer', 'water_approval_points')
  })

  it('Loads feature from route coordinates', () => {
    const coords = [-127.57192816676897, 50.53235018962306]
    const route = {
      query: {
        coordinates: coords
      }
    }
    mountContainer(false, false, route)
    wrapper.vm.loadFeature()
    expect(store.dispatch).toHaveBeenCalledWith(
      'map/addFeaturePOIFromCoordinates',
      {
        coordinates: coords,
        layerName: 'point-of-interest'
      })
  })

  it('Doesn\'t load from coordinates if POI is set', () => {
    const coords = [-127.57192816676897, 50.53235018962306]
    const route = {
      query: {
        coordinates: coords
      }
    }
    mountContainer(false, true, route)
    wrapper.vm.loadFeature()
    expect(store.dispatch).not.toHaveBeenCalledWith(
      'map/addFeaturePOIFromCoordinates',
      {
        coordinates: coords,
        layerName: 'point-of-interest'
      })
  })
})
