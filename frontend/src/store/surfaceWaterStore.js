export default {
  namespaced: true,
  state: {
    // Store monthly allocation values in this object
    // Example:
    //   { key: [1,1,1,1,1,1,1,1,1,1,1] }
    defaultAllocValue: 1,
    defaultAllocValues: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    allocationValues: {},
    shortTermAllocationValues: {},
    // Watershed detail state objects
    watershedDetails: null,
    defaultWatershedDetails: null,
    customModelInputsActive: false,
    defaultScsb2016ModelInputs: null,
    scsb2016ModelInputs: null,
    shortTermLicencePlotData: null,
    availabilityPlotData: null,
    licencePlotData: null
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
          values: state.defaultAllocValues
        })
      }
    },
    initShortTermAllocationItemIfNotExists ({ state, commit, dispatch }, allocItemKey) {
      if (!(allocItemKey in state.shortTermAllocationValues)) {
        commit('setShortTermAllocationValues', {
          key: allocItemKey,
          values: state.defaultAllocValues
        })
      }
    },
    initWatershedDetailsAndInputs ({ state, commit }, payload) {
      commit('clearWatershedDetailsAndDefaults')
      if (payload && payload.scsb2016_model && !payload.scsb2016_model.error) {
        commit('setDefaultScsb2016ModelInputs', payload)
      }
      commit('setDefaultWatershedDetails', payload)
    },
    resetModelInputs ({ state, commit }) {
      commit('resetWatershedDetails')
      commit('setEditableModelInputs', state.defaultScsb2016ModelInputs)
    }
  },
  mutations: {
    setAllocationValues (state, item) {
      state.allocationValues[item.key] = item.values
    },
    clearAllocationValues (state, key) {
      if (key in state.allocationValues) {
        delete state.allocationValues[key]
      }
    },
    clearAllAllocationValues (state) {
      state.allocationValues = {}
    },
    setShortTermAllocationValues (state, item) {
      state.shortTermAllocationValues[item.key] = item.values
    },
    clearShortTermAllocationValues (state, key) {
      if (key in state.shortTermAllocationValues) {
        delete state.shortTermAllocationValues[key]
      }
    },
    clearAllShortTermAllocationValues (state) {
      state.shortTermAllocationValues = {}
    },
    setAvailabilityPlotData (state, data) {
      state.availabilityPlotData = data
    },
    setShortTermLicencePlotData (state, data) {
      state.shortTermLicencePlotData = data
    },
    setLicencePlotData (state, data) {
      state.licencePlotData = data
    },
    clearAvailabilityVsDemandPlotData (state) {
      state.availabilityPlotData = null
      state.shortTermLicencePlotData = null
      state.licencePlotData = null
    },
    setDefaultWatershedDetails (state, payload) {
      state.defaultWatershedDetails = payload
      if (state.watershedDetails == null) {
        state.watershedDetails = state.defaultWatershedDetails
      }
    },
    resetWatershedDetails (state) {
      state.watershedDetails = state.defaultWatershedDetails
      state.scsb2016ModelInputs = state.defaultScsb2016ModelInputs
      state.customModelInputsActive = false
    },
    clearWatershedDetailsAndDefaults (state) {
      state.watershedDetails = null
      state.defaultWatershedDetails = null
      state.scsb2016ModelInputs = null
      state.defaultScsb2016ModelInputs = null
      state.customModelInputsActive = false
      state.allocationValues = {}
    },
    setCustomModelInputs (state, payload) {
      state.scsb2016ModelInputs = payload
    },
    updateCustomScsb2016ModelData (state, payload) {
      // Change Watershed Details depending on modified input data
      const sc = state.scsb2016ModelInputs
      // TODO: move this to set watershed details
      state.watershedDetails = {
        watershed_area: sc.drainage_area * 1e6,
        drainage_area: sc.drainage_area,
        glacial_coverage: sc.glacial_coverage,
        annual_precipitation: sc.annual_precipitation,
        potential_evapotranspiration: sc.evapo_transpiration,
        hydrological_zone: sc.hydrological_zone,
        average_slope: sc.average_slope,
        solar_exposure: sc.solar_exposure,
        median_elevation: sc.median_elevation,
        scsb2016_model: payload
      }
      state.customModelInputsActive = true
    },
    setDefaultScsb2016ModelInputs (state, payload) {
      state.defaultScsb2016ModelInputs = {
        hydrological_zone: payload.hydrological_zone,
        median_elevation: Math.round(payload.median_elevation * 100) / 100,
        glacial_coverage: Math.round(payload.glacial_coverage * 1000) / 1000,
        annual_precipitation: Math.round(payload.annual_precipitation * 100) / 100,
        evapo_transpiration: Math.round(payload.potential_evapotranspiration * 100) / 100,
        drainage_area: Math.round(payload.drainage_area * 100) / 100,
        solar_exposure: Math.round(payload.solar_exposure * 1000) / 1000,
        average_slope: Math.round(payload.average_slope * 100) / 100
      }
    },
    setEditableModelInputs (state, payload) {
      // state.customModelInputsActive = false
      state.scsb2016ModelInputs = {
        hydrological_zone: payload.hydrological_zone,
        median_elevation: Math.round(payload.median_elevation * 100) / 100,
        glacial_coverage: Math.round(payload.glacial_coverage * 1000) / 1000,
        annual_precipitation: Math.round(payload.annual_precipitation * 100) / 100,
        evapo_transpiration: Math.round(payload.evapo_transpiration * 100) / 100,
        drainage_area: Math.round(payload.drainage_area * 100) / 100,
        solar_exposure: Math.round(payload.solar_exposure * 1000) / 1000,
        average_slope: Math.round(payload.average_slope * 100) / 100
      }
    }
  },
  getters: {
    allocationValues: state => state.allocationValues,
    watershedDetails: state => state.watershedDetails,
    scsb2016ModelInputs: state => state.scsb2016ModelInputs || state.defaultScsb2016ModelInputs,
    customModelInputsActive: state => state.customModelInputsActive,
    shortTermLicencePlotData: state => state.shortTermLicencePlotData,
    availabilityPlotData: state => state.availabilityPlotData,
    licencePlotData: state => state.licencePlotData,
    shortTermAllocationValues: state => state.shortTermAllocationValues,
    defaultWatershedDetails: state => state.defaultWatershedDetails
  }
}
