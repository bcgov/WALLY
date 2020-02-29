export default {
  namespaced: true,
  state: {
    // Store monthly allocation values in this object
    // Example:
    //   { key: [1,1,1,1,1,1,1,1,1,1,1] }
    allocationValues: {}
  },
  actions: {
    computeQuantityForMonth ({ state }, qtyPerYear, allocKey, month) {
      let defaultAllocValue = 1
      let allocFraction

      let allocValues = (allocKey in state.allocationValues)
        ? state.allocationValues[allocKey]
        : []

      if (allocValues.length === 0) {
        allocFraction = defaultAllocValue
      } else {
        allocFraction = allocValues[month - 1]
      }
      return qtyPerYear * (allocFraction / 12)
    }
  },
  mutations: {
    setAllocationValues (state, key, values) {
      state.allocationValues[key] = values
    },
    clearAllocationValues (state, key) {
      if (key in state.allocationValues) {
        delete state.allocationValues[key]
      }
    },
    clearAllAllocationValues (state) {
      state.allocationValues = {}
    }
  },
  getters: {
    allocationValues: state => state.allocationValues
  }
}
