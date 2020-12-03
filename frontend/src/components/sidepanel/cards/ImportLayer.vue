<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo" icon="mdi-cloud-upload" icon-color="white" width="100%">
        <v-toolbar-title>Upload file or data</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col>
        <p>Choose files, data or layers to import from your computer, which will become temporarily available on the map.</p>
        <p>Supported file types include: geojson, csv, xlsx, kml</p>
        <p>Imported files require a location in order to be displayed. The supported coordinated system is decimal degrees longitude/latitude (WGS84).
            For example, -127.10205, 51.81051</p>
        <p>For CSV and Excel, the files should have two columns with the headings (not case sensitive): "Latitude" and "Longitude" or "lat" and "long".
            It works best to upload an Excel workbook that has a table on the first sheet (and no other cells filled in outside the table).</p>
        <p>Large or complex files may impact performance. A message will indicate if the file has been successfully uploaded.</p>
      </v-col>
    </v-row>
    <v-row class="pl-5 pr-5">
     <v-col>
       <FileDrop @import:load-files="this.loadFiles" v-if="files.length === 0"></FileDrop>
       <div v-if="files.length > 0" class="mb-5">
         <v-btn @click="clearAllFiles" small color="blue-grey lighten-4"><v-icon class="mr-2">mdi-restore</v-icon>Cancel import</v-btn>
       </div>
       <FileList :dropped-files="fileList"></FileList>
       <FileListImported :files="processedFiles"></FileListImported>
     </v-col>
    </v-row>
    <v-btn class="my-5" v-if="files.length > 0" @click="importLayers" :loading="Object.values(layerLoading).some(Boolean)">Import</v-btn>
  </v-container>
</template>
<script>
import { mapGetters, mapMutations } from 'vuex'
// import centroid from '@turf/centroid'
import FileDrop from '../../tools/import_layer/FileDrop'
import FileList from '../../tools/import_layer/FileList'
import FileListImported from '../../tools/import_layer/FileListImported'
// import {
//   createMessageFromErrorArray,
//   csvToGeoJSON,
//   kmlToGeoJSON,
//   xlsxToGeoJSON,
//   groupErrorsByRow
// } from '../../../common/utils/customLayerUtils'
import Importer from '../../../common/utils/Importer'

export default {
  name: 'ImportLayer',
  components: {
    FileDrop,
    FileList,
    FileListImported
  },
  data: () => ({
    warnFileSizeThreshold: 1e7, // 10 mb
    buttonClicked: false,
    distance: 0,
    area: 0,
    // files: [],
    fileList: [],
    // processedFiles: [],
    layerLoading: {},
    fileData: {}, // the file data object after being read by FileReader
    fileStats: {}, // statistics about the file from generateFileStats()
    message: null
  }),
  methods: {
    handleLoadLayer (file) {
      // file must be a GeoJSON FeatureCollection
      this.layerLoading[file.name] = true

      const geojsonFc = file.data

      geojsonFc.id = `${file.name}.${file.lastModified}`

      if (!geojsonFc.properties) {
        geojsonFc.properties = {}
      }

      geojsonFc.properties.name = file.name.split('.')[0]

      const fileStatus = {
        filename: file.name
      }

      this.$store.dispatch('customLayers/loadCustomGeoJSONLayer', { map: this.map, featureCollection: geojsonFc, geomType: file.stats.geomType, color: file.color.substring(0, 7) })
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
          this.processFile(fileStatus)
          // this.$store.commit('importer/processFile', fileStatus)
          this.layerLoading[file.name] = false
        })
      this.map.once('idle', () => {
        // this.resetFiles()
        // this.$store.commit('importer/setFiles', [])
        this.setFiles([])
      })
    },

    loadFiles (fileList) {
      this.fileList = fileList
      if (fileList.length > 0) {
        // this.resetStatus()
        this.clearAllFiles()

        // Start import
        // EventBus.$on('fileLoading', this.setFileLoading)
        Importer.readFiles(Array.from(fileList))
        // this.readFiles()
      }
    },
    // readFiles () {
    //   // Reset files
    //   this.files = []
    //   this.shapeFiles = []
    //   Array.from(this.fileList).forEach(file => {
    //     this.fileLoading[file.name] = true
    //
    //     // check if shape file
    //     console.log('read file', file, file.name.split('.'))
    //     const filename = file.name.split('.')
    //     console.log('file info', filename)
    //     // const { fileType, fileExtension, fileSupported } = this.determineFileType(file.name)
    //     // console.log('fileType', fileType, fileExtension, fileSupported)
    //
    //     if (filename[1] === 'shp') {
    //       // Find dbf...
    //       console.log(filename)
    //       let newArr = Array.from(this.fileList).filter(element => element.name === filename[0] + '.dbf')
    //       console.log('newarr', newArr)
    //       const dbfFile = newArr.length === 1 && newArr[0]
    //       this.readShapefile(file, dbfFile)
    //     } else if (filename[1] !== 'dbf') {
    //       this.readFile(file)
    //     }
    //   })
    // },
    importLayers () {
      this.files.forEach(file => {
        this.handleLoadLayer(file)
      })
    },
    // validateAndReturnFirstFeatureCoords (geojsonFc) {
    //   const firstFeatureGeom = centroid(geojsonFc.features.filter(f => Boolean(f.geometry))[0].geometry).geometry
    //   const firstFeature = [firstFeatureGeom.coordinates[0], firstFeatureGeom.coordinates[1]]
    //
    //   // basic test to assert that the first feature is near BC.
    //   // this will only be a warning and will only be reliable if all the features are outside BC.
    //   // the most common case will be when users upload data in non WGS84 coordinate systems.
    //   // todo: investigate if better warnings are required based on user feedback.
    //
    //   // using [-139.06 48.30],  [-114.03  60.00] as extents of BC.
    //   if (!(firstFeature[0] > -180 && firstFeature[0] < 180) || !(firstFeature[1] > -90 && firstFeature[1] < 90)) {
    //     throw new Error('coordinates are not in degrees')
    //   }
    //   return firstFeature
    // },
    // processFile ({ filename, status, message, firstFeatureCoords }) {
    //   this.processedFiles.push({
    //     name: filename,
    //     status: status,
    //     message: `${filename}: ${message}`,
    //     firstFeatureCoords: firstFeatureCoords
    //   })
    // },
    //
    // handleFileMessage ({ filename, status, message, firstFeatureCoords }) {
    //   // handles file loading success/error messages.
    //   // takes an optional `firstFeatureCoords` that the user can zoom to.
    //   // ideally in the future this could also be the extents of the data (zoom to show full dataset),
    //   // for now, only the first available feature is shown.
    //   if (!['success', 'warning', 'error'].includes(status)) {
    //     throw new Error(`handleFileMessage called with invalid file status: ${status}`)
    //   }
    //   this.processedFiles.push({
    //     name: filename,
    //     status: status,
    //     message: `${filename}: ${message}`,
    //     firstFeatureCoords: firstFeatureCoords
    //   })
    // },
    // readFile (file) {
    //   const { fileType, fileSupported } = this.determineFileType(file.name)
    //   if (!fileSupported) {
    //     this.handleFileMessage({
    //       filename: file.name,
    //       status: 'error',
    //       message: `file of type ${fileType} not supported.`
    //     })
    //     // Custom Metrics - Import files
    //     window._paq && window._paq.push(['trackEvent', 'Upload files', 'Unsupported filetype', fileType])
    //     return
    //   }
    //
    //   // read file from form input, store the result of FileReader() and generate statistics about the file.
    //   const reader = new FileReader()
    //
    //   // set the onload function. this will be triggered when the file is read below.
    //   reader.onload = async () => {
    //     let fileInfo = {
    //       name: file.name || '',
    //       size: file.size || 0,
    //       color: '#' + Math.floor(Math.random() * 16777215).toString(16),
    //       lastModified: file.lastModified || null,
    //       lastModifiedDate: file.lastModifiedDate || null,
    //       type: file.type || null,
    //       webkitRelativePath: file.webkitRelativePath || null,
    //       options: {
    //         showAllProperties: false
    //       }
    //     }
    //
    //     // place to store errors/warnings that some file handling libraries return (XLS, CSV)
    //     // other libraries throw an exception, so not all file types need the errors var.
    //     let errors
    //     let data
    //
    //     // check file type and call the handler to convert the file to GeoJSON.
    //     // each file type has a different handler.
    //     // a try/catch is used for each type in order to generate a user error
    //     // message if there are any issues converting.
    //     if (fileType === 'csv') {
    //       try {
    //         ({ data, errors } = await csvToGeoJSON(reader.result))
    //         console.log(data)
    //         fileInfo['data'] = data
    //         if (errors && errors.length) {
    //           errors = groupErrorsByRow(errors)
    //           const warnMsg = createMessageFromErrorArray(errors)
    //           this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
    //         }
    //       } catch (e) {
    //         return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
    //       }
    //     } else if (fileType === 'xlsx') {
    //       try {
    //         const fileData = new Uint8Array(reader.result);
    //         ({ data, errors } = await xlsxToGeoJSON(fileData))
    //         console.log(data)
    //
    //         fileInfo['data'] = data
    //
    //         if (errors && errors.length) {
    //           errors = groupErrorsByRow(errors)
    //           const warnMsg = createMessageFromErrorArray(errors)
    //           this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
    //         }
    //       } catch (e) {
    //         return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
    //       }
    //     } else if (fileType === 'kml') {
    //       try {
    //         fileInfo['data'] = kmlToGeoJSON(reader.result)
    //       } catch (e) {
    //         return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
    //       }
    //     } else if (fileType === 'geojson') {
    //       try {
    //         fileInfo['data'] = JSON.parse(reader.result)
    //       } catch (e) {
    //         return this.handleFileMessage({
    //           filename: file.name,
    //           status: 'error',
    //           message: 'file contains invalid JSON.'
    //         })
    //       }
    //     } else if (fileType === 'shapefile') {
    //       // process shapefile
    //       console.log('processing shapefile')
    //       // try {
    //       //   fileInfo['data'] = shapefileToGeoJSON(reader.result)
    //       // } catch (e) {
    //       //   return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
    //       // }
    //     } else {
    //       // Unknown file type
    //       // this should not occur (an unsupported file error should have been caught earlier),
    //       // but log an error here for good measure in case this ever comes up.
    //
    //       return console.error(`File ${file.name} does not have a -toGeoJSON handler and was not caught by file type check.`)
    //     }
    //
    //     // check if there are any features in the dataset
    //     if (!fileInfo['data'].features) {
    //       return this.handleFileMessage({ filename: file.name, status: 'error', message: 'file does not contain any valid features.' })
    //     }
    //
    //     console.log('-------------------------------')
    //     console.log('Imported')
    //     console.log('-------------------------------')
    //     // Custom Metrics - Import files
    //     window._paq && window._paq.push(['trackEvent', 'Upload files', 'Uploaded Filetype', fileType])
    //
    //     // get the coordinates of the first feature.
    //     // this helps zoom to the dataset (if desired).
    //     // todo: in the future, zooming to the dataset extent might be nicer for users.
    //     let firstFeatureCoords = null
    //     try {
    //       firstFeatureCoords = this.validateAndReturnFirstFeatureCoords(fileInfo['data'])
    //     } catch (e) {
    //       return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message })
    //     }
    //
    //     fileInfo['firstFeatureCoords'] = firstFeatureCoords
    //
    //     fileInfo['stats'] = this.generateFileStats(fileInfo)
    //     global.config.debug && console.log('[wally] fileInfo ', fileInfo)
    //     this.files.push(fileInfo)
    //
    //     this.fileLoading[file.name] = false
    //   }
    //
    //   // select read method and then read file, triggering the onload function.
    //   // shapefiles are read as arrayBuffers but most other filetypes are text.
    //   const readMethod = this.determineFileReadMethod(fileType)
    //   if (readMethod === 'text') {
    //     reader.readAsText(file)
    //   } else if (readMethod === 'arrayBuffer') {
    //     reader.readAsArrayBuffer(file)
    //   } else {
    //     console.error(`could not determine method for reading file ${file.name}`)
    //   }
    // },
    // generateFileStats (file) {
    //   const geojsonFc = file['data']
    //
    //   const geojsonStats = {
    //     id: `${file.name}.${file.lastModified}`,
    //     fileType: file['type'],
    //     numFeatures: geojsonFc.features.length,
    //     geomType: geojsonFc.features[0].geometry.type,
    //     propertyFields: Object.keys(geojsonFc.features[0].properties)
    //   }
    //   return Object.assign({}, this.getDefaultFileStats(file), geojsonStats)
    // },
    // determineFileReadMethod (filetype) {
    //   const methods = {
    //     'geojson': 'text',
    //     'csv': 'text',
    //     'xlsx': 'arrayBuffer',
    //     'shapefile': 'arrayBuffer',
    //     'kml': 'text'
    //   }
    //   return methods[filetype]
    // },
    // determineFileType (filename) {
    //   console.log(filename)
    //   if (!filename || !filename.length) {
    //     // basic check for validity before trying to parse filename
    //     console.warn(`invalid filename ${filename}`)
    //     return null
    //   }
    //   const types = {
    //     'geojson': ['geojson', 'json'],
    //     'shapefile': ['shp', 'dbf', 'zip'],
    //     'csv': ['csv'],
    //     'xlsx': ['xls', 'xlsx'],
    //     'kml': ['kml']
    //   }
    //
    //   const filenameParts = filename.split('.')
    //   const extension = filenameParts[filenameParts.length - 1]
    //   console.log('extension', extension)
    //   const typeOptions = Object.keys(types)
    //   for (let i = 0; i < typeOptions.length; i++) {
    //     const k = typeOptions[i]
    //     if (types[k].includes(extension)) {
    //       // filetype extension matched- return filetype key (geojson, shp, etc.)
    //       return {
    //         fileType: k,
    //         fileExtension: extension,
    //         fileSupported: true
    //       }
    //     }
    //   }
    //
    //   // Could not determine file type
    //   return {
    //     fileType: extension,
    //     fileExtension: extension,
    //     fileSupported: false
    //   }
    // },
    // getDefaultFileStats (file) {
    //   if (!file) {
    //     return null
    //   }
    //
    //   return {
    //     size: file.size,
    //     name: file.name,
    //     type: file.type
    //   }
    // },
    // clearFiles () {
    //   this.fileList = []
    //   this.processedFiles = []
    //   this.files = []
    // },
    resetStatus () {
      this.processedFiles = []
    },
    ...mapMutations('importer', ['clearFiles', 'clearAllFiles', 'processFile', 'setFiles'])
  },
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('importer', ['files', 'processedFiles'])
  },
  watch: {
  },
  mounted () {
  }

}
</script>

<style>
</style>
