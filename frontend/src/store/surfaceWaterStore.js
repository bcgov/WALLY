export default {
  namespaced: true,
  state: {
    // Store monthly allocation values in this object
    // Example:
    //   { key: [1,1,1,1,1,1,1,1,1,1,1] }
    defaultAllocValue: 1,
    defaultAllocValues: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    allocationValues: {},
    // Watershed detail state objects
    watershedDetails: null,
    scsb2016ModelInputs: {
      hydrological_zone: 25,
      median_elevation: 1,
      glacial_coverage: 1,
      annual_precipitation: 1,
      evapo_transpiration: 1,
      drainage_area: 1,
      solar_exposure: 1,
      average_slope: 1
    },
  },
  actions: {
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
    },
    updateWatershedDetails ({state, commit}, payload) {
      commit('setWatershedDetails', payload)
      commit('resetEditableModelInputs', payload)
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
    },
    // Watershed detail mutations
    setWatershedDetails (state, payload) {
      state.watershedDetails = payload
    },
    updateCustomScsb2016ModelData (state, payload) {
      let sc = state.scsb2016ModelInputs
      state.watershedDetails = {
        watershed_area: sc.drainage_area * 1e6,
        drainage_area: sc.drainage_area,
        glacial_coverage: sc.glacial_coverage,
        annual_precipitation: sc.annual_precipitation,
        potential_evapotranspiration_thornthwaite: sc.evapo_transpiration,
        hydrological_zone: sc.hydrological_zone,
        average_slope: sc.average_slope,
        solar_exposure: sc.solar_exposure,
        median_elevation: sc.median_elevation,
        scsb2016_model: payload
      }
    },
    resetEditableModelInputs (state, payload) {
      if(payload === null) {
        state.scsb2016ModelInputs = {
          hydrological_zone: 25,
          median_elevation: 1,
          glacial_coverage: 1,
          annual_precipitation: 1,
          evapo_transpiration: 1,
          drainage_area: 1,
          solar_exposure: 1,
          average_slope: 1
        }
      } else {
        state.scsb2016ModelInputs = {
          hydrological_zone: payload.hydrological_zone,
          median_elevation: payload.median_elevation,
          glacial_coverage: payload.glacial_coverage,
          annual_precipitation: payload.annual_precipitation,
          evapo_transpiration: payload.evapo_transpiration,
          drainage_area: payload.drainage_area,
          solar_exposure: payload.solar_exposure,
          average_slope: payload.average_slope
        }
      }
    },
  },
  getters: {
    allocationValues: state => state.allocationValues,
    watershedDetails: state => state.watershedDetails,
    scsb2016ModelInputs: state => state.scsb2016ModelInputs
  }
}
