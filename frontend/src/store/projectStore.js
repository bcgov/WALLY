import { downloadFile } from '../common/utils/exportUtils'
import ApiService from '../services/ApiService'
// import qs from 'querystring'

export default {
  state: {
    selectedProject: {},
    projectFiles: [],
    projects: [],
    loadingProjects: false,
    downloadingFile: false
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
      if (!projectId) { return }
      ApiService.query(`/api/v1/projects/${projectId}/delete`)
        .then((r) => {
          dispatch('getProjects')
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    getProjectFiles ({ commit }, projectId) {
      if (!projectId) { return }
      ApiService.query(`/api/v1/projects/${projectId}/documents`)
        .then((r) => {
          commit('setProjectFiles', r.data)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    deleteProjectDocument ({ state, dispatch }, projectDocumentId) {
      if (!projectDocumentId) { return }
      ApiService.query(`/api/v1/projects/documents/${projectDocumentId}/delete`)
        .then((r) => {
          dispatch('getProjects')
          dispatch('getProjectFiles', state.selectedProject.project_id)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    downloadProject ({ state, commit }) {
      let projectId = state.selectedProject.project_id
      ApiService.query(`/api/v1/projects/${projectId}/download`, null, { responseType: 'arraybuffer' })
        .then((r) => {
          downloadFile(r, 'project_' + projectId, true)
          commit('downloadingFile', false)
        }).catch((e) => {
          commit('downloadingFile', false)
          console.log('error delete project', e)
        })
    },
    downloadProjectDocument ({ commit }, payload) {
      if (!payload.projectDocumentId) { return }
      commit('downloadingFile', true)
      ApiService.query(`/api/v1/projects/documents/${payload.projectDocumentId}`, null, { responseType: 'arraybuffer' })
        .then((r) => {
          downloadFile(r, payload.filename)
          commit('downloadingFile', false)
        }).catch((e) => {
          commit('downloadingFile', false)
          console.log('error delete project', e)
        })
    },
    deselectProjects ({ commit }) {
      commit('setSelectedProject', {})
      commit('setProjectFiles', [])
    }
  },
  mutations: {
    setSelectedProject (state, payload) {
      state.selectedProject = payload
    },
    setProjectFiles (state, files) {
      state.projectFiles = files
    },
    setProjects (state, projects) {
      state.projects = projects
    },
    loadingProjects (state, val) {
      state.loadingProjects = val
    },
    downloadingFile (state, val) {
      state.downloadingFile = val
    }
  },
  getters: {
    selectedProject: state => state.selectedProject,
    projectFiles: state => state.projectFiles,
    projects: state => state.projects,
    loadingProjects: state => state.loadingProjects,
    downloadingFile: state => state.downloadingFile
  }
}
