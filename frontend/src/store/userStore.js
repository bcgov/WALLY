import ApiService from '../services/ApiService.js'

export default {
  namespaced: true,
  state: {
    profile: {}
  },
  actions: {
    getUserProfile ({ commit, dispatch }, uuid) {
      ApiService.post(`/api/v1/user/profile`, { uuid: uuid }).then((r) => {
        commit('setUserProfile', r.data)
        console.log('User profile captured')
      })
    },
    updateDefaultMapLayers ({ commit }, payload) {
      ApiService.post(`/api/v1/user/maplayers`, payload).then((r) => {
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
