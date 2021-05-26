import { createLocalVue, shallowMount } from '@vue/test-utils'
import WellsCrossSection
  from '../../../../src/components/analysis/cross_section/WellsCrossSection.vue'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import VueRouter from 'vue-router'

// import ApiService from '../../../../src/services/ApiService'

const localVue = createLocalVue()
localVue.use(Vuex)
Vue.use(Vuetify)
const router = new VueRouter()
localVue.use(VueRouter)

const vuetify = new Vuetify()

// jest.mock('ApiService')
describe('Wells Cross Section Test', () => {
  let wrapper
  let store
  let mapActions
  let mapMutations
  let getters

  beforeEach(() => {
    getters = {
      app: () => {}
    }
    let mapGetters = {
      isMapLayerActive: state => layerId => false,
      isMapReady: () => true,
      sectionLine: jest.fn(),
      draw: () => {
        return {
          getMode: () => 'draw_line_string'
        }
      },
      map: () => {
        return {
          on: jest.fn(),
          off: jest.fn(),
          getLayer: () => 'wellOffsetDistance',
          getSource: jest.fn(),
          removeLayer: jest.fn(),
          removeSource: jest.fn(),
          addLayer: jest.fn(),
          addSource: jest.fn()
        }
      }
    }
    mapActions = {
      setDrawMode: jest.fn(),
      clearSelections: () => jest.fn(),
      addSelectedFeature: jest.fn(),
      addMapLayer: jest.fn()
    }
    mapMutations = {
      setMode: jest.fn(),
      resetMode: jest.fn(),
      setMapReady: () => true,
      addShape: jest.fn(),
      removeShapes: jest.fn()
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
      mutations: {
        resetSectionLine: jest.fn()
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
    store.commit = jest.fn()
    wrapper = shallowMount(WellsCrossSection, {
      sync: false,
      vuetify,
      store,
      localVue,
      router,
      propsData: {
        record: { geometry: { 'coordinates': [[-122.74542712943077, 50.34900300025518], [-122.76198935563441, 50.343890442681754]], 'type': 'LineString' } }
      },
      mocks: {
        $refs: {
          crossPlot: {}
        }
      },
      methods: {
        fetchWells: (params) => wellResults,
        fetchWellsLithology: (ids) => lithologyResults
      }
    })
  })

  it('processes well results', () => {
    wrapper.vm.processWellResults(wellResults)
    expect(wrapper.vm.wells.length).toBe(8)
    expect(wrapper.vm.elevations.length).toBe(22)
    expect(wrapper.vm.surfacePoints.length).toBe(5)
    expect(wrapper.vm.waterbodies.length).toBe(2)
    expect(wrapper.vm.screens.length).toBe(2)
  })

  it('deletes a well from the well list', () => {
    wrapper.vm.processWellResults(wellResults)
    expect(wrapper.vm.wells.length).toBe(8)
    wrapper.vm.deleteWell({ well_tag_number: 115626 })
    expect(wrapper.vm.wells.length).toBe(7)
  })

  it('processes lithology results', () => {
    wrapper.vm.processWellResults(wellResults)
    wrapper.vm.buildLithologyList(lithologyResults.results)
    expect(wrapper.vm.wellsLithology.length).toBe(45)
    expect(wrapper.vm.wellsLithology[0].y0).toBe(421.66508610810325)
  })

  it('deletes a lithology record from the lithology list', () => {
    wrapper.vm.processWellResults(wellResults)
    wrapper.vm.buildLithologyList(lithologyResults.results)
    expect(wrapper.vm.wellsLithology.length).toBe(45)
    wrapper.vm.deleteWell({ well_tag_number: 72188 })
    expect(wrapper.vm.wellsLithology.length).toBe(42)
  })

  // it('resets all shapes when closed', () => {
  //   wrapper.destroy()
  //   expect(1).toBe(1)
  //
  //   // expect(store.commit).toHaveBeenCalledWith('map/resetMode')
  //   // expect(store.dispatch).toHaveBeenCalledWith('map/clearSelections')
  //   // expect(store.commit).toHaveBeenCalledWith('resetSectionLine')
  // })

  it('has a data table display wells', () => {
    expect(wrapper.find('#cross-section-well-table').exists()).toBe(true)
  })
})

const wellResults = {
  'search_area': {
    'type': 'Polygon',
    'coordinates': [
      [
        [
          -122.74496947009534,
          50.3471778520593
        ],
        [
          -122.74557786567657,
          50.34694970505789
        ],
        [
          -122.74577330645621,
          50.3468828900653
        ],
        [
          -122.74597637186258,
          50.346826127132594
        ],
        [
          -122.74656949523411,
          50.346677847542324
        ],
        [
          -122.74717789374448,
          50.34644969944234
        ],
        [
          -122.74737333146147,
          50.346382885489774
        ],
        [
          -122.74757639354006,
          50.34632612348083
        ],
        [
          -122.74816952037209,
          50.34617784302538
        ],
        [
          -122.74877792181144,
          50.345949693826924
        ],
        [
          -122.74905322905107,
          50.345859093530834
        ],
        [
          -122.74975320874198,
          50.345659100365765
        ],
        [
          -122.74987642388743,
          50.34562611836842
        ],
        [
          -122.75046955556422,
          50.345477836701626
        ],
        [
          -122.75107796110419,
          50.34524968596529
        ],
        [
          -122.75127339147113,
          50.34518287450857
        ],
        [
          -122.75147644556333,
          50.345126114716535
        ],
        [
          -122.75206958070055,
          50.344977832184554
        ],
        [
          -122.7526779891694,
          50.34474968034987
        ],
        [
          -122.7528734164741,
          50.344682869932996
        ],
        [
          -122.75307646723893,
          50.344626111064606
        ],
        [
          -122.75366960583634,
          50.34447782766751
        ],
        [
          -122.75427801723389,
          50.34424967473443
        ],
        [
          -122.75447344147628,
          50.34418286535742
        ],
        [
          -122.75467648891366,
          50.34412610741265
        ],
        [
          -122.75547646385283,
          50.34392611438454
        ],
        [
          -122.75599031337919,
          50.343797653329624
        ],
        [
          -122.75643506992228,
          50.34360704485994
        ],
        [
          -122.75669808403221,
          50.343507139200455
        ],
        [
          -122.75697651925695,
          50.34342610230001
        ],
        [
          -122.75756966615911,
          50.34327781682661
        ],
        [
          -122.75817808458595,
          50.3430496612573
        ],
        [
          -122.75837350147877,
          50.342982854376004
        ],
        [
          -122.75857654093033,
          50.342926098647965
        ],
        [
          -122.75916969129239,
          50.34277781230954
        ],
        [
          -122.7597781126477,
          50.34254965564185
        ],
        [
          -122.75997352647848,
          50.3424828498004
        ],
        [
          -122.76017656260295,
          50.342426094995844
        ],
        [
          -122.76097653754259,
          50.3422261019673
        ],
        [
          -122.76302353815262,
          50.34557388502181
        ],
        [
          -122.76243038500333,
          50.3457221745615
        ],
        [
          -122.76182196677689,
          50.345950332737345
        ],
        [
          -122.76162657429435,
          50.346017131131944
        ],
        [
          -122.7614235598277,
          50.34607388136973
        ],
        [
          -122.76083041013878,
          50.34622217004439
        ],
        [
          -122.76022199484143,
          50.34645032712187
        ],
        [
          -122.76002659929706,
          50.346517126556286
        ],
        [
          -122.75982358150353,
          50.34657387771763
        ],
        [
          -122.75930976573413,
          50.346702332986965
        ],
        [
          -122.75886502059525,
          50.346892939524
        ],
        [
          -122.7586020229208,
          50.34699283943444
        ],
        [
          -122.75832360317993,
          50.347073874065536
        ],
        [
          -122.75752359494003,
          50.34727387683252
        ],
        [
          -122.75693047046704,
          50.347422159203255
        ],
        [
          -122.75632206220018,
          50.347650313644635
        ],
        [
          -122.75612665930656,
          50.34771711557474
        ],
        [
          -122.75592363352744,
          50.347773868952906
        ],
        [
          -122.75533049560492,
          50.347922154686096
        ],
        [
          -122.75472209026744,
          50.3481503080291
        ],
        [
          -122.75452668431177,
          50.34821711099909
        ],
        [
          -122.75432365520548,
          50.34827386530087
        ],
        [
          -122.75373052074363,
          50.34842215016907
        ],
        [
          -122.75312211833544,
          50.3486503024136
        ],
        [
          -122.75292670931752,
          50.348717106423514
        ],
        [
          -122.75272367688385,
          50.34877386164901
        ],
        [
          -122.75198587621885,
          50.34895831273995
        ],
        [
          -122.75148842358317,
          50.34910044305352
        ],
        [
          -122.75082215763207,
          50.349350294551826
        ],
        [
          -122.75062674432685,
          50.34941710001769
        ],
        [
          -122.75042370723465,
          50.3494738565364
        ],
        [
          -122.74983058107911,
          50.3496221393281
        ],
        [
          -122.74922218570185,
          50.349850288936345
        ],
        [
          -122.74902676933428,
          50.34991709544215
        ],
        [
          -122.74882372891456,
          50.34997385288458
        ],
        [
          -122.7482306062201,
          50.35012213481107
        ],
        [
          -122.74762221377252,
          50.35035028332083
        ],
        [
          -122.74742679434246,
          50.35041709086666
        ],
        [
          -122.74722375059508,
          50.35047384923285
        ],
        [
          -122.74642372553225,
          50.35067385620597
        ],
        [
          -122.74437635018454,
          50.34732613078433
        ],
        [
          -122.74496947009534,
          50.3471778520593
        ]
      ]
    ]
  },
  'wells': [
    {
      'well_tag_number': 120542,
      'finished_well_depth': 5.486400000000001,
      'water_depth': null,
      'ground_elevation_from_dem': 424.29859878492414,
      'distance_from_origin': 578.8343446625054,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': null,
      'aquifer_lithology': null,
      'feature': {
        'type': 'Feature',
        'id': '5237bf98-1f95-4da7-8700-f43c25ea3240',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.7536,
            50.3479
          ]
        },
        'properties': {
          'well_tag_number': 120542,
          'static_water_level': null,
          'screen_set': '[]',
          'well_yield': null,
          'diameter': '',
          'latitude': 50.3479,
          'longitude': -122.7536,
          'well_yield_unit': null,
          'finished_well_depth': '18.00',
          'street_address': '1773 REID ROAD',
          'intended_water_use': 'Private Domestic',
          'aquifer_lithology': null,
          'aquifer': null,
          'distance_from_line': 142.5032937055826,
          'compass_direction': 'NW'
        }
      },
      'screen_set': []
    },
    {
      'well_tag_number': 115626,
      'finished_well_depth': 41.148,
      'water_depth': null,
      'ground_elevation_from_dem': 409.4307191556015,
      'distance_from_origin': 220.29473326907,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': null,
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': '87be8a4b-989a-4ac9-8b90-cd648fc4e505',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.74745,
            50.34715
          ]
        },
        'properties': {
          'well_tag_number': 115626,
          'static_water_level': null,
          'screen_set': '[{"start": "135.00", "end": "195.00", "diameter": "6.00", "assembly_type": null, "slot_size": null}]',
          'well_yield': '35.000',
          'diameter': ' ',
          'latitude': 50.34715,
          'longitude': -122.74745,
          'well_yield_unit': 'USGPM',
          'finished_well_depth': '135.00',
          'street_address': 'LOT 5  REID ROAD',
          'intended_water_use': 'Private Domestic',
          'aquifer_lithology': 'Unknown',
          'aquifer': null,
          'distance_from_line': 122.98469852995582,
          'compass_direction': 'SE'
        }
      },
      'screen_set': [
        {
          'start': '135.00',
          'end': '195.00',
          'diameter': '6.00',
          'assembly_type': null,
          'slot_size': null
        }
      ]
    },
    {
      'well_tag_number': 99374,
      'finished_well_depth': 42.062400000000004,
      'water_depth': 18.25752,
      'ground_elevation_from_dem': 460.6982163053367,
      'distance_from_origin': 973.3517002671781,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': {
        'aquifer_id': 1016,
        'subtype': '5a',
        'subtype_desc': 'Fractured sedimentary rock',
        'material': 'B',
        'material_desc': 'Bedrock'
      },
      'aquifer_lithology': 'Bedrock',
      'feature': {
        'type': 'Feature',
        'id': '58e0807c-850f-4336-a014-57e74ef6b901',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.757676,
            50.345139
          ]
        },
        'properties': {
          'well_tag_number': 99374,
          'static_water_level': '59.90',
          'screen_set': '[]',
          'well_yield': '7.000',
          'diameter': '',
          'latitude': 50.345139,
          'longitude': -122.757676,
          'well_yield_unit': 'USGPM',
          'finished_well_depth': '138.00',
          'street_address': '',
          'intended_water_use': 'Private Domestic',
          'aquifer_lithology': 'Bedrock',
          'aquifer_hydraulically_connected': false,
          'aquifer': 1016,
          'distance_from_line': 9.230524429237056,
          'compass_direction': 'SE'
        }
      },
      'screen_set': []
    },
    {
      'well_tag_number': 99385,
      'finished_well_depth': 42.367200000000004,
      'water_depth': 20.4216,
      'ground_elevation_from_dem': 445.37498109257604,
      'distance_from_origin': 879.9284487892686,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': {
        'aquifer_id': 1016,
        'subtype': '5a',
        'subtype_desc': 'Fractured sedimentary rock',
        'material': 'B',
        'material_desc': 'Bedrock'
      },
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': '42f59aab-a93e-4ca0-a8ac-644fad219345',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.756508,
            50.345523
          ]
        },
        'properties': {
          'well_tag_number': 99385,
          'static_water_level': '67.00',
          'screen_set': '[{"start": "119.00", "end": "138.00", "diameter": "4.00", "assembly_type": "RISER_PIPE", "slot_size": "20.00"}]',
          'well_yield': '13.000',
          'diameter': '',
          'latitude': 50.345523,
          'longitude': -122.756508,
          'well_yield_unit': 'USGPM',
          'finished_well_depth': '139.00',
          'street_address': '',
          'intended_water_use': 'Private Domestic',
          'aquifer_lithology': 'Unknown',
          'aquifer_hydraulically_connected': false,
          'aquifer': 1016,
          'distance_from_line': 7.772959269308376,
          'compass_direction': 'SE'
        }
      },
      'screen_set': [
        {
          'start': '119.00',
          'end': '138.00',
          'diameter': '4.00',
          'assembly_type': 'RISER_PIPE',
          'slot_size': '20.00'
        }
      ]
    },
    {
      'well_tag_number': 99351,
      'finished_well_depth': null,
      'water_depth': null,
      'ground_elevation_from_dem': 433.4928000931367,
      'distance_from_origin': 775.8113082133183,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': {
        'aquifer_id': 1016,
        'subtype': '5a',
        'subtype_desc': 'Fractured sedimentary rock',
        'material': 'B',
        'material_desc': 'Bedrock'
      },
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': '55feb7d7-ebc5-4057-9480-928da9b10961',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.755938,
            50.346925
          ]
        },
        'properties': {
          'well_tag_number': 99351,
          'static_water_level': null,
          'screen_set': '[]',
          'well_yield': null,
          'diameter': '',
          'latitude': 50.346925,
          'longitude': -122.755938,
          'well_yield_unit': null,
          'finished_well_depth': null,
          'street_address': 'RIAD ROAD',
          'intended_water_use': 'Private Domestic',
          'aquifer_lithology': 'Unknown',
          'aquifer_hydraulically_connected': false,
          'aquifer': 1016,
          'distance_from_line': 116.55393934176006,
          'compass_direction': 'NW'
        }
      },
      'screen_set': []
    },
    {
      'well_tag_number': 72188,
      'finished_well_depth': 16.764,
      'water_depth': 10.0584,
      'ground_elevation_from_dem': 421.66508610810325,
      'distance_from_origin': 518.9169122356801,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': null,
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': '937531c6-0693-4e0a-8c78-62d4709afacb',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.751165,
            50.345898
          ]
        },
        'properties': {
          'well_tag_number': 72188,
          'static_water_level': '33.00',
          'screen_set': '[]',
          'well_yield': '1.000',
          'diameter': '6.0',
          'latitude': 50.345898,
          'longitude': -122.751165,
          'well_yield_unit': 'GPM',
          'finished_well_depth': '55.00',
          'street_address': 'REID ROAD',
          'intended_water_use': 'Not Applicable',
          'aquifer_lithology': 'Unknown',
          'aquifer': null,
          'distance_from_line': 134.63601570656556,
          'compass_direction': 'SE'
        }
      },
      'screen_set': []
    },
    {
      'well_tag_number': 72189,
      'finished_well_depth': 36.576,
      'water_depth': 14.9352,
      'ground_elevation_from_dem': 432.6348549724075,
      'distance_from_origin': 761.6575652594896,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': {
        'aquifer_id': 1016,
        'subtype': '5a',
        'subtype_desc': 'Fractured sedimentary rock',
        'material': 'B',
        'material_desc': 'Bedrock'
      },
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': 'ae374fa2-0fa9-48dc-a291-9dd644324360',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.754918,
            50.345861
          ]
        },
        'properties': {
          'well_tag_number': 72189,
          'static_water_level': '49.00',
          'screen_set': '[]',
          'well_yield': '4.000',
          'diameter': '6.0',
          'latitude': 50.345861,
          'longitude': -122.754918,
          'well_yield_unit': 'GPM',
          'finished_well_depth': '120.00',
          'street_address': '1750 REID RD',
          'intended_water_use': 'Not Applicable',
          'aquifer_lithology': 'Unknown',
          'aquifer_hydraulically_connected': false,
          'aquifer': 1016,
          'distance_from_line': 22.29346482886155,
          'compass_direction': 'SE'
        }
      },
      'screen_set': []
    },
    {
      'well_tag_number': 72190,
      'finished_well_depth': 54.864000000000004,
      'water_depth': null,
      'ground_elevation_from_dem': 421.4625140129489,
      'distance_from_origin': 512.2332512573602,
      'distance_from_line': null,
      'compass_direction': null,
      'aquifer': {
        'aquifer_id': 1016,
        'subtype': '5a',
        'subtype_desc': 'Fractured sedimentary rock',
        'material': 'B',
        'material_desc': 'Bedrock'
      },
      'aquifer_lithology': 'Unknown',
      'feature': {
        'type': 'Feature',
        'id': '07c48077-2a89-4253-b058-0cbd5c739999',
        'geometry': {
          'type': 'Point',
          'coordinates': [
            -122.751164,
            50.346033
          ]
        },
        'properties': {
          'well_tag_number': 72190,
          'static_water_level': null,
          'screen_set': '[]',
          'well_yield': '2.000',
          'diameter': '6.0',
          'latitude': 50.346033,
          'longitude': -122.751164,
          'well_yield_unit': 'GPM',
          'finished_well_depth': '180.00',
          'street_address': 'REID RD',
          'intended_water_use': 'Not Applicable',
          'aquifer_lithology': 'Unknown',
          'aquifer_hydraulically_connected': false,
          'aquifer': 1016,
          'distance_from_line': 121.71350919828984,
          'compass_direction': 'SE'
        }
      },
      'screen_set': []
    }
  ],
  'elevation_profile': [
    {
      'distance_from_origin': 0,
      'elevation': 407
    },
    {
      'distance_from_origin': 61.1144808803289,
      'elevation': 400
    },
    {
      'distance_from_origin': 126.706315146224,
      'elevation': 405
    },
    {
      'distance_from_origin': 187.683110666355,
      'elevation': 407
    },
    {
      'distance_from_origin': 253.413744621469,
      'elevation': 412
    },
    {
      'distance_from_origin': 314.36421833727,
      'elevation': 413
    },
    {
      'distance_from_origin': 380.122288400816,
      'elevation': 406
    },
    {
      'distance_from_origin': 434.645376966701,
      'elevation': 412
    },
    {
      'distance_from_origin': 495.600456315322,
      'elevation': 421
    },
    {
      'distance_from_origin': 561.354593784878,
      'elevation': 423
    },
    {
      'distance_from_origin': 622.301393969983,
      'elevation': 428
    },
    {
      'distance_from_origin': 688.06526091059,
      'elevation': 429
    },
    {
      'distance_from_origin': 749.006729429285,
      'elevation': 432
    },
    {
      'distance_from_origin': 814.777221536853,
      'elevation': 436
    },
    {
      'distance_from_origin': 875.715037418621,
      'elevation': 445
    },
    {
      'distance_from_origin': 936.676535581829,
      'elevation': 459
    },
    {
      'distance_from_origin': 996.016722839871,
      'elevation': 462
    },
    {
      'distance_from_origin': 1056.95959576722,
      'elevation': 467
    },
    {
      'distance_from_origin': 1122.73098376051,
      'elevation': 468
    },
    {
      'distance_from_origin': 1183.67129119716,
      'elevation': 488
    },
    {
      'distance_from_origin': 1249.4465203552,
      'elevation': 492
    },
    {
      'distance_from_origin': 1310.38485026292,
      'elevation': 498
    }
  ],
  'surface': [
    [],
    [
      [
        -122.746,
        50.3498,
        431
      ],
      [
        -122.7468,
        50.3496,
        430
      ],
      [
        -122.7476,
        50.3493,
        430
      ],
      [
        -122.7484,
        50.3491,
        428
      ],
      [
        -122.7492,
        50.3488,
        435
      ],
      [
        -122.75,
        50.3486,
        442
      ],
      [
        -122.7508,
        50.3484,
        443
      ],
      [
        -122.7516,
        50.3481,
        435
      ],
      [
        -122.7523,
        50.3479,
        439
      ],
      [
        -122.7531,
        50.3476,
        447
      ],
      [
        -122.7539,
        50.3474,
        441
      ],
      [
        -122.7547,
        50.3471,
        447
      ],
      [
        -122.7555,
        50.3469,
        451
      ],
      [
        -122.7563,
        50.3466,
        459
      ],
      [
        -122.7571,
        50.3464,
        468
      ],
      [
        -122.7579,
        50.3462,
        479
      ],
      [
        -122.7587,
        50.3459,
        488
      ],
      [
        -122.7594,
        50.3457,
        497
      ],
      [
        -122.7602,
        50.3454,
        503
      ],
      [
        -122.761,
        50.3452,
        505
      ],
      [
        -122.7618,
        50.3449,
        522
      ],
      [
        -122.7626,
        50.3447,
        524
      ]
    ],
    [
      [
        -122.7454,
        50.349,
        407
      ],
      [
        -122.7462,
        50.3488,
        400
      ],
      [
        -122.747,
        50.3485,
        405
      ],
      [
        -122.7478,
        50.3483,
        407
      ],
      [
        -122.7486,
        50.348,
        412
      ],
      [
        -122.7494,
        50.3478,
        413
      ],
      [
        -122.7502,
        50.3475,
        406
      ],
      [
        -122.7509,
        50.3473,
        412
      ],
      [
        -122.7517,
        50.3471,
        421
      ],
      [
        -122.7525,
        50.3468,
        423
      ],
      [
        -122.7533,
        50.3466,
        428
      ],
      [
        -122.7541,
        50.3463,
        429
      ],
      [
        -122.7549,
        50.3461,
        432
      ],
      [
        -122.7557,
        50.3458,
        436
      ],
      [
        -122.7565,
        50.3456,
        445
      ],
      [
        -122.7573,
        50.3454,
        459
      ],
      [
        -122.758,
        50.3451,
        462
      ],
      [
        -122.7588,
        50.3449,
        467
      ],
      [
        -122.7596,
        50.3446,
        468
      ],
      [
        -122.7604,
        50.3444,
        488
      ],
      [
        -122.7612,
        50.3441,
        492
      ],
      [
        -122.762,
        50.3439,
        498
      ]
    ],
    [
      [
        -122.7448,
        50.3482,
        380
      ],
      [
        -122.7456,
        50.348,
        381
      ],
      [
        -122.7464,
        50.3477,
        383
      ],
      [
        -122.7472,
        50.3475,
        387
      ],
      [
        -122.748,
        50.3472,
        393
      ],
      [
        -122.7488,
        50.347,
        389
      ],
      [
        -122.7495,
        50.3467,
        390
      ],
      [
        -122.7503,
        50.3465,
        404
      ],
      [
        -122.7511,
        50.3462,
        406
      ],
      [
        -122.7519,
        50.346,
        408
      ],
      [
        -122.7527,
        50.3458,
        410
      ],
      [
        -122.7535,
        50.3455,
        411
      ],
      [
        -122.7543,
        50.3453,
        417
      ],
      [
        -122.7551,
        50.345,
        420
      ],
      [
        -122.7559,
        50.3448,
        426
      ],
      [
        -122.7566,
        50.3445,
        443
      ],
      [
        -122.7574,
        50.3443,
        443
      ],
      [
        -122.7582,
        50.3441,
        449
      ],
      [
        -122.759,
        50.3438,
        457
      ],
      [
        -122.7598,
        50.3436,
        467
      ],
      [
        -122.7606,
        50.3433,
        467
      ],
      [
        -122.7614,
        50.3431,
        478
      ]
    ],
    [
      [
        -122.7442,
        50.3474,
        366
      ],
      [
        -122.745,
        50.3471,
        369
      ],
      [
        -122.7458,
        50.3469,
        372
      ],
      [
        -122.7466,
        50.3467,
        376
      ],
      [
        -122.7474,
        50.3464,
        377
      ],
      [
        -122.7481,
        50.3462,
        378
      ],
      [
        -122.7489,
        50.3459,
        383
      ],
      [
        -122.7497,
        50.3457,
        389
      ],
      [
        -122.7505,
        50.3454,
        394
      ],
      [
        -122.7513,
        50.3452,
        392
      ],
      [
        -122.7521,
        50.3449,
        393
      ],
      [
        -122.7529,
        50.3447,
        398
      ],
      [
        -122.7537,
        50.3445,
        406
      ],
      [
        -122.7545,
        50.3442,
        413
      ],
      [
        -122.7552,
        50.344,
        422
      ],
      [
        -122.756,
        50.3437,
        426
      ],
      [
        -122.7568,
        50.3435,
        438
      ],
      [
        -122.7576,
        50.3432,
        448
      ],
      [
        -122.7584,
        50.343,
        453
      ],
      [
        -122.7592,
        50.3428,
        450
      ],
      [
        -122.76,
        50.3425,
        454
      ],
      [
        -122.7608,
        50.3423,
        460
      ]
    ]
  ],
  'waterbodies': [
    {
      'name': 'Unnamed Stream',
      'distance': 1134.3878592235742,
      'elevation': 464.8719177301493,
      'geometry': {
        '_is_empty': false,
        '__geom__': 140091632857968,
        '_ndim': 3
      }
    },
    {
      'name': 'Unnamed Stream',
      'distance': 401.28622364062363,
      'elevation': 401.2163622300472,
      'geometry': {
        '_is_empty': false,
        '__geom__': 140091632758192,
        '_ndim': 3
      }
    }
  ]
}

const lithologyResults = {
  'count': 8,
  'next': null,
  'previous': null,
  'results': [
    {
      'well_tag_number': 72188,
      'latitude': 50.345898,
      'longitude': -122.751165,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '20.00',
          'lithology_raw_data': 'EXISTING DUG WELL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '20.00',
          'end': '50.00',
          'lithology_raw_data': 'COURSE TILL GRAVEL & BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '50.00',
          'end': '55.00',
          'lithology_raw_data': 'WATER BEARING COURSE TILL & BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 72189,
      'latitude': 50.345861,
      'longitude': -122.754918,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '1.00',
          'lithology_raw_data': 'HARD PACKED GRAVEL DRIVE WAY',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '1.00',
          'end': '23.00',
          'lithology_raw_data': 'COURSE GRAVEL & BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '23.00',
          'end': '54.00',
          'lithology_raw_data': 'VERY HARD STONEY GRAY CLAY',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '54.00',
          'end': '77.00',
          'lithology_raw_data': 'TILLY GRAY CLAY & STONES SMALL SEAMS OF',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '0.00',
          'end': '0.00',
          'lithology_raw_data': 'WATER',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '77.00',
          'end': '80.00',
          'lithology_raw_data': 'BROKEN ROCK GREEN GRANITE',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '80.00',
          'end': '120.00',
          'lithology_raw_data': 'HARD GREEN GRANITE SOME QUARTZ',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 72190,
      'latitude': 50.346033,
      'longitude': -122.751164,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '7.00',
          'lithology_raw_data': 'SANDY GRAVEL & BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '7.00',
          'end': '52.00',
          'lithology_raw_data': 'COURSE TILL GRAVEL BOUDLERS & CLAY',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '0.00',
          'end': '0.00',
          'lithology_raw_data': 'OLD SLIDE',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '52.00',
          'end': '95.00',
          'lithology_raw_data': 'COURSE TILL GRAY CLAY BROKEN ROCK BOULDE',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '95.00',
          'end': '100.00',
          'lithology_raw_data': 'FRACTURED ROCK',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '100.00',
          'end': '112.00',
          'lithology_raw_data': 'HARD GREEN SHALE SOME CRACKS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '112.00',
          'end': '118.00',
          'lithology_raw_data': 'SOFT GREEN GRANITE & QUARTZ',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '118.00',
          'end': '120.00',
          'lithology_raw_data': 'PURPLE SANDSTONE',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '120.00',
          'end': '180.00',
          'lithology_raw_data': 'GRAY SHALE WITH QUARTZ LAYERS OF SANDSTO',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '0.00',
          'end': '0.00',
          'lithology_raw_data': 'SOME FRACTURES',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '0.00',
          'end': '0.00',
          'lithology_raw_data': '1/2 GPM AT 100-120FT',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '0.00',
          'end': '0.00',
          'lithology_raw_data': '1 1/2 GPM AT 120-140FT',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 99351,
      'latitude': 50.346925,
      'longitude': -122.755938,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '27.00',
          'lithology_raw_data': 'SAND & GRAVEL WITH COBBLES',
          'lithology_colour': 'brown',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '207.00',
          'end': '360.00',
          'lithology_raw_data': null,
          'lithology_colour': 'brown',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '27.00',
          'end': '43.00',
          'lithology_raw_data': null,
          'lithology_hardness': 'Soft',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '360.00',
          'end': '520.00',
          'lithology_raw_data': 'ROCK GRANITE',
          'lithology_colour': 'green',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '43.00',
          'end': '207.00',
          'lithology_raw_data': null,
          'lithology_colour': 'green',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 99374,
      'latitude': 50.345139,
      'longitude': -122.757676,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '36.00',
          'lithology_raw_data': 'BROWN SILTY SAND & LARGE BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '36.00',
          'end': '73.00',
          'lithology_raw_data': null,
          'lithology_colour': 'grey',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '73.00',
          'end': '77.00',
          'lithology_raw_data': 'BROKEN ROCK',
          'lithology_colour': 'green',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '77.00',
          'end': '138.00',
          'lithology_raw_data': 'STONE',
          'lithology_colour': 'green',
          'lithology_observation': "FRACTURED 130-134' 7 GPM",
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 99385,
      'latitude': 50.345523,
      'longitude': -122.756508,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '39.00',
          'lithology_raw_data': 'BROWN SAND SILTY WITH BOULDERS',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '133.00',
          'end': '137.00',
          'lithology_raw_data': null,
          'lithology_observation': 'FRACTURED, WB',
          'water_bearing_estimated_flow': null
        },
        {
          'start': '137.00',
          'end': '139.00',
          'lithology_raw_data': null,
          'lithology_colour': 'green',
          'lithology_observation': 'HOLE CAVING',
          'water_bearing_estimated_flow': null
        },
        {
          'start': '39.00',
          'end': '77.00',
          'lithology_raw_data': null,
          'lithology_colour': 'grey',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '77.00',
          'end': '90.00',
          'lithology_raw_data': 'BROKEN ROCK & BROWN SILT',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '90.00',
          'end': '133.00',
          'lithology_raw_data': 'STONE',
          'lithology_colour': 'green',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 115626,
      'latitude': 50.34715,
      'longitude': -122.74745,
      'lithologydescription_set': [
        {
          'start': '0.00',
          'end': '28.00',
          'lithology_raw_data': 'BOULDERS, COBBLES AND LARGE GRAVEL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '28.00',
          'end': '75.00',
          'lithology_raw_data': 'FINE SILTY SAND AND GRAVEL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '75.00',
          'end': '77.00',
          'lithology_raw_data': 'FINE SILTY SAND AND GRAVEL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '77.00',
          'end': '93.00',
          'lithology_raw_data': 'CEMENTED SAND AND GRAVEL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '93.00',
          'end': '96.00',
          'lithology_raw_data': 'W/B FINE SILTY SAND',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '96.00',
          'end': '126.00',
          'lithology_raw_data': 'CEMENTED SAND AND GRAVEL',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '126.00',
          'end': '135.00',
          'lithology_raw_data': 'CASED SOFT BEDROCK',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        },
        {
          'start': '135.00',
          'end': '195.00',
          'lithology_raw_data': '6" OPEN BEDROCK HOLE',
          'lithology_observation': null,
          'water_bearing_estimated_flow': null
        }
      ]
    },
    {
      'well_tag_number': 120542,
      'latitude': 50.3479,
      'longitude': -122.7536,
      'lithologydescription_set': []
    }
  ]
}
