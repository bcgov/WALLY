import { mount, createLocalVue } from '@vue/test-utils'
import Notifications from '../../src/components/notifications/Notifications'
import Vuex from 'vuex'
import Vuetify from 'vuetify'
import Vue from 'vue'
import EventBus from '../../src/services/EventBus'
const localVue = createLocalVue()
localVue.use(Vuex)
// localVue with Vuetify shows console warnings so we'll use Vue instead
// https://github.com/vuetifyjs/vuetify/issues/4964
// localVue.use(Vuetify)
Vue.use(Vuetify)

const vuetify = new Vuetify()

describe('Map Legend Test', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(Notifications, {
      vuetify,
      localVue
    })
  })

  it('Component begins with no messages shown', () => {
    expect(wrapper.find('#infoNotification').exists()).toBe(false)
    expect(wrapper.find('#errorNotification').exists()).toBe(false)
    expect(wrapper.find('#helpNotification').exists()).toBe(false)
  })

  it('Info message appears when an info event is sent', () => {
    EventBus.$emit('info', 'test info msg')
    expect(wrapper.find('#infoNotification').text()).toContain('test info msg')
  })
  it('Error message appears when an error event is sent', () => {
    EventBus.$emit('error', 'test error msg')
    expect(wrapper.find('#errorNotification').text()).toContain('test error msg')
  })
  it('Help message appears when a help event is sent', () => {
    EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
    expect(wrapper.find('#helpNotification').text()).toContain('test help msg')
  })
  it('Help message can be disabled', () => {
    EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
    expect(wrapper.find('#helpNotification').text()).toContain('test help msg')

    wrapper.find('#disableHelpButton').trigger('click')
    expect(wrapper.find('#helpNotification').exists()).toBe(false)

    // try to trigger the same help message again after triggering the "disable" button.
    EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
    expect(wrapper.find('#helpNotification').exists()).toBe(false)
  })
})
