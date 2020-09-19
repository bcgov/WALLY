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
          <v-btn v-if="file" @click="importLayer" :loading="loading">Import</v-btn>
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
    buttonClicked: false,
    distance: 0,
    area: 0,
    loading: false,
    file: null, // the uploaded file from the form input
    fileData: null, // the file data object after being read by FileReader
    fileStats: {}, // statistics about the file from generateFileStats()
    message: null,
    status: null
  }),
  methods: {
    importLayer () {
      // after user has confirmed the selected file (including properties/options), import it into the map.
      if (this.fileStats.fileType === 'geojson') {
        const geojsonFc = JSON.parse(this.fileData)

        geojsonFc.id = `${this.file.name}.${this.file.lastModified}`

        if (!geojsonFc.properties) {
          geojsonFc.properties = {}
        }

        geojsonFc.properties.name = this.file.name.split('.')[0]

        this.$store.dispatch('loadCustomLayer', { map: this.map, featureCollection: geojsonFc, geomType: this.fileStats.geomType, color: 'blue' })
        this.loading = true
        setTimeout(() => {
          this.map.once('idle', () => {
            this.loading = false
            this.resetFile()

            this.status = 'success'
            this.message = `Loaded file ${geojsonFc.properties.name}`
          })
        })
      }
    },
    readFile () {
      // read file from form input, store the result of FileReader() and generate statistics about the file.
      const reader = new FileReader()
      reader.onload = () => {
        this.fileData = reader.result
        this.fileStats = this.generateFileStats()
      }
      reader.readAsText(this.file)
    },
    generateFileStats () {
      const mediatypes = {
        geojson: ['application/json', 'application/geojson', 'application/geo+json']
      }
      // handling for GeoJSON types
      if (mediatypes['geojson'].includes(this.file.type)) {
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
    resetFile () {
      this.file = null
      this.fileData = null
      this.fileStats = {}
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
      this.readFile()
    }
  },
  mounted () {
  }

}
</script>

<style>
</style>
