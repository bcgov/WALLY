export default {
  namespaced: true,
  state: {
    fileList: [], // files dropped or selected from the computer
    // todo: rename this to queuedFiles
    queuedFiles: [], // files queued to be processed
    loadingFiles: [], // status for files,
    processedFiles: {
      success: [],
      error: [],
      warning: []
    }
  },
  actions: {
    processFile ({ commit, state }, { filename, status, message, firstFeatureCoords }) {
      // console.log(state, state.processedFiles)
      if (!['success', 'warning', 'error'].includes(status)) {
        throw new Error(`handleFileMessage called with invalid file status: ${status}`)
      }

      let processedFile = {
        name: filename,
        status: status,
        message: `${filename}: ${message}`
      }

      if (status === 'success') {
        processedFile['firstFeatureCoords'] = firstFeatureCoords
        // state.processedFiles.success.push(processedFile)
      // } else if (status === 'warning' || status === 'error') {
      //   state.processedFiles[status].push(processedFile)
      }

      commit('setLoadingFile', { filename, loading: false })
      commit('setProcessedFile', { status, processedFile })

      // state.processedFiles.push({
      //   name: filename,
      //   status: status,
      //   message: `${filename}: ${message}`,
      //   firstFeatureCoords: firstFeatureCoords
      // })
    }
  },
  mutations: {
    setQueuedFiles (state, queuedFiles) {
      state.queuedFiles = queuedFiles
    },
    addQueuedFile (state, file) {
      state.queuedFiles.push(file)
    },
    setLoadingFile (state, { filename, loading = true }) {
      console.log('set loading file', filename, loading)
      state.loadingFiles[filename] = loading
    },
    setProcessedFile (state, { status, processedFile }) {
      state.processedFiles[status].push(processedFile)
    },
    clearQueuedFiles (state) {
      state.queuedFiles = []
    },
    clearAllFiles (state) {
      state.processedFiles = {
        success: [],
        error: [],
        warning: []
      }
      state.queuedFiles = []
    }
  },
  getters: {
    queuedFiles: state => state.queuedFiles,
    loadingFiles: state => state.loadingFiles,
    processedFiles: state => state.processedFiles
  }
}
