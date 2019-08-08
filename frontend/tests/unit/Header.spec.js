import { shallowMount } from '@vue/test-utils'
import Header from '@/components/Header.vue'

describe('Home.vue', () => {
  it('displays title', () => {
    const wrapper = shallowMount(Header)
    expect(wrapper.text()).toMatch('Water Allocation')
  })
})
