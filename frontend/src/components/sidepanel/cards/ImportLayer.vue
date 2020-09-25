<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo" icon="mdi-cloud-upload" icon-color="white" width="100%">
        <v-toolbar-title>Import a map layer</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5">
      <v-col>
        <p>Import a map layer</p>
      </v-col>
    </v-row>

      <div id="file-drag-drop">
        <form ref="fileform">
          <span class="drop-files"><v-icon>mdi-cloud-upload</v-icon> Drop the files here, or <a>browse</a></span>
        </form>
      </div>
          <v-file-input label="File" v-model="file"></v-file-input>
          <div v-if="fileLoading">
            <v-progress-linear show indeterminate></v-progress-linear>
          </div>
          <div v-if="file && fileStats">
            <div>
              Size: {{ fileStats.size }}
            </div>
            <div>
              Geometry type: {{ fileStats.geomType }}
            </div>
            <div v-if="fileStats.propertyFields">
              Available properties for each feature: {{ fileStats.propertyFields.join(', ') }}
            </div>
          </div>
          <v-alert class="my-3" v-if="file && fileStats.size > warnFileSizeThreshold" type="warning">Warning: file size greater than 10 mb. This file may take additional time to load and it may cause performance issues.</v-alert>
          <v-btn v-if="file" @click="importLayer" :loading="layerLoading">Import</v-btn>
          <v-alert v-if="message && status" :type="status">{{ message }}</v-alert>
  </v-container>
</template>
<style>
  #file-drag-drop form{
    display: block;
    height: 200px;
    width: 400px;
    background: #ccc;
    margin: auto;
    margin-top: 40px;
    text-align: center;
    line-height: 200px;
    border-radius: 4px;
  }
</style>
<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ImportLayer',
  data: () => ({
    warnFileSizeThreshold: 1e7, // 10 mb
    buttonClicked: false,
    distance: 0,
    area: 0,
    fileLoading: false,
    layerLoading: false,
    file: null, // the uploaded file from the form input
    fileData: null, // the file data object after being read by FileReader
    fileStats: {}, // statistics about the file from generateFileStats()
    message: null,
    status: null
  }),
  methods: {
    handleLoadLayer () {
      if (this.fileStats.fileType === 'geojson') {
        const geojsonFc = JSON.parse(this.fileData)

        geojsonFc.id = `${this.file.name}.${this.file.lastModified}`

        if (!geojsonFc.properties) {
          geojsonFc.properties = {}
        }

        geojsonFc.properties.name = this.file.name.split('.')[0]

        this.$store.dispatch('customLayers/loadCustomGeoJSONLayer', { map: this.map, featureCollection: geojsonFc, geomType: this.fileStats.geomType, color: 'blue' })
        setTimeout(() => {
          this.map.once('idle', () => {
            this.layerLoading = false
            this.resetFile()

            this.status = 'success'
            this.message = `Loaded file ${geojsonFc.properties.name}`
          })
        })
      }
    },
    importLayer () {
      this.layerLoading = true
      // after user has confirmed the selected file (including properties/options), import it into the map.
      // setTimeout calls the handleLoadLayer function after the UI has had a chance to render (progress bar shown
      // before app starts trying to load the layer, possibly causing some lag/delays)
      setTimeout(() => {
        this.handleLoadLayer()
      }, 0)
    },
    readFile () {
      this.fileLoading = true

      // read file from form input, store the result of FileReader() and generate statistics about the file.
      const reader = new FileReader()

      // set the onload function. this will be triggered when the file is read below.
      reader.onload = () => {
        this.fileData = reader.result
        this.fileStats = this.generateFileStats()
        this.fileLoading = false
      }

      // select read method and then read file, triggering the onload function.
      // shapefiles are read as arrayBuffers but most other filetypes are text.
      const readMethod = this.determineFileReadMethod(this.determineFileType(this.file.name))
      if (readMethod === 'text') {
        reader.readAsText(this.file)
      } else if (readMethod === 'arrayBuffer') {
        reader.readAsArrayBuffer(this.file)
      } else {
        console.error(`could not determine method for reading file ${this.file.name}`)
      }
    },
    generateFileStats () {
      // handling for GeoJSON types
      if (this.determineFileType(this.file.name) === 'geojson') {
        const geojsonFc = JSON.parse(this.fileData)

        const geojsonStats = {
          id: `${this.file.name}.${this.file.lastModified}`,
          fileType: 'geojson',
          numFeatures: geojsonFc.features.length,
          geomType: geojsonFc.features[0].geometry.type,
          propertyFields: Object.keys(geojsonFc.features[0].properties)
        }
        return Object.assign({}, this.defaultFileStats, geojsonStats)
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
    resetFile () {
      this.file = null
      this.fileData = null
      this.fileStats = {}
    },
    resetStatus () {
      this.message = null
      this.status = null
    }
  },
  computed: {
    defaultFileStats () {
      if (!this.file) {
        return null
      }

      const defaults = {
        size: this.file.size,
        name: this.file.name,
        type: this.file.type
      }
      return defaults
    },
    ...mapGetters('map', ['map'])
  },
  watch: {
    file (newFile, prevFile) {
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
