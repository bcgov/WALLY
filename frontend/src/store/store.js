import router from '../router.js'
export default {
  state: {
    infoPanelVisible: true
  },
  actions: {
    exitFeature ({ dispatch }) {
      dispatch('map/clearSelections')
      router.push('/')
    }
  },
  mutations: {
    setInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload
    },
    toggleInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload !== undefined ? payload : !state.infoPanelVisible
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible
  }
}
