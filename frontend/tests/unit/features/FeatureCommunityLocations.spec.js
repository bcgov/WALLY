import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vuetify from 'vuetify'
import Vue from 'vue'
import FeatureCommunityLocation from '@/components/features/FeatureCommunityLocation.vue'

const localVue = createLocalVue()
Vue.use(Vuetify)
const vuetify = new Vuetify()

describe('FeatureCommunityLocation.vue', () => {
  it('displays title', () => {
    const wrapper = shallowMount(FeatureCommunityLocation, {
      vuetify,
      localVue,
      propsData: {
        record: {
          properties: { FIRST_NATION_BC_NAME: 'Skatin Nations (Skookumchuck)' }
        }
      }
    })
    expect(wrapper.find('#communityName').text()).toMatch('Skatin Nations (Skookumchuck)')
  })
})
