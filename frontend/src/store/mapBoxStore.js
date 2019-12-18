/*
 Start slowly refactoring the map store into this file
 */
export default {
  namespaced: true,
  state: {
    infoPanelVisible: true
  },
  mutations: {
    toggleInfoPanelVisibility (state) {
      state.infoPanelVisible = !state.infoPanelVisible
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible
  }
}
