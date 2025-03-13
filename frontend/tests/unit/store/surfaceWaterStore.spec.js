import { createLocalVue } from '@vue/test-utils'
import Vuex from 'vuex'
import * as surfaceWaterStore from '../../../src/store/surfaceWaterStore'

const localVue = createLocalVue()
localVue.use(Vuex)

describe('Surface Water Store tests', () => {
  let store
  beforeEach(() => {
    store = surfaceWaterStore.default
    store.dispatch = jest.fn()
    store.commit = jest.fn()
  })

  it('Sets allocation values', () => {
    const allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]

    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues
    })
    expect(store.state.allocationValues).toEqual({ test: allocValues })
  })

  it('Clears a set of allocation values', () => {
    const allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues
    })
    expect(store.state.allocationValues).toEqual({ test: allocValues })

    store.mutations.clearAllocationValues(store.state, 'test')
    expect(store.state.allocationValues).toEqual({})
  })

  it('Clears all allocation values', () => {
    const allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]
    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues
    })

    store.mutations.clearAllAllocationValues(store.state)
    expect(store.state.allocationValues).toEqual({})
  })

  it('Initializes allocation item if it doesn\'t exist', () => {
    store.state.defaultAllocValue = 1
    store.actions.initAllocationItemIfNotExists(store, 'test2')
    const defaultAllocValue = 1
    const allocValues = []
    for (let i = 0; i < 12; i++) {
      allocValues.push(defaultAllocValue)
    }
    expect(store.commit).toHaveBeenCalledWith(
      'setAllocationValues', {
        key: 'test2',
        values: allocValues
      }
    )
  })

  it('Initializes model inputs', () => {
    const watershedDetails = {
      scsb2016_model: {
      }
    }
    store.actions.initWatershedDetailsAndInputs(store, watershedDetails)
    expect(store.commit).toHaveBeenCalledWith(
      'setDefaultScsb2016ModelInputs',
      watershedDetails
    )
  })

  it('Changes model inputs and updates values ' +
    'dependent on model inputs', () => {
    // expect().toEqual()
    const newInputs = {
      drainage_area: 200
    }
    const watershedDetails = {
      scsb2016_model: {
      }
    }
    store.mutations.setCustomModelInputs(store.state, newInputs)
    expect(store.state.scsb2016ModelInputs).toEqual(newInputs)

    store.mutations.updateCustomScsb2016ModelData(store.state, watershedDetails)
    expect(store.state.watershedDetails.drainage_area).toEqual(200)
  })

  it('Resets model inputs to wally values', () => {
    const watershedDetails = {
      drainage_area: 150,
      scsb2016_model: {
      }
    }
    const newInputs = {
      drainage_area: 200
    }
    store.actions.initWatershedDetailsAndInputs(store, watershedDetails)
    store.mutations.setDefaultWatershedDetails(store.state, watershedDetails)
    expect(store.state.defaultWatershedDetails).toEqual(watershedDetails)

    store.mutations.setCustomModelInputs(store.state, newInputs)
    store.mutations.updateCustomScsb2016ModelData(store.state, watershedDetails)
    expect(store.state.watershedDetails.drainage_area)
      .toEqual(newInputs.drainage_area)

    store.actions.resetModelInputs(store)
    expect(store.commit).toHaveBeenCalledWith(
      'resetWatershedDetails'
    )

    store.mutations.resetWatershedDetails(store.state)
    expect(store.state.watershedDetails.drainage_area)
      .toEqual(watershedDetails.drainage_area)
    expect(store.state.watershedDetails.scsb2016_model)
      .toEqual(watershedDetails.scsb2016_model)
  })

  it('Sets custom inputs flag on when inputs are modified', () => {
    const watershedDetails = {
      drainage_area: 150,
      potential_evapotranspiration: 123,
      scsb2016_model: {
      }
    }
    const newInputs = {
      drainage_area: 200,
      evapo_transpiration: 456
    }
    expect(store.state.customModelInputsActive).toBeFalsy()
    store.actions.initWatershedDetailsAndInputs(store, watershedDetails)
    store.mutations.setDefaultWatershedDetails(store.state, watershedDetails)
    expect(store.state.defaultWatershedDetails).toEqual(watershedDetails)

    store.mutations.setCustomModelInputs(store.state, newInputs)
    store.mutations.updateCustomScsb2016ModelData(store.state, watershedDetails)
    expect(store.state.watershedDetails.drainage_area)
      .toEqual(newInputs.drainage_area)

    expect(store.state.customModelInputsActive).toBeTruthy()

    store.mutations.resetWatershedDetails(store.state)
    expect(store.state.customModelInputsActive).toBeFalsy()
  })

  it('Resets custom inputs flag when the reset button is clicked', () => {
    const watershedDetails = {
      drainage_area: 150,
      potential_evapotranspiration: 123,
      scsb2016_model: {
      }
    }
    const newInputs = {
      drainage_area: 200,
      evapo_transpiration: 456
    }
    expect(store.state.customModelInputsActive).toBeFalsy()
    store.actions.initWatershedDetailsAndInputs(store, watershedDetails)
    store.mutations.setDefaultWatershedDetails(store.state, watershedDetails)
    expect(store.state.defaultWatershedDetails).toEqual(watershedDetails)

    store.mutations.setCustomModelInputs(store.state, newInputs)
    store.mutations.updateCustomScsb2016ModelData(store.state, watershedDetails)
    expect(store.state.watershedDetails.drainage_area)
      .toEqual(newInputs.drainage_area)

    expect(store.state.customModelInputsActive).toBeTruthy()

    store.mutations.clearWatershedDetailsAndDefaults(store.state)
    expect(store.state.scsb2016ModelInputs).toBeNull()
  })

  it('Resets allocation values on clearWatershedDetailsAndDefaults', () => {
    const allocValues = [3, 3, 0, 0,
      0, 0, 0, 0,
      0, 0, 3, 3]

    store.mutations.setAllocationValues(store.state, {
      key: 'test',
      values: allocValues
    })
    expect(store.state.allocationValues).toEqual({ test: allocValues })
    store.mutations.clearWatershedDetailsAndDefaults(store.state)
    expect(store.state.allocationValues).toEqual({})
  })
})
