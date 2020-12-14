export default {
  namespaced: true,
  state: {
    fileList: [], // files dropped or selected from the computer
    queuedFiles: [], // files queued to be processed
    loadingFiles: [], // status for files,
    processedFiles: {
      success: [],
      error: [],
      warning: []
    }
  },
  actions: {
    processFile ({ commit, state }, { filenames, status, message, firstFeatureCoords }) {
      if (!['success', 'warning', 'error'].includes(status)) {
        throw new Error(`handleFileMessage called with invalid file status: ${status}`)
      }

      let filenamesStr = filenames.filter(Boolean).join(', ')

      let processedFile = {
        name: filenamesStr,
        status: status,
        message: `${filenamesStr}: ${message}`
      }

      if (status === 'success') {
        processedFile['firstFeatureCoords'] = firstFeatureCoords
      }

      filenames.forEach(file => {
        commit('stopLoadingFile', file)
      })
      commit('setProcessedFile', { status, processedFile })
    }
  },
  mutations: {
    setQueuedFiles (state, queuedFiles) {
      state.queuedFiles = queuedFiles
    },
    addQueuedFile (state, file) {
      state.queuedFiles.push(file)
    },
    stopLoadingFile (state, filename) {
      state.loadingFiles = state.loadingFiles.filter(x => x !== filename)
    },
    startLoadingFile (state, filename) {
      state.loadingFiles.push(filename)
    },
    setProcessedFile (state, { status, processedFile }) {
      state.processedFiles[status].push(processedFile)
    },
    clearQueuedFiles (state) {
      state.queuedFiles = []
      state.loadingFiles = []
    },
    clearAllFiles (state) {
      state.processedFiles = {
        success: [],
        error: [],
        warning: []
      }
      state.loadingFiles = []
      state.queuedFiles = []
    }
  },
  getters: {
    queuedFiles: state => state.queuedFiles,
    loadingFiles: state => state.loadingFiles,
    processedFiles: state => state.processedFiles,
    isFileLoading: state => filename => state.loadingFiles.find((x) => x && x === filename)
  }
}
