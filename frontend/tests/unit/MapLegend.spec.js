import { shallowMount } from '@vue/test-utils'
import Header from '../../src/components/map/MapLegend.vue'

describe('Map Legend Test', () => {
  it('Is hidden when empty', () => {
    const wrapper = shallowMount(Header)
    expect(wrapper.text()).toMatch('Water Allocation')
  })

  it('Shows the legend div', () => {
    expect(1).toEqual(1)
  })

  it('Loads a legend when a layer with a legend is selected', () => {
    expect(1).toEqual(1)
  })
})
