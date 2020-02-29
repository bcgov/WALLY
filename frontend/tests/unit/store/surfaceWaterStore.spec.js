import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as surfaceWaterStore from '../../../src/store/surfaceWaterStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Store', () => {
  let store
  beforeEach(() => {
    store = surfaceWaterStore.default
  })

  it('Sets allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]

    store.mutations.setAllocationValues(store.state, 'test', allocValues)
    expect(store.state.allocationValues).toEqual({ 'test': allocValues })
  })

  it('Clears a set of allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, 'test', allocValues)
    expect(store.state.allocationValues).toEqual({ 'test': allocValues })

    store.mutations.clearAllocationValues(store.state, 'test')
    expect(store.state.allocationValues).toEqual({})
  })

  it('Clears all allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, 'test', allocValues)

    store.mutations.clearAllAllocationValues(store.state)
    expect(store.state.allocationValues).toEqual({})
  })

  it('Recomputes demand for a given month', () => {
    // No alloc values exist yet
    let monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 1)
    expect(monthQty).toEqual(100)

    // Set alloc values for 'test'
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, 'test', allocValues)
    monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 1)
    expect(monthQty).toEqual(300)

    monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 3)
    expect(monthQty).toEqual(0)
  })
})
