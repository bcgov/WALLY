import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import Vuex from 'vuex'

import FirstNationsAreasNearby from '@/components/analysis/FirstNationsAreasNearby.vue'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const vuetify = new Vuetify()

const testResults = JSON.parse(JSON.stringify({ 'nearest_communities': [{ 'distance': 21787.23837417, 'FIRST_NATION_BC_NAME': 'Quatsino First Nation', 'URL_TO_BC_WEBSITE': 'http://www2.gov.bc.ca/gov/content/environment/natural-resource-stewardship/consulting-with-first-nations/first-nations-negotiations/first-nations-a-z-listing/quatsino-first-nation' }, { 'distance': 34291.94595866, 'FIRST_NATION_BC_NAME': "Gwa'sala-'Nakwaxda'xw Nation", 'URL_TO_BC_WEBSITE': 'http://www2.gov.bc.ca/gov/content/environment/natural-resource-stewardship/consulting-with-first-nations/first-nations-negotiations/first-nations-a-z-listing/gwa-sala-nakwaxda-xw-nation' }, { 'distance': 36331.90803954, 'FIRST_NATION_BC_NAME': 'Kwakiutl Indian Band', 'URL_TO_BC_WEBSITE': 'http://www2.gov.bc.ca/gov/content/environment/natural-resource-stewardship/consulting-with-first-nations/first-nations-negotiations/first-nations-a-z-listing/kwakiutl-indian-band' }, { 'distance': 45343.49597034, 'FIRST_NATION_BC_NAME': 'Tlatlasikwala First Nation', 'URL_TO_BC_WEBSITE': 'http://www2.gov.bc.ca/gov/content/environment/natural-resource-stewardship/consulting-with-first-nations/first-nations-negotiations/first-nations-a-z-listing/tlatlasikwala-first-nation' }], 'nearest_treaty_lands': [{ 'distance': 43887.20951978, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Provincial Crown Land - Including Subsurface' }, { 'distance': 44360.30361287, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Provincial Crown Land - Including Subsurface' }, { 'distance': 44817.53400659, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }, { 'distance': 45657.17793612, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Provincial Crown Land - Including Subsurface' }, { 'distance': 46276.7119832, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }, { 'distance': 46520.03174566, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }, { 'distance': 47170.29821232, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Provincial Crown Land - Including Subsurface' }, { 'distance': 47383.68861343, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }, { 'distance': 48006.79169162, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Provincial Crown Land - Including Subsurface' }, { 'distance': 48555.12590491, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }, { 'distance': 49688.26124106, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': "Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'EFFECTIVE_DATE': '20110401', 'LAND_TYPE': 'Former Indian Reserve' }], 'nearest_treaty_areas': [{ 'distance': 30779.88944883, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Domestic Fishing Area', 'LAND_TYPE': 'blank' }, { 'distance': 30780.41936642, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': "Area of Ka:'yu:'k't'h'/Che:k'tles7et'h' First Nations", 'LAND_TYPE': 'blank' }, { 'distance': 30780.41936642, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Migratory Birds Harvest Area', 'LAND_TYPE': 'blank' }, { 'distance': 30780.41936642, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Wildlife Harvest Area', 'LAND_TYPE': 'blank' }, { 'distance': 30780.41936642, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Roosevelt Elk Harvest Area', 'LAND_TYPE': 'blank' }, { 'distance': 42043.93886157, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Roosevelt Elk Harvest Area', 'LAND_TYPE': 'blank' }, { 'distance': 46334.10838305, 'TREATY': 'Maa-nulth', 'FIRST_NATION_NAME': 'Maa-nulth First Nations', 'EFFECTIVE_DATE': '20110401', 'AREA_TYPE': 'Potential Addition to KCFN Lands', 'LAND_TYPE': 'blank' }] }))

describe('FirstNationsAreasNearby.vue', () => {
  let mutations, getters, store
  beforeEach(() => {
    mutations = {
      setActiveMapLayers: jest.fn(),
      removeMapLayer: jest.fn()
    }
    getters = {
      isMapLayerActive: state => layerId => false,
      activeMapLayers: () => ([]),
      dataMartFeatureInfo: () => {
      },
      dataMartFeatures: () => [],
      allMapLayers: () => [],
      getCategories: () => [],
      featureSelectionExists: () => null
    }
    store = new Vuex.Store({ getters, mutations })
  })

  it('displays nearest communities', async () => {
    const wrapper = shallowMount(FirstNationsAreasNearby, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: { geometry: { 'coordinates': [-127.57192816676897, 50.53235018962306], 'type': 'Point' } }
      },
      methods: {
        fetchNearbyFirstNationsAreas: jest.fn()
      }
    })

    wrapper.setData({
      communities: testResults.nearest_communities
    })
    await wrapper.vm.$nextTick()

    // test data set has 4 communities
    expect(wrapper.find('#nearestCommunities').findAll('dt').length).toBe(4)
  })
  it('displays nearest Treaty Areas', async () => {
    const wrapper = shallowMount(FirstNationsAreasNearby, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: { geometry: { 'coordinates': [-127.57192816676897, 50.53235018962306], 'type': 'Point' } }
      },
      methods: {
        fetchNearbyFirstNationsAreas: jest.fn()
      }
    })

    wrapper.setData({
      areas: testResults.nearest_treaty_areas
    })

    await wrapper.vm.$nextTick()

    // test data set has 7 Treaty Areas
    expect(wrapper.find('#nearestTreatyAreas').findAll('dt').length).toBe(7)
  })
  it('displays nearest Treaty Lands', async () => {
    const wrapper = shallowMount(FirstNationsAreasNearby, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: { geometry: { 'coordinates': [-127.57192816676897, 50.53235018962306], 'type': 'Point' } }
      },
      methods: {
        fetchNearbyFirstNationsAreas: jest.fn()
      }
    })

    wrapper.setData({
      lands: testResults.nearest_treaty_lands
    })

    await wrapper.vm.$nextTick()

    // test data set has 11 Treaty Lands
    expect(wrapper.find('#nearestTreatyLands').findAll('dt').length).toBe(11)
  })
})
