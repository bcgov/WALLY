export default {
  state: {
    infoPanelVisible: false
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
