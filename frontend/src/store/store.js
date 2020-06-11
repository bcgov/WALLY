import router from '../router.js'
import ApiService from '../services/ApiService'
export default {
  state: {
    infoPanelVisible: true,
    app: {
      api_version: null,
      wally_env: 'development',
      wally_version: null
    }
  },
  actions: {
    async getAppInfo ({ commit }) {
      const appInfo = await ApiService.get('api/v1/config/version')
      commit('setAppInfo', appInfo.data)
    },
    exitFeature ({ dispatch }) {
      dispatch('map/clearSelections')
      dispatch('map/resizeMap')
      router.push('/')
    }
  },
  mutations: {
    setInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload
    },
    toggleInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload !== undefined ? payload : !state.infoPanelVisible
    },
    setAppInfo (state, payload) {
      global.config.debug && console.log('[wally]', state.app, payload)
      state.app.api_version = payload.api_version
      state.app.wally_env = payload.wally_env
      state.app.wally_version = payload.wally_version
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible,
    app: state => state.app
  }
}
