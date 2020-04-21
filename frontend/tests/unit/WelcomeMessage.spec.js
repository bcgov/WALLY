import { shallowMount, createLocalVue } from '@vue/test-utils'
import Vue from 'vue'
import Vuetify from 'vuetify'
import Vuex from 'vuex'
import WelcomeMessage from '../../src/components/WelcomeMessage'

Vue.use(Vuetify)
const localVue = createLocalVue()
localVue.use(Vuex)

describe('Welcome Message', () => {
  let wrapper

  beforeEach(() => {
    const getters = {
      adjustableSidePanel: () => true
    }
    const store = new Vuex.Store({ getters })
    wrapper = shallowMount(WelcomeMessage, { store, localVue })
  })

  it('Displays Welcome Message', () => {
    expect(wrapper.text()).toMatch('Welcome to WALLY')
  })

  it('Hides welcome message', () => {
    expect(wrapper.vm.show.welcome_message).toBeTruthy()
    wrapper.vm.exit()
    expect(wrapper.vm.show.welcome_message).toBeFalsy()
  })

  it('Hides welcome message on "Dont show again"', () => {
    expect(wrapper.vm.show.welcome_message).toBeTruthy()
    wrapper.vm.hideByDefault()
    expect(wrapper.vm.show.welcome_message).toBeFalsy()
  })
})
