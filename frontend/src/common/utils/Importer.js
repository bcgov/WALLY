import centroid from '@turf/centroid'
import {
  createMessageFromErrorArray,
  csvToGeoJSON, FILE_TYPES_ACCEPTED,
  groupErrorsByRow, kmlToGeoJSON, xlsxToGeoJSON,
  shapefileToGeoJSON
} from './customLayerUtils'
import {
  getFileExtension, generateFileStats, determineFileReadMethod,
  determineFileType
} from './fileUtils'
import store from '../../store/index'

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
    files.forEach(file => {
      // Set loading file spinner
      store.commit('importer/setLoadingFile', {
        filename: file.name,
        loading: true
      })

      const fileExtension = getFileExtension(file.name)
      const fileName = file.name.replace(`.${fileExtension}`, '')

      if (!FILE_TYPES_ACCEPTED['shapefile'].includes(fileExtension)) {
        Importer.readFile(file)
      } else if (fileExtension === 'shp') {
        // File is a shapefile, find other associated files
        let findDBFArr = files.filter(element => element.name === fileName + '.dbf')
        let findSHXArr = files.filter(element => element.name === fileName + '.shx')
        let findPRJArr = files.filter(element => element.name === fileName + '.prj')

        const dbfFile = findDBFArr.length === 1 ? findDBFArr[0] : null
        const shxFile = findSHXArr.length === 1 ? findSHXArr[0] : null
        const prjFile = findPRJArr.length === 1 ? findPRJArr[0] : null

        Importer.readShapefile(file, dbfFile, prjFile)
      } else if (fileExtension === 'zip') {
        // Install `unzip` package to unpack zip file which contains
        // multiple files for shapefiles.
      }
    })
  }

  /**
   * Read a single (supported) file
   * @param {File} file
   */
  static readFile (file) {
    const { fileType, fileSupported, fileExtension } = determineFileType(file.name)
    if (!fileSupported) {
      // this.handleFileMessage({
      //   filename: file.name,
      //   status: 'error',
      //   message: `file of type ${fileType} not supported.`
      // })
      store.commit('importer/processFile', {
        filename: file.name,
        status: 'error',
        message: `file of type .${fileExtension} not supported.`
      })

      store.commit('importer/clearFiles')

      // EventBus
      // Custom Metrics - Import files
      window._paq && window._paq.push(['trackEvent', 'Upload files', 'Unsupported filetype', fileType])
      return
    }

    // read file from form input, store the result of FileReader() and generate statistics about the file.
    const reader = new FileReader()

    // set the onload function. this will be triggered when the file is read below.
    reader.onload = async () => {
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
      let errors
      let data

      // check file type and call the handler to convert the file to GeoJSON.
      // each file type has a different handler.
      // a try/catch is used for each type in order to generate a user error
      // message if there are any issues converting.
      if (fileType === 'csv') {
        try {
          ({ data, errors } = await csvToGeoJSON(reader.result))
          console.log(data)
          fileInfo['data'] = data
          if (errors && errors.length) {
            errors = groupErrorsByRow(errors)
            const warnMsg = createMessageFromErrorArray(errors)
            store.commit('importer/processFile', {
              filename: file.name,
              status: 'warning',
              message: `${errors.length} rows removed - ${warnMsg}`
            })
            // this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
          }
        } catch (e) {
          store.commit('importer/processFile', {
            filename: file.name,
            status: 'error',
            message: e.message ? e.message : e
          })
          return
          // return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
        }
      } else if (fileType === 'xlsx') {
        try {
          const fileData = new Uint8Array(reader.result);
          ({ data, errors } = await xlsxToGeoJSON(fileData))
          console.log(data)

          fileInfo['data'] = data

          if (errors && errors.length) {
            errors = groupErrorsByRow(errors)
            const warnMsg = createMessageFromErrorArray(errors)
            store.commit('importer/processFile', {
              filename: file.name,
              status: 'warning',
              message: `${errors.length} rows removed - ${warnMsg}`
            })
            // this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
          }
        } catch (e) {
          store.commit('importer/processFile', {
            filename: file.name,
            status: 'error',
            message: e.message ? e.message : e
          })
          return
          // return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
        }
      } else if (fileType === 'kml') {
        try {
          fileInfo['data'] = kmlToGeoJSON(reader.result)
        } catch (e) {
          store.commit('importer/processFile', {
            filename: file.name,
            status: 'error',
            message: e.message
          })
          return
          // return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
        }
      } else if (fileType === 'geojson') {
        try {
          fileInfo['data'] = JSON.parse(reader.result)
        } catch (e) {
          store.commit('importer/processFile', {
            filename: file.name,
            status: 'error',
            message: 'file contains invalid JSON.'
          })
          return
          // return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file contains invalid JSON.' })
        }
      } else {
        // Unknown file type
        // this should not occur (an unsupported file error should have been caught earlier),
        // but log an error here for good measure in case this ever comes up.

        return console.error(`File ${file.name} does not have a -toGeoJSON handler and was not caught by file type check.`)
      }

      // check if there are any features in the dataset
      if (!fileInfo['data'].features) {
        store.commit('importer/processFile', {
          filename: file.name,
          status: 'error',
          message: 'file does not contain any valid features.'
        })
        return
        // return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file does not contain any valid features.' })
      }

      console.log('-------------------------------')
      console.log('Imported')
      console.log('-------------------------------')
      // Custom Metrics - Import files
      window._paq && window._paq.push(['trackEvent', 'Upload files', 'Uploaded Filetype', fileType])

      Importer.queueFile([file], fileInfo)

      store.commit('importer/setLoadingFile', {
        filename: file.name,
        loading: false
      })
      // this.fileLoading[file.name] = false
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

  /**
   *
   * @param shpFile
   * @param dbfFile
   * @param prjFile
   */
  static readShapefile (shpFile, dbfFile = null, prjFile = null) {
    console.log('Staring to read shapefile', shpFile, dbfFile, prjFile)

    // Read file from form input
    const shpReader = new FileReader()
    let dbfReader, prjReader
    if (dbfFile) {
      dbfReader = new FileReader()
    }

    if (prjFile) {
      prjReader = new FileReader()
    }

    // TODO: Concat all files into name and size
    let fileInfo = {
      name: shpFile.name || '',
      size: shpFile.size || 0,
      color: '#' + Math.floor(Math.random() * 16777215).toString(16),
      lastModified: shpFile.lastModified || null,
      lastModifiedDate: shpFile.lastModifiedDate || null,
      type: shpFile.type || null,
      webkitRelativePath: shpFile.webkitRelativePath || null,
      options: {
        showAllProperties: false
      }
    }

    const handleFileLoaded = async (e) => {
      console.log(e)
      console.log('shapefile loaded?', shpReader.readyState)
      dbfFile && console.log('dbf loaded?', dbfReader.readyState)

      const DONE = 2
      if (shpReader.readyState === DONE &&
          (dbfFile ? dbfReader.readyState === DONE : true) &&
          (prjFile ? prjReader.readyState === DONE : true)) {
        console.log('shp result', shpReader.result)
        dbfFile && console.log('dbf result', dbfReader.result)

        let dbfReaderResult = (dbfFile) ? dbfReader.result : null
        let prjReaderResult = (prjFile) ? prjReader.result : null
        fileInfo['data'] = await shapefileToGeoJSON(shpReader.result, dbfReaderResult, prjReaderResult)
        console.log('--------DATA--------')
        console.log(fileInfo['data'], fileInfo['data'].features[0])
        console.log('------END DATA------')
        let fileQueue = [shpFile]
        if (dbfFile) {
          fileQueue.push(dbfFile)
        }
        if (prjFile) {
          fileQueue.push(prjFile)
        }
        Importer.queueFile(fileQueue, fileInfo)
        store.commit('importer/setLoadingFile', {
          filename: shpFile.name,
          loading: false
        })
        dbfFile && store.commit('importer/setLoadingFile', {
          filename: dbfFile.name,
          loading: false
        })
        prjFile && store.commit('importer/setLoadingFile', {
          filename: prjFile.name,
          loading: false
        })
      }
    }

    shpReader.addEventListener('loadend', handleFileLoaded)
    dbfFile && dbfReader.addEventListener('loadend', handleFileLoaded)
    prjFile && prjReader.addEventListener('loadend', handleFileLoaded)

    shpReader.readAsArrayBuffer(shpFile)
    dbfFile && dbfReader.readAsArrayBuffer(dbfFile)
    prjFile && prjReader.readAsText(prjFile)
  }

  static queueFile (queuedFileGroup, fileInfo) {
    // get the coordinates of the first feature.
    // this helps zoom to the dataset (if desired).
    let firstFeatureCoords = null
    try {
      firstFeatureCoords = Importer.validateAndReturnFirstFeatureCoords(fileInfo['data'])
    } catch (e) {
      queuedFileGroup.forEach(queuedFile => {
        store.commit('importer/processFile', {
          filename: queuedFile.name,
          status: 'error',
          message: e.message
        })
      })

      return
      // return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
    }

    fileInfo['firstFeatureCoords'] = firstFeatureCoords

    fileInfo['stats'] = generateFileStats(fileInfo)
    global.config.debug && console.log('[wally] fileInfo ', fileInfo)
    // this.files.push(fileInfo)

    store.commit('importer/addFile', fileInfo)
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
}
