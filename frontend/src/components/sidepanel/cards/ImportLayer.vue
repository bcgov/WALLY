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
        <p>Supported file types include: geojson, csv, xlsx, kml, shapefiles (shp, dbf, prj)</p>
        <p>Imported files require a location in order to be displayed. The supported coordinated system is decimal degrees longitude/latitude (WGS84).
            For example, -127.10205, 51.81051</p>
        <p>For CSV and Excel, the files should have two columns with the headings (not case sensitive): "Latitude" and "Longitude" or "lat" and "long".
            It works best to upload an Excel workbook that has a table on the first sheet (and no other cells filled in outside the table).</p>
        <p>Shapefiles must include both the .shp and .prj. Uploading the .dbf is also recommended if you want to view features and properties of the layer.</p>
        <p>Large or complex files may impact performance. A message will indicate if the file has been successfully uploaded.</p>
      </v-col>
    </v-row>
    <v-row class="pl-5 pr-5">
     <v-col>
       <FileDrop @import:load-files="this.handleSelectedFiles" v-if="fileList.length === 0"></FileDrop>
       <div v-if="fileList.length > 0" class="mb-5">
         <v-btn @click="cancelImport" small color="blue-grey lighten-4">
           <v-icon class="mr-2">mdi-restore</v-icon>Cancel import
         </v-btn>
       </div>
       <FileList :dropped-files="fileList"></FileList>
       <FileListProcessed :files="processedFiles"></FileListProcessed>
     </v-col>
    </v-row>
    <v-btn class="my-5" v-if="fileList.length > 0 && queuedFiles.length===0" @click="prepareFiles" :loading="Object.values(layerLoading).some(Boolean)">
      Prepare files for import (1/2)
    </v-btn>
    <v-btn class="my-5" v-if="queuedFiles.length > 0" @click="importLayers" :loading="Object.values(layerLoading).some(Boolean)">
      Import Layer(s) (2/2)
    </v-btn>
  </v-container>
</template>
<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import FileDrop from '../../tools/import_layer/FileDrop'
import FileList from '../../tools/import_layer/FileList'
import FileListProcessed from '../../tools/import_layer/FileListProcessed'
import Importer from '../../../common/utils/Importer'

export default {
  name: 'ImportLayer',
  components: {
    FileDrop,
    FileList,
    FileListProcessed
  },
  data: () => ({
    warnFileSizeThreshold: 1e7, // 10 mb
    buttonClicked: false,
    distance: 0,
    area: 0,
    fileList: [],
    layerLoading: {},
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
        // this.setQueuedFiles([])
        this.clearQueuedFiles()
      })
    },
    cancelImport () {
      this.clearAllFiles()
      this.fileList = []
    },
    handleSelectedFiles (fileList) {
      this.clearAllFiles()
      this.fileList = fileList
    },
    prepareFiles () {
      if (this.fileList.length > 0) {
        this.clearAllFiles()

        // Prepare files for import
        Importer.readFiles(Array.from(this.fileList))
      }
    },
    importLayers () {
      this.queuedFiles.forEach(file => {
        this.handleLoadLayer(file)
      })
      this.fileList = []
    },
    ...mapMutations('importer', ['clearQueuedFiles', 'clearAllFiles', 'processFile', 'setFiles']),
    ...mapActions('importer', ['processFile'])
  },
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('importer', ['queuedFiles', 'processedFiles'])
  },
  watch: {
  },
  mounted () {
  }

}
</script>

<style>
</style>
