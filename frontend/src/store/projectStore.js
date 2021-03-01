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
      ApiService.query('/api/v1/projects')
        .then((r) => {
          // set unique ids for treeview to use
          let projects = r.data.map(project => {
            project.id = 'project-' + project.project_uuid
            let children = project.children.map(child => {
              child.id = 'document-' + child.project_document_uuid
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
    deleteProject ({ dispatch }, projectUUID) {
      if (!projectUUID) { return }
      ApiService.query(`/api/v1/projects/${projectUUID}/delete`)
        .then((r) => {
          dispatch('getProjects')
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    getProjectFiles ({ commit }, projectUUID) {
      if (!projectUUID) { return }
      ApiService.query(`/api/v1/projects/${projectUUID}/documents`)
        .then((r) => {
          commit('setProjectFiles', r.data)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    deleteProjectDocument ({ state, dispatch }, projectDocumentUUID) {
      if (!projectDocumentUUID) { return }
      ApiService.query(`/api/v1/projects/documents/${projectDocumentUUID}/delete`)
        .then((r) => {
          dispatch('getProjects')
          dispatch('getProjectFiles', state.selectedProject.project_uuid)
        }).catch((e) => {
          console.log('error delete project', e)
        })
    },
    downloadProject ({ state, commit }) {
      let projectUUID = state.selectedProject.project_uuid
      ApiService.query(`/api/v1/projects/${projectUUID}/download`, null, { responseType: 'arraybuffer' })
        .then((r) => {
          downloadFile(r, 'project_' + projectUUID, true)
          commit('downloadingFile', false)
        }).catch((e) => {
          commit('downloadingFile', false)
          console.log('error delete project', e)
        })
    },
    downloadProjectDocument ({ commit }, payload) {
      if (!payload.projectDocumentUUID) { return }
      commit('downloadingFile', true)
      ApiService.query(`/api/v1/projects/documents/${payload.projectDocumentUUID}`, null, { responseType: 'arraybuffer' })
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
