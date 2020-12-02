export default {
  namespaced: true,
  state: {
    fileList: [], // files dropped or selected from the computer
    // todo: rename this to queuedFiles
    files: [], // files queued to be processed
    loadingFiles: [], // status for files
    processedFiles: [], // files processed (whether successful or not)
    successFiles: [],
    errorFiles: []
  },
  mutations: {
    setFiles (state, files) {
      state.files = files
    },
    addFile (state, file) {
      state.files.push(file)
    },
    setLoadingFile (state, { filename, loading = true }) {
      console.log('set loading file', filename, loading)
      state.loadingFiles[filename] = loading
    },
    processFile (state, { filename, status, message, firstFeatureCoords }) {
      if (!['success', 'warning', 'error'].includes(status)) {
        throw new Error(`handleFileMessage called with invalid file status: ${status}`)
      }

      switch (status) {
        case 'success':
          state.successFiles.push({
            name: filename,
            status: status,
            message: `${filename}: ${message}`,
            firstFeatureCoords: firstFeatureCoords
          })
          break
        case 'warning':
          break
        case 'error':
          break
        default:
          break
      }

      state.processedFiles.push({
        name: filename,
        status: status,
        message: `${filename}: ${message}`,
        firstFeatureCoords: firstFeatureCoords
      })
    },
    clearFiles (state) {
      state.files = []
    },
    clearAllFiles (state) {
      state.processedFiles = []
      state.files = []
    }
  },
  getters: {
    files: state => state.files,
    loadingFiles: state => state.loadingFiles,
    processedFiles: state => state.processedFiles
  }
}
