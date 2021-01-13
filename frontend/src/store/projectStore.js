// import ApiService from '../services/ApiService'
// import qs from 'querystring'

export default {
  state: {
    selectedProjectItem: {},
    activeFiles: [],
    projects: []
  },
  actions: {

  },
  mutations: {
    setSelectedProjectItem (state, payload) {
      state.selectedProjectItem = payload
    },
    setActiveFiles (state, files) {
      state.activeFiles = files
    }
  },
  getters: {
    selectedProjectItem: state => state.selectedProjectItem,
    activeFiles: state => state.activeFiles
  }
}
