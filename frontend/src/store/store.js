export default {
  state: {
    infoPanelVisible: true
  },
  mutations: {
    toggleInfoPanelVisibility (state) {
      state.infoPanelVisible = !state.infoPanelVisible
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible,
  }
}
