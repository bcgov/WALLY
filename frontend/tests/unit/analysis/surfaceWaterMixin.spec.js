import { mount } from '@vue/test-utils'

import surfaceWaterMixin from '../../../src/components/analysis/surface_water/mixins'

describe('Surface Water mixin', () => {
  test('Returns an array of monthly qty values', () => {
    const Component = {
      render () {},
      mixins: [surfaceWaterMixin]
    }
    let wrapper = mount(Component)

    let allocValues = [1, 1, 1, 1,
      1, 1, 1, 1,
      1, 1, 1, 1]

    let monthlyQuantities = wrapper.vm.computeMonthlyQuantities('1200', allocValues)
    expect(monthlyQuantities).toEqual([100, 100, 100, 100,
      100, 100, 100, 100,
      100, 100, 100, 100 ])

    allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    monthlyQuantities = wrapper.vm.computeMonthlyQuantities('1200', allocValues)
    expect(monthlyQuantities).toEqual([300, 300, 0, 0,
      0, 0, 0, 0,
      0, 0, 300, 300 ])
  })
})
