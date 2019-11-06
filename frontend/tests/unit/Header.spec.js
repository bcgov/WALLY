import { shallowMount, createLocalVue } from '@vue/test-utils'
import Header from '@/components/Header.vue'
import Vue from 'vue'
import Vuetify from 'vuetify'

Vue.use(Vuetify)
const localVue = createLocalVue()

describe('Home.vue', () => {
  it('displays title', () => {
    const wrapper = shallowMount(Header, { localVue })
    expect(wrapper.text()).toMatch('Water Allocation')
  })
})
