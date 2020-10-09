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
        <p>Supported file types include: <strong>geojson, csv, xlsx, kml</strong></p>
        <p><strong>CSV</strong>: files should have two columns with the headings "Latitude" and "Longitude", or "lat" and "long" (not case sensitive).</p>
        <p><strong>Excel</strong>: workbooks with a table on the first sheet (and no other cells filled in outside the table) are supported. The same column heading rules as CSV files apply.</p>
        <p><strong>Supported coordinate system</strong>:  Degrees Longitude/Latitude (WGS84). e.g. -127.10205, 51.81051</p>
        <p>Large or complex spatial data may impact browser performance.</p>
      </v-col>
    </v-row>
    <v-row class="pl-5 pr-5">
     <v-col>

       <FileDrop @import:load-files="this.loadFiles"></FileDrop>
     </v-col>
    </v-row>
    <div v-for="(file, index) in files" class="mb-5" v-bind:key="index" id="fileList">

      <dl>
        <dt>
          Filename:
        </dt>
        <dd>
          {{file.name}}
        </dd>
      </dl>

      <v-progress-linear v-if="fileLoading[file.name]" show indeterminate></v-progress-linear>
      <dl v-if="file && file.name && file.stats">
        <dt>
          Colour:
        </dt>
        <dd>
          <v-color-picker
            hide-canvas
            hide-inputs
            v-model="file.color"
          ></v-color-picker>
        </dd>
        <dt>
          Size:
        </dt>
        <dd>
          {{ file.stats.size ? `${(file.stats.size / 1e6).toFixed(2)} mb` : '' }}
          <v-icon
            v-if="file && file.stats && file.stats.size > warnFileSizeThreshold"
            color="orange"
            small
          >mdi-alert</v-icon>
        </dd>
        <dt>
          Geometry type:
        </dt>
        <dd> {{ file.stats.geomType }}</dd>
        <dt>Total features:</dt>
        <dd>{{file.stats.numFeatures}}</dd>
        <dt v-if="file.stats.propertyFields">
          Feature properties:
        </dt>
        <dd>
          <v-row>
            <v-col>
              <div v-if="!file.options.showAllProperties">{{file.stats.propertyFields.length}} properties</div>
              <div v-else>
                <div v-for="prop in file.stats.propertyFields" :key="`${file.name}${prop}`">{{prop}}</div>
              </div>
            </v-col>
          <v-btn dense @click="file.options.showAllProperties = !file.options.showAllProperties">{{file.options.showAllProperties ? 'Hide' : 'Show'}}</v-btn>
            <v-col cols="2"></v-col>
          </v-row>
        </dd>
      </dl>
      <v-alert
        class="my-3"
        :id="`fileSizeWarning${index}`"
        v-if="file && file.size > warnFileSizeThreshold"
        type="warning"
      >
        {{file.name}}: file size greater than 10 mb. This file may take additional time to load and it may cause performance issues.
      </v-alert>
    </div>
    <div v-for="(processedFile,i) in processedFiles.filter(x => x.status)" :key="`fileMsg${i}`">
      <v-alert
        :id="`statusMessage${i}`"
        v-if="processedFile.message"
        :type="processedFile.status"
      >
        {{ processedFile.message }}
        <span class="float-right" v-if="processedFile.firstFeatureCoords">
          <v-btn text small @click="map.flyTo({center: processedFile.firstFeatureCoords})"><v-icon small>mdi-arrow-top-right</v-icon></v-btn>
        </span>
      </v-alert>
    </div>
    <v-btn class="my-5" v-if="files.length > 0" @click="importLayers" :loading="Object.values(layerLoading).some(Boolean)">Import</v-btn>
  </v-container>
</template>
<style lang="scss">
  #fileList {
    dl {
      display: flex;
      flex-wrap: wrap;
      padding-bottom: 10px;
    }

    dt {
      width: 33%;
      margin-top: 0;
      border-bottom: 1px solid lightgrey;
    }

    dd {
      padding-left: 10px;
      width: 66%;
      border-bottom: 1px solid lightgrey;
    }

    dt:nth-last-child(2), dd:last-child{
      border-bottom: none;
    }
  }
</style>
<script>
import { mapGetters } from 'vuex'
import FileDrop from '../../tools/FileDrop'
import csv2geojson from 'csv2geojson'
import { kml } from '@tmcw/togeojson'
import centroid from '@turf/centroid'
import XLSX from 'xlsx'

export default {
  name: 'ImportLayer',
  components: { FileDrop },
  data: () => ({
    warnFileSizeThreshold: 1e7, // 10 mb
    buttonClicked: false,
    distance: 0,
    area: 0,
    files: [],
    fileList: [],
    processedFiles: [],
    fileLoading: {},
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
          this.handleFileMessage(fileStatus)
          this.layerLoading[file.name] = false
        })
      this.map.once('idle', () => {
        this.resetFiles()
      })
    },
    xlsxToGeoJSON (file) {
      // file should be of type Uint8Array
      // returns a promise (via csvToGeoJSON)

      const workbook = XLSX.read(file, { type: 'array' })
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]]

      const csvData = XLSX.utils.sheet_to_csv(firstSheet)

      // Converting from xlsx directly to geojson would be more efficient
      // but we can only handle csv-like spreadsheets right now, so
      // by converting to csv first we can take advantage of the csv2geojson
      // library.
      return this.csvToGeoJSON(csvData)
    },
    createMessageFromErrorArray (errors) {
      if (!errors || !errors.length) {
        return ''
      }
      const numErrs = errors.length

      // get the first error.
      // some users spreadsheets have hundreds of rows so we won't
      // be able to show all possible errors.
      const firstErrRow = errors.map(e => e.index)[0]
      const firstErrMsg = errors.map(e => e.message)[0]

      let msg = `error on row ${firstErrRow}: ${firstErrMsg}`

      // show number of additional errors e.g. "and 2 more errors"
      if (numErrs > 1) {
        msg = `${msg} (and ${numErrs - 1} more ${numErrs === 2 ? 'error' : 'errors'})`
      }
      return msg
    },
    csvToGeoJSON (file) {
      console.log('converting csv to geojson')
      return new Promise((resolve, reject) => {
        csv2geojson.csv2geojson(file, (errors, data) => {
          if (data && data.features && data.features.length) {
            // check to make sure that features were given a geometry.
            // this can occur if the file was read but no lat/long columns were found.
            if (
              data.features &&
                data.features.length &&
                !data.features.map(f => f.geometry).filter(Boolean).length) {
              reject(new Error('could not find valid longitude and latitude headings in file.'))
            }
            resolve({ data, errors })
          } else {
            console.error(errors)

            const numErrs = errors && errors.length
            if (numErrs && numErrs > 0) {
              reject(new Error(this.createMessageFromErrorArray(errors)))
            }
            reject(new Error('An error occured loading file'))
          }
        })
      })
    },
    kmlToGeoJSON (xml) {
      return kml(new DOMParser().parseFromString(xml, 'text/xml'))
    },
    loadFiles (fileList) {
      this.fileList = fileList
      if (fileList.length > 0) {
        this.resetStatus()
        this.readFiles()
      }
    },
    readFiles () {
      // Reset files
      this.files = []
      Array.from(this.fileList).forEach(file => {
        this.fileLoading[file.name] = true
        this.readFile(file)
      })
    },
    importLayers () {
      this.files.forEach(file => {
        this.handleLoadLayer(file)
      })
    },
    validateAndReturnFirstFeatureCoords (geojsonFc) {
      const firstFeatureGeom = centroid(geojsonFc.features.filter(f => Boolean(f.geometry))[0].geometry).geometry
      const firstFeature = [firstFeatureGeom.coordinates[0], firstFeatureGeom.coordinates[1]]

      // basic test to assert that the first feature is near BC.
      // this will only be a warning and will only be reliable if all the features are outside BC.
      // the most common case will be when users upload data in non WGS84 coordinate systems.
      // todo: investigate if better warnings are required based on user feedback.

      // using [-139.06 48.30],  [-114.03  60.00] as extents of BC.
      if (!(firstFeature[0] > -180 && firstFeature[0] < 180) || !(firstFeature[1] > -90 && firstFeature[1] < 90)) {
        throw new Error('coordinates are not in degrees')
      }
      return firstFeature
    },

    handleFileMessage ({ filename, status, message, firstFeatureCoords }) {
      // handles file loading success/error messages.
      // takes an optional `firstFeatureCoords` that the user can zoom to.
      // ideally in the future this could also be the extents of the data (zoom to show full dataset),
      // for now, only the first available feature is shown.
      if (!['success', 'warning', 'error'].includes(status)) {
        throw new Error(`handleFileMessage called with invalid file status: ${status}`)
      }
      this.processedFiles.push({
        name: filename,
        status: status,
        message: `${filename}: ${message}`,
        firstFeatureCoords: firstFeatureCoords
      })
    },
    readFile (file) {
      const { fileType, fileSupported } = this.determineFileType(file.name)
      if (!fileSupported) {
        this.handleFileMessage({
          filename: file.name,
          status: 'error',
          message: `file of type ${fileType} not supported.`
        })
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
            ({ data, errors } = await this.csvToGeoJSON(reader.result))
            console.log(data)
            fileInfo['data'] = data
            if (errors && errors.length) {
              const warnMsg = this.createMessageFromErrorArray(errors)
              this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
            }
          } catch (e) {
            return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
          }
        } else if (fileType === 'xlsx') {
          try {
            const fileData = new Uint8Array(reader.result);
            ({ data, errors } = await this.xlsxToGeoJSON(fileData))
            console.log(data)

            fileInfo['data'] = data

            if (errors && errors.length) {
              const warnMsg = this.createMessageFromErrorArray(errors)
              this.handleFileMessage({ filename: file.name, status: 'warning', message: `${errors.length} rows removed - ${warnMsg}` })
            }
          } catch (e) {
            return this.handleFileMessage({ filename: file.name, status: 'error', message: e.message ? e.message : e })
          }
        } else if (fileType === 'kml') {
          try {
            fileInfo['data'] = this.kmlToGeoJSON(reader.result)
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
    },
    generateFileStats (file) {
      const geojsonFc = file['data']

      const geojsonStats = {
        id: `${file.name}.${file.lastModified}`,
        fileType: file['type'],
        numFeatures: geojsonFc.features.length,
        geomType: geojsonFc.features[0].geometry.type,
        propertyFields: Object.keys(geojsonFc.features[0].properties)
      }
      return Object.assign({}, this.getDefaultFileStats(file), geojsonStats)
    },
    determineFileReadMethod (filetype) {
      const methods = {
        'geojson': 'text',
        'csv': 'text',
        'xlsx': 'arrayBuffer',
        'shp': 'arrayBuffer',
        'kml': 'text'
      }
      return methods[filetype]
    },
    determineFileType (filename) {
      if (!filename || !filename.length) {
        // basic check for validity before trying to parse filename
        console.warn(`invalid filename ${filename}`)
        return null
      }
      const types = {
        'geojson': ['geojson', 'json'],
        // 'shp': ['shp', 'zip'],
        'csv': ['csv'],
        'xlsx': ['xls', 'xlsx'],
        'kml': ['kml']
      }

      const filenameParts = filename.split('.')
      const extension = filenameParts[filenameParts.length - 1]
      const typeOptions = Object.keys(types)
      for (let i = 0; i < typeOptions.length; i++) {
        const k = typeOptions[i]
        if (types[k].includes(extension)) {
          // filetype extension matched- return filetype key (geojson, shp, etc.)
          return {
            fileType: k,
            fileSupported: true
          }
        }
      }

      return { fileType: extension, fileSupported: false } // could not determine file type
    },
    getDefaultFileStats (file) {
      if (!file) {
        return null
      }

      return {
        size: file.size,
        name: file.name,
        type: file.type
      }
    },
    resetFiles () {
      this.files = []
    },
    resetStatus () {
      this.processedFiles = []
    }
  },
  computed: {
    ...mapGetters('map', ['map'])
  },
  watch: {
  },
  mounted () {
  }

}
</script>

<style>
</style>
