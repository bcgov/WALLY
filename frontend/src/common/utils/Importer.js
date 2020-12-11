import centroid from '@turf/centroid'
import {
  createMessageFromErrorArray,
  csvToGeoJSON, FILE_TYPE_SHAPEFILE,
  groupErrorsByRow, kmlToGeoJSON, xlsxToGeoJSON,
  shapefileToGeoJSON
} from './customLayerUtils'
import {
  generateFileStats, determineFileReadMethod,
  determineFileType
} from './fileUtils'
import store from '../../store/index'

/** Importer class */
export default class Importer {
  constructor () {
    if (this instanceof Importer) {
      throw Error('Cannot instantiate, Importer is a static class')
    }
  }

  /**
   * Go through each file and check if some of them should be grouped together
   * Shapefiles consist of multiple files that need to be processed together
   * @param {Array} files
   */
  static readFiles (files) {
    const groupedFiles = Importer.groupFiles(files)
    groupedFiles.forEach(x => {
      if (Object.keys(x.file).length > 1 && x.type === FILE_TYPE_SHAPEFILE) {
        Importer.readShapefile(x.file.shp, x.file.dbf, x.file.prj)
        return
      }
      Importer.readFile(x.file)
    })
  }

  /**
   * Given a list of files, find all shapefiles (fileTypes)
   * and remove them from the file list
   * @param files
   * @param fileName
   * @param fileTypes
   * @param returnObj
   * @returns {files: [], shapefiles: {}} object listing remaining files and shapefiles
   */
  static findShapefiles (files, fileName, fileTypes = ['shp', 'dbf', 'prj'], returnObj = { 'files': [], 'shapefiles': {} }) {
    if (fileTypes.length === 0) {
      return returnObj
    }
    const fileExtension = fileTypes.pop()
    let findFile = files.filter(e => e.name === fileName + '.' + fileExtension)

    files = files.filter(e => e.name !== fileName + '.' + fileExtension)
    returnObj.files = files
    returnObj['shapefiles'][fileExtension] = findFile.length === 1 ? findFile[0] : null

    return Importer.findShapefiles(files, fileName, fileTypes, returnObj)
  }

  /**
   * Go through the list of files and group together files that are supposed
   * to go together (i.e. shapefiles)
   * @param files
   * @param groupedFiles
   * @returns {*[]} Files grouped together if required by their fileType
   */
  static groupFiles (files = [], groupedFiles = []) {
    if (files.length === 0) {
      return groupedFiles
    }
    const fileToRead = files[0]

    const { fileType, fileSupported, fileExtension } = determineFileType(fileToRead.name)

    const fileName = fileToRead.name.replace(`.${fileExtension}`, '')
    if (String(fileType) === FILE_TYPE_SHAPEFILE) {
      const returnObj = Importer.findShapefiles(files, fileName)
      groupedFiles.push({
        'type': FILE_TYPE_SHAPEFILE,
        'extension': null,
        'supported': fileSupported,
        'file': returnObj.shapefiles
      })
      return Importer.groupFiles(returnObj.files, groupedFiles)
    }

    files = files.filter(e => e.name !== fileName + '.' + fileExtension)

    groupedFiles.push({
      'type': fileType,
      'extension': fileExtension,
      'supported': fileSupported,
      'file': fileToRead
    })
    return Importer.groupFiles(files, groupedFiles)
  }

  /**
   * Read a single (supported) file
   * @param {File} file
   */
  static readFile (file) {
    store.commit('importer/startLoadingFile', file.name)

    let { fileType, fileSupported, fileExtension } = determineFileType(file.name)
    if (!fileSupported) {
      fileExtension = fileExtension ? `.${fileExtension}` : 'None'
      store.dispatch('importer/processFile', {
        filenames: [file.name],
        status: 'error',
        message: `file of type ${fileExtension} not supported.`
      })

      store.commit('importer/clearQueuedFiles')

      // Custom Metrics - Import files
      window._paq && window._paq.push(['trackEvent', 'Upload files', 'Unsupported filetype', fileType])
      return
    }

    // read file from form input, store the result of FileReader() and generate statistics about the file.
    const reader = new FileReader()

    // set the onload function. this will be triggered when the file is read below.
    reader.onload = async () => {
      await Importer.processFileData(file, fileType, reader.result)
    }

    // select read method and then read file, triggering the onload function.
    // csvs are read as arrayBuffers but most other filetypes are text.
    const readMethod = determineFileReadMethod(fileType)
    if (readMethod === 'text') {
      reader.readAsText(file)
    } else if (readMethod === 'arrayBuffer') {
      reader.readAsArrayBuffer(file)
    } else {
      console.error(`could not determine method for reading file ${file.name}`)
    }
  }

  static async processFileData (file, fileType, data) {
    let fileInfo = {
      name: file.name || '',
      size: file.size || 0,
      color: '#' + Math.floor(Math.random() * 16777215).toString(16),
      lastModified: file.lastModified || null,
      lastModifiedDate: file.lastModifiedDate || null,
      type: file.type || null,
      webkitRelativePath: file.webkitRelativePath || null,
      options: {
        showAllProperties: false
      }
    }

    // place to store errors/warnings that some file handling libraries return (XLS, CSV)
    // other libraries throw an exception, so not all file types need the errors var.
    // let errors
    // let data

    // check file type and call the handler to convert the file to GeoJSON.
    // each file type has a different handler.
    // a try/catch is used for each type in order to generate a user error
    // message if there are any issues converting.
    if (fileType === 'csv') {
      fileInfo['data'] = await Importer.readCSV(file.name, data)
      // try {
      //   ({ data, errors } = await csvToGeoJSON(reader.result))
      //   global.config.debug && console.log(data)
      //   fileInfo['data'] = data
      //   if (errors && errors.length) {
      //     errors = groupErrorsByRow(errors)
      //     const warnMsg = createMessageFromErrorArray(errors)
      //     store.dispatch('importer/processFile', {
      //       filename: file.name,
      //       status: 'warning',
      //       message: `${errors.length} rows removed - ${warnMsg}`
      //     })
      //   }
      // } catch (e) {
      //   store.dispatch('importer/processFile', {
      //     filename: file.name,
      //     status: 'error',
      //     message: e.message ? e.message : e
      //   })
      //   return
      // }
    } else if (fileType === 'xlsx') {
      fileInfo['data'] = await Importer.readXLSX(file.name, data)
      // try {
      //   const fileData = new Uint8Array(reader.result);
      //   ({ data, errors } = await xlsxToGeoJSON(fileData))
      //   global.config.debug && console.log(data)
      //
      //   fileInfo['data'] = data
      //
      //   if (errors && errors.length) {
      //     errors = groupErrorsByRow(errors)
      //     const warnMsg = createMessageFromErrorArray(errors)
      //     store.dispatch('importer/processFile', {
      //       filename: file.name,
      //       status: 'warning',
      //       message: `${errors.length} rows removed - ${warnMsg}`
      //     })
      //   }
      // } catch (e) {
      //   store.dispatch('importer/processFile', {
      //     filename: file.name,
      //     status: 'error',
      //     message: e.message ? e.message : e
      //   })
      //   return
      // }
    } else if (fileType === 'kml') {
      fileInfo['data'] = Importer.readKML(file.name, data)
    } else if (fileType === 'geojson') {
      fileInfo['data'] = Importer.readGeoJSON(file.name, data)
      // return
    } else {
      // Unknown file type
      // this should not occur (an unsupported file error should have been caught earlier),
      // but log an error here for good measure in case this ever comes up.

      return console.error(`File ${file.name} does not have a -toGeoJSON handler and was not caught by file type check.`)
    }

    // // check if there are any features in the dataset
    // if (!fileInfo['data'].features) {
    //   store.dispatch('importer/processFile', {
    //     filename: file.name,
    //     status: 'error',
    //     message: 'file does not contain any valid features.'
    //   })
    //   return
    //   // return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file does not contain any valid features.' })
    // }
    if (fileInfo['data']) {
      global.config.debug && console.log('[wally]-------------------------------')
      global.config.debug && console.log('[wally]File has been loaded successfully')
      global.config.debug && console.log('[wally]-------------------------------')

      // TODO: Move this
      // Custom Metrics - Import files
      window._paq && window._paq.push(['trackEvent', 'Upload files', 'Uploaded Filetype', fileType])

      Importer.prepareLoadedFileForImport([file], fileInfo)
    }
  }

  static async readCSV (filename, contents) {
    let data, errors
    try {
      ({ data, errors } = await csvToGeoJSON(contents))
      global.config.debug && console.log(data)
      if (errors && errors.length) {
        errors = groupErrorsByRow(errors)
        const warnMsg = createMessageFromErrorArray(errors)
        await store.dispatch('importer/processFile', {
          filenames: [filename],
          status: 'warning',
          message: `${errors.length} rows removed - ${warnMsg}`
        })
      }
      return data
    } catch (e) {
      await store.dispatch('importer/processFile', {
        filenames: [filename],
        status: 'error',
        message: e.message ? e.message : e
      })
      // return
    }
  }

  static async readXLSX (filename, contents) {
    let data, errors
    try {
      const fileData = new Uint8Array(contents);
      ({ data, errors } = await xlsxToGeoJSON(fileData))
      global.config.debug && console.log(data)

      // fileInfo['data'] = data

      if (errors && errors.length) {
        errors = groupErrorsByRow(errors)
        const warnMsg = createMessageFromErrorArray(errors)
        await store.dispatch('importer/processFile', {
          filenames: [filename],
          status: 'warning',
          message: `${errors.length} rows removed - ${warnMsg}`
        })
      }

      return data
    } catch (e) {
      await store.dispatch('importer/processFile', {
        filenames: [filename],
        status: 'error',
        message: e.message ? e.message : e
      })
      // return
    }
  }

  static readKML (filename, contents) {
    try {
      return kmlToGeoJSON(contents)
    } catch (e) {
      store.dispatch('importer/processFile', {
        filenames: [filename],
        status: 'error',
        message: e.message
      })
      // return
    }
  }

  static readGeoJSON (filename, contents) {
    try {
      return JSON.parse(contents)
    } catch (e) {
      store.dispatch('importer/processFile', {
        filenames: [filename],
        status: 'error',
        message: 'file contains invalid JSON.'
      })
      // return
    }
  }

  /**
   *
   * @param shpFile
   * @param dbfFile
   * @param prjFile
   */
  static readShapefile (shpFile = null, dbfFile = null, prjFile = null) {
    if (!shpFile) {
      store.dispatch('importer/processFile', {
        filenames: [(dbfFile && dbfFile.name), (prjFile && prjFile.name)],
        // filename: [(dbfFile && dbfFile.name), (prjFile && prjFile.name)].filter(Boolean).join(', '),
        status: 'error',
        message: 'It looks like you\'re uploading a shapefile. Please' +
          ' provide the .shp file.'
      })
      // dbfFile && store.commit('importer/startLoadingFile', dbfFile.name)
      // prjFile && store.commit('importer/startLoadingFile', prjFile.name)
      return
    }

    let filenamesArr = [shpFile.name]
    let filesizeTotal = shpFile.size

    // Read file from form input
    const shpReader = new FileReader()
    let dbfReader, prjReader

    if (dbfFile) {
      dbfReader = new FileReader()
      filenamesArr.push(dbfFile.name)
      filesizeTotal += dbfFile.size
    }

    if (prjFile) {
      prjReader = new FileReader()
      filenamesArr.push(prjFile.name)
      filesizeTotal += prjFile.size
    }

    let fileInfo = {
      name: filenamesArr.join(', ') || '',
      size: filesizeTotal || 0,
      color: '#' + Math.floor(Math.random() * 16777215).toString(16),
      lastModified: '(.shp)' + shpFile.lastModified || null,
      lastModifiedDate: '(.shp)' + shpFile.lastModifiedDate || null,
      type: '(.shp)' + shpFile.type || null,
      webkitRelativePath: '(.shp)' + shpFile.webkitRelativePath || null,
      options: {
        showAllProperties: false
      }
    }

    const handleFileLoaded = async (e) => {
      const DONE = 2
      if (shpReader.readyState === DONE &&
          (dbfFile ? dbfReader.readyState === DONE : true) &&
          (prjFile ? prjReader.readyState === DONE : true)) {
        let dbfReaderResult = (dbfFile) ? dbfReader.result : null
        let prjReaderResult = (prjFile) ? prjReader.result : null
        fileInfo['data'] = await shapefileToGeoJSON(shpReader.result, dbfReaderResult, prjReaderResult)

        let fileQueue = [shpFile]
        if (dbfFile) {
          fileQueue.push(dbfFile)
        }
        if (prjFile) {
          fileQueue.push(prjFile)
        }
        Importer.prepareLoadedFileForImport(fileQueue, fileInfo)
        // store.commit('importer/setLoadingFile', {
        //   filename: shpFile.name,
        //   loading: false
        // })
        // dbfFile && store.commit('importer/stopLoadingFile', dbfFile.name)
        // prjFile && store.commit('importer/stopLoadingFile', prjFile.name)
      }
    }

    shpReader.addEventListener('loadend', handleFileLoaded)
    dbfFile && dbfReader.addEventListener('loadend', handleFileLoaded)
    prjFile && prjReader.addEventListener('loadend', handleFileLoaded)

    shpReader.readAsArrayBuffer(shpFile)
    dbfFile && dbfReader.readAsArrayBuffer(dbfFile)
    prjFile && prjReader.readAsText(prjFile)
  }

  /**
   * Files are read and loaded; let's prepare them for the final import
   * @param queuedFileGroup
   * @param fileInfo
   */
  static prepareLoadedFileForImport (queuedFileGroup, fileInfo) {
    // store.commit('importer/addQueuedFile', fileInfo)
    console.log('loaded file is', fileInfo)

    // check if there are any features in the dataset
    if (!fileInfo['data'].features) {
      store.dispatch('importer/processFile', {
        filenames: [fileInfo.filename],
        status: 'error',
        message: 'file does not contain any valid features.'
      })
      return
      // return
      // return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file does not contain any valid features.' })
    }

    // get the coordinates of the first feature.
    // this helps zoom to the dataset (if desired).
    let firstFeatureCoords = null
    try {
      firstFeatureCoords = Importer.validateAndReturnFirstFeatureCoords(fileInfo['data'])
    } catch (e) {
      let filenames = []
      queuedFileGroup.forEach(file => {
        filenames.push(file.name)
      })
      store.dispatch('importer/processFile', {
        filenames: [filenames],
        status: 'error',
        message: e.message
      })
      // queuedFileGroup.forEach(queuedFile => {
      //   store.dispatch('importer/processFile', {
      //     filename: queuedFile.name,
      //     status: 'error',
      //     message: e.message
      //   })
      // })
      return

      // return
    }

    fileInfo['firstFeatureCoords'] = firstFeatureCoords

    fileInfo['stats'] = generateFileStats(fileInfo)
    global.config.debug && console.log('[wally] fileInfo ', fileInfo)

    store.commit('importer/addQueuedFile', fileInfo)
  }

  static validateAndReturnFirstFeatureCoords (geojsonFc) {
    const firstFeatureGeom = centroid(geojsonFc.features.filter(f => Boolean(f.geometry))[0].geometry).geometry
    const firstFeature = [firstFeatureGeom.coordinates[0], firstFeatureGeom.coordinates[1]]

    // basic test to assert that the first feature is near BC.
    // this will only be a warning and will only be reliable if all the features are outside BC.
    // the most common case will be when users upload data in non WGS84 coordinate systems.
    // todo: investigate if better warnings are required based on user feedback.

    // using [-139.06 48.30],  [-114.03  60.00] as extents of BC.
    if (!(firstFeature[0] > -180 && firstFeature[0] < 180) || !(firstFeature[1] > -90 && firstFeature[1] < 90)) {
      throw new Error('Coordinates are not in degrees. If this is a' +
        ' shapefile, please upload a .prj file with the same name')
    }
    return firstFeature
  }

  static finalizeImport (file) {
    // file must be a GeoJSON FeatureCollection
    // this.layerLoading[file.name] = true
    store.commit('importer/startLoadingFile', file.name)

    const geojsonFc = file.data

    geojsonFc.id = `${file.name}.${file.lastModified}`

    if (!geojsonFc.properties) {
      geojsonFc.properties = {}
    }

    geojsonFc.properties.name = file.name.split('.')[0]

    const fileStatus = {
      filenames: [file.name]
    }

    const map = store.getters['map/map']
    // todo: set loading?

    store.dispatch('customLayers/loadCustomGeoJSONLayer', { map: map, featureCollection: geojsonFc, geomType: file.stats.geomType, color: file.color.substring(0, 7) })
      .then(() => {
        fileStatus.status = 'success'
        fileStatus.message = `file loaded`
        fileStatus.firstFeatureCoords = file.firstFeatureCoords
      }).catch((e) => {
        fileStatus.status = 'error'
        console.log(e)
        fileStatus.message = `error loading file ${file.name}: ${e}`
      }).finally(() => {
      // this.handleFileMessage(fileStatus)
      //   this.processFile(fileStatus)
        store.dispatch('importer/processFile', fileStatus)
        // this.$store.commit('importer/processFile', fileStatus)
        // this.layerLoading[file.name] = false
      })
    map.once('idle', () => {
      // this.resetFiles()
      // this.$store.commit('importer/setFiles', [])
      // this.setQueuedFiles([])
      store.commit('importer/clearQueuedFiles')
    })
  }
}
