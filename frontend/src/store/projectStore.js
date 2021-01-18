import { downloadFile } from '../common/utils/exportUtils'
import ApiService from '../services/ApiService'
// import qs from 'querystring'

export default {
  state: {
    selectedProjectItem: {},
    activeFiles: [],
    projects: [],
    loadingProjects: false
  },
  actions: {
    getProjects ({ commit, dispatch }) {
      commit('loadingProjects', true)
      ApiService.query('/api/v1/projects/')
        .then((r) => {
          // set unique ids for treeview to use
          let projects = r.data.map(project => {
            project.id = 'project-' + project.project_id
            let children = project.children.map(child => {
              child.id = 'document-' + child.project_document_id
              child.name = child.filename.split('.')[0]
              return child
            })
            project.children = children
            return project
          })
          commit('setProjects', projects)
          commit('loadingProjects', false)
        }).catch((e) => {
          console.log('error loading projects', e)
          commit('loadingProjects', false)
        })
    },
    deleteProject ({ dispatch }, projectId) {
      ApiService.query(`/api/v1/projects/${projectId}/delete`)
        .then((r) => {
          dispatch('getProjects')
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    deleteProjectDocument ({ dispatch }, projectDocumentId) {
      ApiService.query(`/api/v1/projects/documents/${projectDocumentId}/delete`)
        .then((r) => {
          dispatch('getProjects')
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    downloadProjectDocument ({ dispatch }, payload) {
      console.log(payload)
      ApiService.query(`/api/v1/projects/documents/${payload.projectDocumentId}`, null, { responseType: 'arraybuffer' })
        .then((r) => {
          downloadFile(r, payload.filename)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    }
  },
  mutations: {
    setSelectedProjectItem (state, payload) {
      state.selectedProjectItem = payload
    },
    setActiveFiles (state, files) {
      state.activeFiles = files
    },
    setProjects (state, projects) {
      state.projects = projects
    },
    loadingProjects (state, val) {
      state.loadingProjects = val
    }
  },
  getters: {
    selectedProjectItem: state => state.selectedProjectItem,
    activeFiles: state => state.activeFiles,
    loadingProjects: state => state.loadingProjects,
    projects: state => state.projects
  }
}
