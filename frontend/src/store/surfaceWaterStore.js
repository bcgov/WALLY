export default {
  namespaced: true,
  state: {
    // Store monthly allocation values in this object
    // Example:
    //   { key: [1,1,1,1,1,1,1,1,1,1,1] }
    defaultAllocValue: 1,
    defaultAllocValues: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    allocationValues: { key: [] }
  },
  actions: {
    computeQuantityForMonth ({ state, dispatch }, qtyPerYear, allocItemKey, month) {
      dispatch('initAllocationItemIfNotExists', allocItemKey)

      let allocValues = state.allocationValues[allocItemKey]
      let allocFraction = allocValues[month - 1]
      return qtyPerYear * (allocFraction / 12)
    },
    loadAllocationItemsFromStorage ({ state }) {
      state.allocationValues =
        JSON.parse(localStorage.getItem('allocationItems')) || {}
    },
    initAllocationItemIfNotExists ({ state, commit, dispatch }, allocItemKey) {
      if (!(allocItemKey in state.allocationValues)) {
        commit('setAllocationValues', {
          key: allocItemKey,
          values: state.defaultAllocValues })
      }
    }
  },
  mutations: {
    setAllocationValues (state, item) {
      state.allocationValues[item.key] = item.values
    },
    saveAllocationValues (state) {
      localStorage.setItem('allocationItems',
        JSON.stringify(state.allocationValues))
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
    allocationValues: state => state.allocationValues,
    test: state => state.allocationValues
  }
}
