import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as surfaceWaterStore from '../../../src/store/surfaceWaterStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Map Store', () => {
  let store
  beforeEach(() => {
    store = surfaceWaterStore.default
    store.dispatch = jest.fn()
    // store.commit = jest.fn()
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
    let allocValues = [1, 1, 1, 1,
      1, 1, 1, 1,
      1, 1, 1, 1]
    store.mutations.setAllocationValues(store.state, 'test', allocValues)

    // No alloc values exist yet
    store.commit = jest.fn()
    let monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 1)
    expect(store.dispatch).toHaveBeenCalledWith(
      'initAllocationItemIfNotExists', 'test')

    // Alloc item default values
    console.log(store.state.allocationValues)
    expect(monthQty).toEqual(100)

    // Set alloc values for 'test'
    allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, 'test', allocValues)
    monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 1)
    expect(monthQty).toEqual(300)

    monthQty = store.actions.computeQuantityForMonth(store, 1200, 'test', 3)
    expect(monthQty).toEqual(0)
  })

  it('Initializes allocation item if it doesn\'t exist', () => {
    store.state.defaultAllocValue = 1
    store.actions.initAllocationItemIfNotExists(store, 'test2')
    let defaultAllocValue = 1
    let allocValues = []
    for (let i = 0; i < 12; i++) {
      allocValues.push(defaultAllocValue)
    }
    expect(store.commit).toHaveBeenCalledWith(
      'setAllocationValues', 'test2', allocValues
    )
  })
})
