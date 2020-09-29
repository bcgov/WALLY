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
    <div v-if="fileLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <FileDrop :file="file" @import:load-files="this.loadFiles"></FileDrop>
    <v-file-input label="File" v-model="files[0]"></v-file-input>
    <div v-for="file in files" v-bind:key="file">
      <dl v-if="file && file.name && fileStats[file.name]">
        <dt>
          Size:
        </dt>
        <dd>
          {{ fileStats[file.name].size ? `${(fileStats[file.name].size / 1e6).toFixed(2)} mb` : '' }}
        </dd>
        <dt>
          Geometry type:
        </dt>
        <dd> {{ fileStats[file.name].geomType }}</dd>
        <dt v-if="fileStats[file.name].propertyFields">
          Available properties for each feature:
        </dt>
        <dd>
          <div v-for="prop in fileStats[file.name].propertyFields" :key="`${file.name}${prop}`">{{prop}}</div>
        </dd>
      </dl>
      <v-alert class="my-3" v-if="file && fileStats[file.name].size > warnFileSizeThreshold" type="warning">Warning: file size greater than 10 mb. This file may take additional time to load and it may cause performance issues.</v-alert>
    </div>
    <v-btn v-if="files.length > 0" @click="importLayers" :loading="layerLoading">Import</v-btn>
    <v-alert v-if="message && status" :type="status">{{ message }}</v-alert>
  </v-container>
</template>
<style>

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
    fileLoading: false,
    layerLoading: false,
    file: null, // the uploaded file from the form input
    fileData: {}, // the file data object after being read by FileReader
    fileStats: {}, // statistics about the file from generateFileStats()
    message: null,
    status: null
  }),
  methods: {
    handleLoadLayer (file) {
      if (this.fileStats[file.name].fileType === 'geojson') {
        const geojsonFc = JSON.parse(this.fileData[file.name])

        geojsonFc.id = `${file.name}.${file.lastModified}`

        if (!geojsonFc.properties) {
          geojsonFc.properties = {}
        }

        geojsonFc.properties.name = file.name.split('.')[0]

        this.$store.dispatch('customLayers/loadCustomGeoJSONLayer', { map: this.map, featureCollection: geojsonFc, geomType: this.fileStats[file.name].geomType, color: 'blue' })
        setTimeout(() => {
          this.map.once('idle', () => {
            this.layerLoading = false
            this.resetFiles()

            this.status = 'success'
            this.message = `Loaded file ${geojsonFc.properties.name}`
          })
        })
      }
    },
    loadFiles (files) {
      console.log('load files', files)
      this.files = files
    },
    readFiles () {
      console.log(this.files)
      Array.from(this.files).forEach(file => {
        this.readFile(file)
      })
    },
    importLayers () {
      Array.from(this.files).forEach(file => {
        this.importLayer(file)
      })
    },
    importLayer (file) {
      this.layerLoading = true
      // after user has confirmed the selected file (including properties/options), import it into the map.
      // setTimeout calls the handleLoadLayer function after the UI has had a chance to render (progress bar shown
      // before app starts trying to load the layer, possibly causing some lag/delays)
      setTimeout(() => {
        this.handleLoadLayer(file)
      }, 0)
    },
    readFile (file) {
      this.fileLoading = true

      // read file from form input, store the result of FileReader() and generate statistics about the file.
      const reader = new FileReader()

      // set the onload function. this will be triggered when the file is read below.
      reader.onload = () => {
        this.fileData[file.name] = reader.result
        this.fileStats[file.name] = this.generateFileStats(file)
        this.fileLoading = false
      }

      // select read method and then read file, triggering the onload function.
      // shapefiles are read as arrayBuffers but most other filetypes are text.
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
        const geojsonFc = JSON.parse(this.fileData[file.name])

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
      this.fileData = {}
      this.fileStats = {}
    },
    resetFile () {
      // this.file = null
      this.fileData = {}
      this.fileStats = {}
    },
    resetStatus () {
      this.message = null
      this.status = null
    }
  },
  computed: {

    ...mapGetters('map', ['map'])
  },
  watch: {
    files (files) {
      this.readFiles()
    },
    file (newFile, prevFile) {
      console.log(newFile)
      if (!newFile) {
        return this.resetFile()
      }
      this.resetStatus()
      this.readFile()
    }
  },
  mounted () {
  }

}
</script>

<style>
</style>
