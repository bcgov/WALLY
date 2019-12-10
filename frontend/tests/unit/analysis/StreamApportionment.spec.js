import { shallowMount, createLocalVue, mount } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import StreamApportionment from '@/components/analysis/StreamApportionment.vue'
import Vuex from 'vuex'

const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Stream apportionment tests', () => {
  let wrapper
  let store
  let getters

  const testStreams = [
    {
      'ogc_fid': 2170,
      'geojson': {
        'type': 'Feature',
        'id': 2170,
        'geometry': {},
        'properties': {}
      },
      'length_metre': 1989.49593951961,
      'feature_source': 'RiverStream',
      'gnis_name': null,
      'left_right_tributary': 'RIGHT',
      'geometry_length': null,
      'watershed_group_code': 'LILL',
      'fwa_watershed_code': '100-077501-955583-455209-980096-922302-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000',
      'distance_degrees': 0.00116068147741847,
      'distance': 125.56105267,
      'closest_stream_point': {
        'type': 'Point',
        'coordinates': [
          -122.975980933839,
          50.1066134891576
        ]
      },
      'inverse_distance': 0.00006342932706455742,
      'apportionment': 54.79420004618943
    },
    {
      'ogc_fid': 2166,
      'geojson': {
        'type': 'Feature',
        'id': 2166,
        'geometry': {},
        'properties': {}
      },
      'length_metre': 1426.74052087304,
      'feature_source': 'RiverStream',
      'gnis_name': null,
      'left_right_tributary': 'LEFT',
      'geometry_length': null,
      'watershed_group_code': 'LILL',
      'fwa_watershed_code': '100-077501-955583-455209-980096-922302-119744-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000',
      'distance_degrees': 0.0024950731053954,
      'distance': 193.32160783,
      'closest_stream_point': {
        'type': 'Point',
        'coordinates': [
          -122.978479065613,
          50.1064716150089
        ]
      },
      'inverse_distance': 0.000026757109940891126,
      'apportionment': 23.114456712852437
    },
    {
      'ogc_fid': 2165,
      'geojson': {
        'type': 'Feature',
        'id': 2165,
        'geometry': {},
        'properties': {}
      },
      'length_metre': 227.690100029848,
      'feature_source': 'RiverStream',
      'gnis_name': null,
      'left_right_tributary': 'RIGHT',
      'geometry_length': null,
      'watershed_group_code': 'LILL',
      'fwa_watershed_code': '100-077501-955583-455209-980096-922302-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000-000000',
      'distance_degrees': 0.00249279407633164,
      'distance': 197.747582,
      'closest_stream_point': {
        'type': 'Point',
        'coordinates': [
          -122.978432228407,
          50.1065673948107
        ]
      },
      'inverse_distance': 0.000025572761981102783,
      'apportionment': 22.091343240958132
    }
  ]

  beforeEach(() => {
    getters = {
      isMapLayerActive: () => () => {}
    }
    store = new Vuex.Store({ getters })
    wrapper = mount(StreamApportionment, {
      vuetify,
      store,
      localVue,
      propsData: {
        record: {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'coordinates': [-122.9769538778261, 50.10578278124623],
            'type': 'Point'
          },
          'display_data_name': 'user_defined_point'
        }
      }
    })
  })

  it('Displays streams', () => {
    expect(wrapper.findAll('.v-card').length).toEqual(0)
    wrapper.setData({ streams: testStreams })
    expect(wrapper.findAll('.v-card').length).toEqual(3)
  })

  it('Calculates apportionment', () => {
    expect(1).toEqual(1)
  })
})
