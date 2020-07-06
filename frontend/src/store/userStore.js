import ApiService from '../services/ApiService.js'
import AuthService from '../services/AuthService.js'

export default {
  state: {
    profile: {}
  },
  actions: {
    getUserProfile ({ commit }) {
      ApiService.post(`/api/v1/user/profile`, { uuid: AuthService.uuid }).then((r) => {
        commit('setUserProfile', r.data)
        console.log("User profile captured: " + r.data)
      })
    },
    updateDefaultMapLayers (mapLayers) {
      ApiService.post(`/api/v1/user/maplayers`, { 
        uuid: AuthService.uuid, 
        map_layers: mapLayers 
      }).then((r) => {
        console.log("updated user default map layers: " + r.data)
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
    defaultMapLayers: state => state.profile.map_layers,
  }
}
