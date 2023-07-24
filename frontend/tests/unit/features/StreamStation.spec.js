import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import StreamStation from '@/components/features/FeatureStreamStation.vue'

const localVue = createLocalVue()
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('StreamStation.vue', () => {
  it('displays title', () => {
    const wrapper = shallowMount(StreamStation, {
      vuetify,
      localVue,
      propsData: {
        record: {
          properties: { name: 'station name', url: '/test' }
        }
      }
    })
    expect(wrapper.find('#stationTitle').text()).toMatch('station name')
  })
})
