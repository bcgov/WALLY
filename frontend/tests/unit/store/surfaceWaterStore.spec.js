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
    store.commit = jest.fn()
  })

  it('Sets allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]

    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues })
    expect(store.state.allocationValues).toEqual({ 'test': allocValues })
  })

  it('Clears a set of allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues })
    expect(store.state.allocationValues).toEqual({ 'test': allocValues })

    store.mutations.clearAllocationValues(store.state, 'test')
    expect(store.state.allocationValues).toEqual({})
  })

  it('Clears all allocation values', () => {
    let allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues })

    store.mutations.clearAllAllocationValues(store.state)
    expect(store.state.allocationValues).toEqual({})
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
      'setAllocationValues', {
        key: 'test2',
        values: allocValues }
    )
  })

  // TODO: Add test to check if it populates from localStorage
})
