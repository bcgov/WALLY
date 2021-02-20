import ApiService from '../services/ApiService.js'

var config = {}
if (process.env.VUE_APP_ENV === 'dev') {
  config = { headers: { 'X-Auth-UserId': '00000000-0000-0000-0000-00000' } }
}

export default {
  namespaced: true,
  state: {
    profile: {}
  },
  actions: {
    getUserProfile ({ commit, dispatch }) {
      ApiService.getApi(`/user/profile`, config).then((r) => {
        commit('setUserProfile', r.data)
      })
    },
    updateDefaultMapLayers ({ commit }, payload) {
      ApiService.post(`/api/v1/user/maplayers`, {
        map_layers: payload
      }, config).then((r) => {
        console.log('updated user default map layers: ' + r.data)
      })
    }
  },
  mutations: {
    setUserProfile (state, payload) {
      state.profile = payload
    }
  },
  getters: {
    profile: state => state.profile,
    defaultMapLayers: state => state.profile.default_map_layers
  }
}
