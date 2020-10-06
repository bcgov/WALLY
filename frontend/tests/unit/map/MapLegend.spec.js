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

  // beforeEach(() => {
  //   let map = {
  //     namespaced: true,
  //     getters: {
  //       activeMapLayers: () => []
  //     }
  //   }
  //   store = new Vuex.Store({ modules: { map } })
  //   wrapper = mount(MapLegend, {
  //     vuetify,
  //     store,
  //     localVue
  //   })
  // })

  it('Is hidden on start', () => {
    let map = {
      namespaced: true,
      getters: {
        activeMapLayers: () => []
      }
    }
    store = new Vuex.Store({ modules: { map } })
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
          var types = {
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
          description: "A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps",
          display_data_name: "ecocat_water_related_reports",
          display_name: "EcoCat Water-related Reports",
          highlight_columns: [
            "REPORT_ID",
            "TITLE",
            "SHORT_DESCRIPTION",
            "AUTHOR",
            "DATE_PUBLISHED",
            "REPORT_AUDIENCE",
            "LONG_DESCRIPTION",
          ],
          label: "Title",
          label_column: "TITLE",
          layer_category_code: "REPORTS",
          name: "Ecological Catalogue (formerly AquaCat)",
          source_url: "https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat",
          url: "",
          use_wms: true,
          vector_name: "",
          wms_name: "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW",
          wms_style: ""
        }]
      }
    }
    store = new Vuex.Store({ modules: { map } })
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
    ).toEqual('Ecological Catalogue (formerly AquaCat)')
  })

  it('Shows the legend items for a layer that has multiple legend items', async () => {
    let propsData = {
      map: {
        getLayer: (name) => {
          var types = {
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
          description: "A compendium of reports that provide information about aquatic and terrestrial animals and plants, soils, surface water, groundwater and their accompanying data files and maps",
          display_data_name: "ecocat_water_related_reports",
          display_name: "EcoCat Water-related Reports",
          highlight_columns: [
            "REPORT_ID",
            "TITLE",
            "SHORT_DESCRIPTION",
            "AUTHOR",
            "DATE_PUBLISHED",
            "REPORT_AUDIENCE",
            "LONG_DESCRIPTION",
          ],
          label: "Title",
          label_column: "TITLE",
          layer_category_code: "REPORTS",
          name: "Ecological Catalogue (formerly AquaCat)",
          source_url: "https://catalogue.data.gov.bc.ca/dataset/ecological-catalogue-formerly-aquacat",
          url: "",
          use_wms: true,
          vector_name: "",
          wms_name: "WHSE_FISH.ACAT_REPORT_POINT_PUB_SVW",
          wms_style: ""
        },
        {
          description: "Flow network arcs (observed, inferred and constructed). Contains no banks, coast or watershed bourdary arcs. Directionalized and connected. Contains heirarchial key and route identifier.",
          display_data_name: "freshwater_atlas_stream_networks",
          display_name: "Freshwater Atlas Stream Networks",
          highlight_columns: [
            "STREAM_ORDER",
            "STREAM_MAGNITUDE",
            "FEATURE_LENGTH_M",
            "WATERSHED_GROUP_ID"
          ],
          label: "Feature ID",
          label_column: "LINEAR_FEATURE_ID",
          layer_category_code: "FRESHWATER_MARINE",
          name: "Freshwater Atlas Stream Networks",
          source_url: "https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network",
          url: "",
          use_wms: true,
          vector_name: "",
          wms_name: "WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP",
          wms_style: "1853",
        }]
      }
    }
    store = new Vuex.Store({ modules: { map } })
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

    expect(layerName).toEqual('Ecological Catalogue (formerly AquaCat)')
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
    store = new Vuex.Store({ modules: { map } })
    var legendItem = shallowMount(StreamAllocationRestrictionsLegendItem, {
      vuetify,
      store,
      propsData,
      localVue
    })

    let legendText = legendItem.vm.labelLookup('OR')
    expect(legendText).toEqual('Office Reserve')
    legendText = legendItem.vm.labelLookup('FR_EXC')
    expect(legendText).toEqual('Fully Recorded Except')
  })
})
