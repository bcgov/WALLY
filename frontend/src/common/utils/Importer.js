import {
  createMessageFromErrorArray,
  csvToGeoJSON, FILE_TYPES_ACCEPTED,
  groupErrorsByRow, kmlToGeoJSON, xlsxToGeoJSON
} from './customLayerUtils'
import { getFileExtension } from './fileUtils'
import EventBus from '../../services/EventBus'

export default class Importer {
  constructor () {
    if (this instanceof Importer) {
      throw Error('Cannot instantiate, Importer is a static class')
    }
  }

  /**
   * Reads a FileList
   * @param {Array} files
   */
  static readFiles (files) {
    files.forEach(file => {
      // Set loading file spinner
      // this.fileLoading[file.name] = true
      console.log('emitting....')
      EventBus.$emit('fileLoading', file.name)
      console.log('done emitting')

      const fileExtension = getFileExtension(file.name)
      const fileName = file.name.replace(`.${fileExtension}`, '')

      if (!FILE_TYPES_ACCEPTED['shapefile'].includes(fileExtension)) {
        Importer.readFile(file)
      } else if (fileExtension === 'shp') {
        // File is a shapefile, find other associated files
        let findDBFArr = files.filter(element => element.name === fileName + '.dbf')
        let findSHXArr = files.filter(element => element.name === fileName + '.shx')

        const dbfFile = findDBFArr.length === 1 ? findDBFArr[0] : null
        const shxFile = findSHXArr.length === 1 ? findSHXArr[0] : null

        Importer.readShapefile(file, dbfFile, shxFile)
      }
    })
  }

  /**
   *
   * @param {File} file
   */
  static readFile (file) {
    console.log("I'm in importer read file")
    const { fileType, fileSupported } = this.determineFileType(file.name)
    if (!fileSupported) {
      this.handleFileMessage({
        filename: file.name,
        status: 'error',
        message: `file of type ${fileType} not supported.`
      })
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
            this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
          }
        } catch (e) {
          return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
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
            this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
          }
        } catch (e) {
          return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
        }
      } else if (fileType === 'kml') {
        try {
          fileInfo['data'] = kmlToGeoJSON(reader.result)
        } catch (e) {
          return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
        }
      } else if (fileType === 'geojson') {
        try {
          fileInfo['data'] = JSON.parse(reader.result)
        } catch (e) {
          return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file contains invalid JSON.' })
        }
      } else {
        // Unknown file type
        // this should not occur (an unsupported file error should have been caught earlier),
        // but log an error here for good measure in case this ever comes up.

        return console.error(`File ${file.name} does not have a -toGeoJSON handler and was not caught by file type check.`)
      }

      // check if there are any features in the dataset
      if (!fileInfo['data'].features) {
        return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file does not contain any valid features.' })
      }

      console.log('-------------------------------')
      console.log('Imported')
      console.log('-------------------------------')
      // Custom Metrics - Import files
      window._paq && window._paq.push(['trackEvent', 'Upload files', 'Uploaded Filetype', fileType])

      // get the coordinates of the first feature.
      // this helps zoom to the dataset (if desired).
      // todo: in the future, zooming to the dataset extent might be nicer for users.
      let firstFeatureCoords = null
      try {
        firstFeatureCoords = this.validateAndReturnFirstFeatureCoords(fileInfo['data'])
      } catch (e) {
        return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
      }

      fileInfo['firstFeatureCoords'] = firstFeatureCoords

      fileInfo['stats'] = this.generateFileStats(fileInfo)
      global.config.debug && console.log('[wally] fileInfo ', fileInfo)
      this.files.push(fileInfo)

      this.fileLoading[file.name] = false
    }

    // select read method and then read file, triggering the onload function.
    // shapefiles are read as arrayBuffers but most other filetypes are text.
    const readMethod = this.determineFileReadMethod(fileType)
    if (readMethod === 'text') {
      reader.readAsText(file)
    } else if (readMethod === 'arrayBuffer') {
      reader.readAsArrayBuffer(file)
    } else {
      console.error(`could not determine method for reading file ${file.name}`)
    }
  }

  static determineFileType (filename) {
    const extension = getFileExtension(filename)
    for (const fileType of Object.keys(FILE_TYPES_ACCEPTED)) {
      if (FILE_TYPES_ACCEPTED[fileType].includes(extension)) {
        return {
          fileType: fileType,
          fileExtension: extension,
          fileSupported: true
        }
      }
    }

    // Could not determine file type based on file extension
    return {
      fileType: extension,
      fileExtension: extension,
      fileSupported: false
    }
  }

  static readShapefile (shpFile, dbfFile, shxFile) {
    console.log('Staring to read shapefile', shpFile, dbfFile, shxFile)

    // Skip determineFileType as we're only checking file name extensions
    // there and we're sure it's supported
    // const { dbfFileType, dbfFileExtension, dbfFileSupported } = Importer.determineFileType(dbfFile)
  }
}
