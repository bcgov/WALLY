export default {
  state: {
    adjustableSidePanel: true
  },
  mutations: {
    toggleAdjustableSidePanel (state) {
      state.adjustableSidePanel = !state.adjustableSidePanel
    }
  },
  getters: {
    adjustableSidePanel: state => state.adjustableSidePanel
  }
}
