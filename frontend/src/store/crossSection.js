export default {
  state: {
    sectionLine: null
  },
  mutations: {
    setSectionLine (state, payload) {
      state.sectionLine = payload
    },
    resetSectionLine (state, payload) {
      state.sectionLine = null
    }
  },
  getters: {
    sectionLine: state => state.sectionLine
  }
}
