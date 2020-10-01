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
        <p>Supported files types include: <em>.geojson</em></p>
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
      <v-alert class="my-3" v-if="file && file.size > warnFileSizeThreshold" type="warning">{{file.name}}: file size greater than 10 mb. This file may take additional time to load and it may cause performance issues.</v-alert>
    </div>
    <v-btn v-if="files.length > 0" @click="importLayers" :loading="Object.values(layerLoading).some(Boolean)">Import</v-btn>
    <div v-for="(processedFile,i) in processedFiles.filter(x => x.status)" :key="`fileMsg${i}`">
      <v-alert v-if="processedFile.message" :type="processedFile.status">{{ processedFile.message }}</v-alert>
    </div>
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
      // if (this.fileStats[file.name].fileType === 'geojson') {
      if (file.stats.fileType === 'geojson') {
        const geojsonFc = JSON.parse(file.data)

        geojsonFc.id = `${file.name}.${file.lastModified}`

        if (!geojsonFc.properties) {
          geojsonFc.properties = {}
        }

        geojsonFc.properties.name = file.name.split('.')[0]

        this.$store.dispatch('customLayers/loadCustomGeoJSONLayer', { map: this.map, featureCollection: geojsonFc, geomType: file.stats.geomType, color: 'blue' })
      }
    },
    loadFiles (fileList) {
      global.config.debug && console.log('[wally] loading files', fileList)
      this.fileList = fileList
    },
    readFiles () {
      global.config.debug && console.log('[wally] reading files', this.files)
      // Reset files
      this.files = []
      Array.from(this.fileList).forEach(file => {
        this.fileLoading[file.name] = true
        setTimeout(() => {
          this.readFile(file)
        }, 0)
      })
    },
    importLayers () {
      this.files.forEach(file => {
        this.importLayer(file)
      })
    },
    importLayer (file) {
      this.layerLoading[file.name] = true
      // after user has confirmed the selected file (including properties/options), import it into the map.
      // setTimeout calls the handleLoadLayer function after the UI has had a chance to render (progress bar shown
      // before app starts trying to load the layer, possibly causing some lag/delays)
      setTimeout(() => {
        this.handleLoadLayer(file)

        setTimeout(() => {
          this.map.once('idle', () => {
            this.layerLoading[file.name] = false
            this.resetFiles()

            // create a fileStatus object to be filled in below
            // based on whether the layer was successfully created or not
            const fileStatus = {
              name: file.name
            }

            // note: need a better way to manage this, based on errors
            // that might have occured while loading.  this code just
            // checks that the layer exists after everything has been loaded
            // onto the map (will not be true if errors occured loading the layer).
            if (this.map.getLayer(`${file.name}.${file.lastModified}`)) {
              fileStatus.status = 'success'
              fileStatus.message = `Loaded file ${file.name}`
            } else {
              fileStatus.status = 'error'
              fileStatus.message = `Could not load file ${file.name}`
            }
            this.processedFiles.push(fileStatus)
          })
        })
      }, 0)
    },
    readFile (file) {
      // read file from form input, store the result of FileReader() and generate statistics about the file.
      const reader = new FileReader()

      // set the onload function. this will be triggered when the file is read below.
      reader.onload = () => {
        let fileInfo = {
          name: file.name || '',
          size: file.size || 0,
          lastModified: file.lastModified || null,
          lastModifiedDate: file.lastModifiedDate || null,
          type: file.type || null,
          webkitRelativePath: file.webkitRelativePath || null,
          options: {
            showAllProperties: false
          }
        }
        fileInfo['data'] = reader.result
        fileInfo['stats'] = this.generateFileStats(fileInfo)
        global.config.debug && console.log('[wally] fileInfo ', fileInfo)
        this.files.push(fileInfo)

        this.fileLoading[file.name] = false
      }

      // select read method and then read file, triggering the onload function.
      // shapefiles are read as arrayBuffers but most other filetypes are text.
      console.log(file, file.name)
      const readMethod = this.determineFileReadMethod(this.determineFileType(file.name))
      if (readMethod === 'text') {
        reader.readAsText(file)
      } else if (readMethod === 'arrayBuffer') {
        reader.readAsArrayBuffer(file)
      } else {
        console.error(`could not determine method for reading file ${file.name}`)
      }
    },
    generateFileStats (file) {
      // handling for GeoJSON types
      if (this.determineFileType(file.name) === 'geojson') {
        // const geojsonFc = JSON.parse(this.fileData[file.name])
        const geojsonFc = JSON.parse(file['data'])

        const geojsonStats = {
          id: `${file.name}.${file.lastModified}`,
          fileType: 'geojson',
          numFeatures: geojsonFc.features.length,
          geomType: geojsonFc.features[0].geometry.type,
          propertyFields: Object.keys(geojsonFc.features[0].properties)
        }
        return Object.assign({}, this.getDefaultFileStats(file), geojsonStats)
      }
    },
    determineFileReadMethod (filetype) {
      const methods = {
        'geojson': 'text',
        'csv': 'text',
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
        'shp': ['shp', 'zip'],
        'csv': ['csv'],
        'kml': ['kml']
      }

      const filenameParts = filename.split('.')
      const extension = filenameParts[filenameParts.length - 1]
      const typeOptions = Object.keys(types)
      for (let i = 0; i < typeOptions.length; i++) {
        const k = typeOptions[i]
        if (types[k].includes(extension)) {
          // filetype extension matched- return filetype key (geojson, shp, etc.)
          return k
        }
      }
      return null // could not determine file type
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
    fileList (fileList) {
      if (fileList.length > 0) {
        this.resetStatus()
        this.readFiles()
      }
    }
  },
  mounted () {
  }

}
</script>

<style>
</style>
