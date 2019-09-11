import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import StreamStation from '@/components/features/StreamStation.vue'

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
  it('generates chartOptions with x and y axis', () => {
    const wrapper = shallowMount(StreamStation, {
      vuetify,
      localVue,
      propsData: {
        record: {
          properties: { name: 'station name', url: '/test' }
        }
      }
    })
    wrapper.setData(
      {
        flowChartOptions: wrapper.vm.newChartOptions(
          'New chart',
          'days', // unit
          [1, 2, 3, 4]
        )
      }
    )
    expect(wrapper.vm.flowChartOptions.scales.yAxes.length).toEqual(1)
    expect(wrapper.vm.flowChartOptions.scales.xAxes.length).toEqual(1)
  })
})
