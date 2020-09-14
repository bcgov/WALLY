import router from '../router.js'
import ApiService from '../services/ApiService'
export default {
  state: {
    infoPanelVisible: true,
    infoPanelWidth: 800,
    app: {
      api_version: null,
      wally_env: 'development',
      wally_version: null,
      config: {}
    }
  },
  actions: {
    async getAppInfo ({ commit }) {
      const appInfo = await ApiService.get('api/v1/config/version')
      commit('setAppInfo', appInfo.data)
    },
    async getAppConfig ({ commit }) {
      const appInfo = await ApiService.get('api/v1/config/')
      commit('setAppConfig', appInfo.data)
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
    setInfoPanelWidth (state, payload) {
      state.infoPanelWidth = payload
    },
    toggleInfoPanelVisibility (state, payload) {
      state.infoPanelVisible = payload !== undefined ? payload : !state.infoPanelVisible
    },
    setAppInfo (state, payload) {
      global.config.debug && console.log('[wally]', state.app, payload)
      state.app.api_version = payload.api_version
      state.app.wally_env = payload.wally_env
      state.app.wally_version = payload.wally_version
    },
    setAppConfig (state, payload) {
      global.config.debug && console.log('[wally]', state.app, payload)
      if (global && global.config) {
        global.config.app = payload
      }
      state.app.config = payload
    }
  },
  getters: {
    infoPanelVisible: state => state.infoPanelVisible,
    infoPanelWidth: state => state.infoPanelWidth,
    app: state => state.app
  }
}
