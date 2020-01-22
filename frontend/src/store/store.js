export default {
  state: {
    infoPanelVisible: true
  },
  mutations: {
    toggleInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload !== undefined ? payload : !state.infoPanelVisible
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible
  }
}
