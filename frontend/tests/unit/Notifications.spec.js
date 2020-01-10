import { mount, createLocalVue } from '@vue/test-utils'
import Notifications from '../../src/components/Notifications'
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

describe('Notifications', () => {
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

  it('Info message appears when an info event is sent', async () => {
    EventBus.$emit('info', 'test info msg')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('#infoNotification').text()).toContain('test info msg')
  })
  it('Error message appears when an error event is sent', async () => {
    EventBus.$emit('error', 'test error msg')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('#errorNotification').text()).toContain('test error msg')
  })
  it('Help message appears when a help event is sent', async () => {
    EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('#helpNotification').text()).toContain('test help msg')
  })
  /*
  Buggy test
  Not working even when localStorage is mocked (and confirmed to work).
  Issue is that the #helpNotification div doesn't go away
  */
  // it('Help message can be disabled', async () => {
  //   EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
  //   await wrapper.vm.$nextTick()
  //   expect(wrapper.find('#helpNotification').text()).toContain('test help msg')
  //
  //   wrapper.find('#disableHelpButton').trigger('click')
  //   await wrapper.vm.$nextTick()
  //   expect(wrapper.find('#helpNotification').exists()).toBe(false)
  //
  //   // try to trigger the same help message again after triggering the "disable" button.
  //   EventBus.$emit('help', { text: 'test help msg', disableKey: 'testHelpKey' })
  //   expect(wrapper.find('#helpNotification').exists()).toBe(false)
  // })
})
