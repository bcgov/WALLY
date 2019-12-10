import { shallowMount, createLocalVue, mount } from '@vue/test-utils'
import Header from '@/components/Header.vue'
import Vue from 'vue'
import Vuetify from 'vuetify'
import Vuex from 'vuex'

Vue.use(Vuetify)
const localVue = createLocalVue()
localVue.use(Vuex)

describe('Home.vue', () => {
  it('displays title', () => {
    const getters = {
      adjustableSidePanel: () => true
    }
    const store = new Vuex.Store({ getters })
    const wrapper = shallowMount(Header, { store, localVue })
    expect(wrapper.text()).toMatch('Water Allocation')
  })
})
