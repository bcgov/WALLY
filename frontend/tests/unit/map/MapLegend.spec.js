import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import MapLegend from '../../../src/components/map/maplegend/MapLegend.vue'
import StreamAllocationRestrictionsLegendItem from '../../../src/components/map/maplegend/customLegendItems/StreamAllocationRestrictionsLegendItem'
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

  it('Is hidden on start', () => {
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => []
      }
    }
    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => [],
        customLayers: () => { return { children: [] } }
      }
    }
    store = new Vuex.Store({ modules: { map, customLayers } })

    wrapper = mount(MapLegend, {
      vuetify,
      store,
      localVue
    })
    expect(wrapper.findAll('div#legend').length).toBe(0)
  })

  it('Is not hidden when not empty', async () => {
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('div#legend').length).toEqual(0)
    let propsData = {
      map: {
        getLayer: (name) => {
          let types = {
            'ecocat_water_related_reports': 'circle',
            'freshwater_atlas_stream_networks': 'line'
          }
          return types[name]
        },
        getPaintProperty: () => {}
      }
    }
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => [{
          description: 'A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps',
          display_data_name: 'ecocat_water_related_reports',
          display_name: 'EcoCat Water-related Reports',
          highlight_columns: [
            'REPORT_ID',
            'TITLE',
            'SHORT_DESCRIPTION',
            'AUTHOR',
            'DATE_PUBLISHED',
            'REPORT_AUDIENCE',
            'LONG_DESCRIPTION'
          ],
          label: 'Title',
          label_column: 'TITLE',
          layer_category_code: 'REPORTS',
          name: 'Ecological Catalogue (formerly AquaCat)',
          source_url: 'https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat',
          url: '',
          use_wms: true,
          vector_name: '',
          wms_name: 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
          wms_style: ''
        }]
      }
    }
    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => [],
        customLayers: () => { return { children: [] } }
      }
    }
    store = new Vuex.Store({ modules: { map, customLayers } })
    wrapper = mount(MapLegend, {
      vuetify,
      store,
      propsData,
      localVue
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('div#legend').length).toEqual(1)
  })

  it('Shows the legend for the layer that\'s selected', async () => {
    await wrapper.vm.$nextTick()
    expect(
      wrapper.findAll('div#legend div').at(0)
        .find('.layerName').text()
    ).toEqual('EcoCat Water-related Reports')
  })

  it('Shows the legend items for a layer that has multiple legend items', async () => {
    let propsData = {
      map: {
        getLayer: (name) => {
          let types = {
            'ecocat_water_related_reports': 'circle',
            'freshwater_atlas_stream_networks': 'line'
          }
          return types[name]
        },
        getPaintProperty: () => {}
      }
    }
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => [{
          description: 'A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps',
          display_data_name: 'ecocat_water_related_reports',
          display_name: 'EcoCat Water-related Reports',
          highlight_columns: [
            'REPORT_ID',
            'TITLE',
            'SHORT_DESCRIPTION',
            'AUTHOR',
            'DATE_PUBLISHED',
            'REPORT_AUDIENCE',
            'LONG_DESCRIPTION'
          ],
          label: 'Title',
          label_column: 'TITLE',
          layer_category_code: 'REPORTS',
          source_name: 'Ecological Catalogue (formerly AquaCat)',
          source_url: 'https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat',
          url: '',
          use_wms: true,
          vector_name: '',
          wms_name: 'WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW',
          wms_style: ''
        },
        {
          description: 'Flow network arcs (observed, inferred and constructed). Contains no banks, coast or watershed bourdary arcs. Directionalized and connected. Contains heirarchial key and route identifier.',
          display_data_name: 'freshwater_atlas_stream_networks',
          display_name: 'Freshwater Atlas Stream Networks',
          highlight_columns: [
            'STREAM_ORDER',
            'STREAM_MAGNITUDE',
            'FEATURE_LENGTH_M',
            'WATERSHED_GROUP_ID'
          ],
          label: 'Feature ID',
          label_column: 'LINEAR_FEATURE_ID',
          layer_category_code: 'FRESHWATER_MARINE',
          name: 'Freshwater Atlas Stream Networks',
          source_url: 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network',
          url: '',
          use_wms: true,
          vector_name: '',
          wms_name: 'WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP',
          wms_style: '1853'
        }]
      }
    }
    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => [],
        customLayers: () => { return { children: [] } }
      }
    }
    store = new Vuex.Store({ modules: { map, customLayers } })
    wrapper = mount(MapLegend, {
      vuetify,
      store,
      propsData,
      localVue
    })
    await wrapper.vm.$nextTick()

    let layerName = wrapper.findAll('div#legend div').at(0)
      .find('.layerName').text()
    let legendItems = wrapper.findAll('div#legend').at(0)
      .findAll('.legendItem')

    expect(layerName).toEqual('EcoCat Water-related Reports')
    expect(legendItems.length).toEqual(2)
  })

  it('Is collapsible', async () => {
    await wrapper.vm.$nextTick()

    expect(wrapper.findAll('div#legend>.legendItems').length).toEqual(1)

    // Legend is visible when a layer is selected
    expect(wrapper.find('div#legend>.legendItems').isVisible()).toBe(true)

    // Hide legend
    wrapper.find('.v-btn.close').trigger('click')
    await Vue.nextTick()
    expect(wrapper.find('div#legend>.legendItems').isVisible()).toBe(false)

    // Show legend
    wrapper.find('.v-btn.close').trigger('click')
    await Vue.nextTick()
    expect(wrapper.find('div#legend>.legendItems').isVisible()).toBe(true)
  })

  it('Replaces label code', () => {
    let propsData = {
      item: {
        text: 'Stream Allocation Restrictions',
        type: 'line',
        color: 'blue'
      }
    }
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => []
      }
    }

    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => [],
        customLayers: () => { return { children: [] } }
      }
    }
    store = new Vuex.Store({ modules: { map, customLayers } })
    const legendItem = shallowMount(StreamAllocationRestrictionsLegendItem, {
      vuetify,
      store,
      propsData,
      localVue
    })

    let legendText = legendItem.vm.labelLookup('OR')
    expect(legendText).toEqual('Office Reserve')
    legendText = legendItem.vm.labelLookup('FR-EXC')
    expect(legendText).toEqual('Fully Recorded Except')
  })

  it('Returns layers with a display name', async () => {
    await wrapper.vm.$nextTick()
    let propsData = {
      map: {
        getLayer: (name) => {
          let types = {
            'fish_obstacles.geojson.1593556874000': 'Point'
          }
          return types[name]
        },
        getPaintProperty: () => {}
      }
    }
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => []
      }
    }
    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => ['fish_obstacles.geojson.1593556874000', '_imported-map-layers'],
        customLayers: () => {
          return {
            children: [{
              color: '#D2126',
              geomType: 'Point',
              id: 'fish_obstacles.geojson.1593556874000',
              name: 'fish_obstacles'
            }]
          }
        }
      }
    }
    store = new Vuex.Store({ modules: { map, customLayers } })
    wrapper = mount(MapLegend, {
      vuetify,
      store,
      propsData,
      localVue
    })
    await wrapper.vm.$nextTick()
    expect(wrapper.findAll('div#legend').length).toEqual(1)
    let fishObstacles = wrapper.findAll('div#legend').at(0).find('span.layerName')
    expect(fishObstacles.text()).toEqual('Fish obstacles')
  })

  it('Displays the correct colors of the icon', async () => {
    const paints = {
      'freshwater_atlas_stream_networks': {
        'line-color': 'hsl(213, 78%, 55%)'
      },
      'snow_stations': {
        'circle-color': 'hsl(2, 1%, 100%)',
        'circle-stroke-color': 'hsl(140, 95%, 52%)',
        'circle-stroke-width': 1
      }
    }

    const layers = {
      'freshwater_atlas_stream_networks': {
        type: 'line'
      },
      'snow_stations': {
        type: 'circle'
      }
    }
    const streamLayer = {
      display_data_name: 'freshwater_atlas_stream_networks',
      display_name: 'FWA Stream Networks'
    }
    let mapLayers = [streamLayer]
    let propsData = {
      map: {
        getLayer: (name) => {
          return layers[name]
        },
        getPaintProperty: (id, type) => {
          return paints[id][type]
        }
      }
    }
    let map = {
      namespaced: true,
      state: {
        activeMapLayers: []
      },
      getters: {
        activeMapLayers: (state) => state.activeMapLayers
      },
      mutations: {
        setActiveMapLayers: (state, payload) => {
          state.activeMapLayers = payload
        }
      }
    }
    let customLayers = {
      namespaced: true,
      getters: {
        selectedCustomLayers: () => [],
        customLayers: () => {
          return {
            children: [] }
        }
      }
    }

    store = new Vuex.Store({ modules: { map, customLayers } })
    wrapper = mount(MapLegend, {
      vuetify,
      store,
      propsData,
      localVue,
      computed: {
        legend: {
          get () {
            return this.activeMapLayers
          },
          set (val) {
            this.activeMapLayers = val
          }
        }
      }
    })

    // activate a line string layer
    store.commit('map/setActiveMapLayers', mapLayers)
    await wrapper.vm.$nextTick()
    let legendItems = wrapper.findAll('div.legendItem i')

    // expect 1 item in map legend
    // 1 line, blue w/no outline
    expect(legendItems.length).toBe(1)
    let streamIconColor = legendItems.at(0).element.style.getPropertyValue('color')
    let streamIconOutlineColor = legendItems.at(0).element.style.getPropertyValue('-webkit-text-stroke-color')
    expect(streamIconColor).toBe(paints['freshwater_atlas_stream_networks']['line-color'])
    expect(streamIconOutlineColor).toBeFalsy()

    // activate a point layer and a line string layer
    const snowLayer = {
      display_data_name: 'snow_stations',
      display_name: 'Snow Stations'
    }
    mapLayers = [snowLayer, streamLayer]
    store.commit('map/setActiveMapLayers', mapLayers)
    await wrapper.vm.$nextTick()

    // expect 2 items in map legend
    // 1 point, white w/cyan outline
    // 1 line, blue w/no outline
    legendItems = wrapper.findAll('div.legendItem i')
    expect(legendItems.length).toBe(2)
    let snowIconColor = legendItems.at(0).element.style.getPropertyValue('color')
    let snowIconOutlineColor = legendItems.at(0).element.style.getPropertyValue('-webkit-text-stroke-color')
    streamIconColor = legendItems.at(1).element.style.getPropertyValue('color')
    streamIconOutlineColor = legendItems.at(1).element.style.getPropertyValue('-webkit-text-stroke-color')
    expect(snowIconColor).toBe(paints['snow_stations']['circle-color'])
    expect(snowIconOutlineColor).toBe(paints['snow_stations']['circle-stroke-color'])
    expect(streamIconColor).toBe(paints['freshwater_atlas_stream_networks']['line-color'])
    expect(streamIconOutlineColor).toBeFalsy()

    // deactivate snow stations layer
    mapLayers = [streamLayer]
    store.commit('map/setActiveMapLayers', mapLayers)
    await wrapper.vm.$nextTick()

    // expect 1 item in map legend
    // 1 line, blue w/no outline
    legendItems = wrapper.findAll('div.legendItem i')
    streamIconColor = legendItems.at(0).element.style.getPropertyValue('color')
    streamIconOutlineColor = legendItems.at(0).element.style.getPropertyValue('-webkit-text-stroke-color')
    expect(legendItems.length).toBe(1)
    expect(streamIconColor).toBe(paints['freshwater_atlas_stream_networks']['line-color'])
    expect(streamIconOutlineColor).toBeFalsy()
  })
})
