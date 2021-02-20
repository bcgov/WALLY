import ApiService from '../services/ApiService'

export default {
  state: {
    currentAnalysis: {},
    savedAnalyses: [],
    geometry: {},
    loadingSavedAnalyses: false
  },
  actions: {
    getSavedAnalyses ({ commit, dispatch }) {
      commit('loadingSavedAnalyses', true)
      ApiService.query('/api/v1/saved_analyses/')
        .then((r) => {
          const savedAnalyses = r.data
          // TODO
          commit('setSavedAnalyses', savedAnalyses)
          commit('loadingSavedAnalyses', false)
        }).catch((e) => {
          console.log('error loading saved analyses', e)
          commit('loadingSavedAnalyses', false)
        })
    },
    getSavedAnalysis ({ commit }, uuid) {
      if (!uuid) { return }
      ApiService.query(`/api/v1/saved_analyses/${uuid}`)
        .then((r) => {
          commit('setSavedAnalyses', r.data)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    deleteSavedAnalysis ({ dispatch }, uuid) {
      if (!uuid) { return }
      ApiService.query(`/api/v1/saved_analyses/${uuid}/delete`)
        .then((r) => {
          dispatch('getSavedAnalyses')
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    createSavedAnalysis ({ dispatch }, payload) {
    }
  },
  mutations: {
    setCurrentAnalysis (state, payload) {
      state.currentAnalysis = payload
    },
    setSavedAnalyses (state, files) {
      state.savedAnalyses = files
    },
    setGeometry (state, geometry) {
      state.geometry = geometry
    },
    loadingSavedAnalyses (state, val) {
      state.loadingSavedAnalyses = val
    }
  },
  getters: {
    currentAnalysis: state => state.currentAnalysis,
    savedAnalyses: state => state.savedAnalyses,
    projects: state => state.projects,
    loadingSavedAnalyses: state => state.loadingSavedAnalyses
  }
}
