<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo" icon="mdi-cloud-upload" icon-color="white" width="100%">
        <v-toolbar-title>Upload file or data</v-toolbar-title>
      </v-banner>
    </v-toolbar>
    <v-row>
      <v-col>
        <v-card flat>
          <v-card-text>
            <ImportLayerInstructions/>
          </v-card-text>
        </v-card>
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
import ImportLayerInstructions from '../../tools/import_layer/ImportLayerInstructions'
import FileDrop from '../../tools/import_layer/FileDrop'
import FileList from '../../tools/import_layer/FileList'
import FileListProcessed from '../../tools/import_layer/FileListProcessed'
import Importer from '../../../common/utils/Importer'

export default {
  name: 'ImportLayer',
  components: {
    ImportLayerInstructions,
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
    /**
     * Import a file that has already been loaded and processed
     * @param file
     */
    handleLoadLayer (file) {
      Importer.finalizeImport(file)
      this.map.once('idle', () => {
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

        // Read and prepare files for import
        Importer.readFiles(Array.from(this.fileList))
      }
    },
    importLayers () {
      this.queuedFiles.forEach(file => {
        this.handleLoadLayer(file)
      })
      this.fileList = []
    },
    ...mapMutations('importer', ['clearQueuedFiles', 'clearAllFiles', 'setFiles']),
    ...mapActions('importer', ['processFile'])
  },
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('importer', ['queuedFiles', 'processedFiles'])
  },
  watch: {
  },
  mounted () {
  },
  beforeDestroy () {
    this.cancelImport()
  }
}
</script>

<style>
</style>
