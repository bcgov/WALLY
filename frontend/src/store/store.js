export default {
  state: {
    infoPanelVisible: true
  },
  actions: {
    exitFeature ({ dispatch }) {
      dispatch('map/clearSelections')
      dispatch('map/resizeMap')
      router.push('/')
    }
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
