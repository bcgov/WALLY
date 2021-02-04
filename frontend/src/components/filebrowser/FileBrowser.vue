<template>
    <v-card class="mx-auto" :loading="loading > 0">
        <FileBrowserToolbar
            :endpoints="endpoints"
            v-on:add-files="addUploadingFiles"
            v-on:folder-created="refreshPending = true"
        ></FileBrowserToolbar>
        <v-row no-gutters>
            <v-col v-if="tree && $vuetify.breakpoint.smAndUp" sm="auto">
                <FileBrowserTreeView
                    :icons="icons"
                    :endpoints="endpoints"
                    :refreshPending="refreshPending"
                    v-on:loading="loadingChanged"
                    v-on:refreshed="refreshPending = false"
                ></FileBrowserTreeView>
            </v-col>
            <v-divider v-if="tree" vertical></v-divider>
            <v-col>
                <FileBrowserFileList
                    :icons="icons"
                    :endpoints="endpoints"
                    :refreshPending="refreshPending"
                    v-on:loading="loadingChanged"
                    v-on:refreshed="refreshPending = false"
                    v-on:file-deleted="refreshPending = true"
                ></FileBrowserFileList>
            </v-col>
        </v-row>
        <FileBrowserUpload
            v-if="uploadingFiles !== false"
            :files="uploadingFiles"
            :icons="icons"
            :endpoint="endpoints.upload"
            :maxUploadFilesCount="maxUploadFilesCount"
            :maxUploadFileSize="maxUploadFileSize"
            v-on:add-files="addUploadingFiles"
            v-on:remove-file="removeUploadingFile"
            v-on:clear-files="uploadingFiles = []"
            v-on:cancel="uploadingFiles = false"
            v-on:uploaded="uploaded"
        ></FileBrowserUpload>
    </v-card>
</template>

<script>
import FileBrowserToolbar from './FileBrowserToolbar.vue'
import FileBrowserTreeView from './FileBrowserTreeView.vue'
import FileBrowserFileList from './FileBrowserFileList.vue'
import FileBrowserUpload from './FileBrowserUpload.vue'

const endpoints = {
  projects: { url: '/api/v1/projects/', method: 'get' },
  createProject: { url: '/api/v1/projects/', method: 'post' },
  deleteProject: { url: '/api/v1/projects/delete', method: 'post' },

  documents: { url: '/api/v1/projects/{projectId}/documents', method: 'get' },
  upload: { url: '/api/v1/projects/{projectId}/documents', method: 'post' },
  delete: { url: '/api/v1/projects/documents/{documentId}/delete', method: 'delete' }
}

const fileIcons = {
  zip: 'mdi-folder-zip-outline',
  rar: 'mdi-folder-zip-outline',
  htm: 'mdi-language-html5',
  html: 'mdi-language-html5',
  js: 'mdi-nodejs',
  json: 'mdi-json',
  md: 'mdi-markdown',
  pdf: 'mdi-file-pdf',
  png: 'mdi-file-image',
  jpg: 'mdi-file-image',
  jpeg: 'mdi-file-image',
  mp4: 'mdi-filmstrip',
  mkv: 'mdi-filmstrip',
  avi: 'mdi-filmstrip',
  wmv: 'mdi-filmstrip',
  mov: 'mdi-filmstrip',
  txt: 'mdi-file-document-outline',
  xls: 'mdi-file-excel',
  other: 'mdi-file-outline'
}

export default {
  components: {
    FileBrowserToolbar,
    FileBrowserTreeView,
    FileBrowserFileList,
    FileBrowserUpload
  },
  model: {
    event: 'change'
  },
  props: {
    // show tree view
    tree: { type: Boolean, default: true },
    // file icons set
    icons: { type: Object, default: () => fileIcons },
    // custom backend endpoints
    endpoints: { type: Object, default: () => endpoints },
    // max files count to upload at once.
    maxUploadFilesCount: { type: Number, default: 25 },
    // max file size to upload.
    maxUploadFileSize: { type: Number, default: 1000000 }
  },
  data () {
    return {
      loading: 0,
      uploadingFiles: false, // or an Array of files
      refreshPending: false
    }
  },
  computed: {

  },
  methods: {
    loadingChanged (loading) {
      if (loading) {
        this.loading++
      } else if (this.loading > 0) {
        this.loading--
      }
    },
    addUploadingFiles (files) {
      files = Array.from(files)

      if (this.maxUploadFileSize) {
        files = files.filter(
          file => file.size <= this.maxUploadFileSize
        )
      }

      if (this.uploadingFiles === false) {
        this.uploadingFiles = []
      }

      if (this.maxUploadFilesCount && this.uploadingFiles.length + files.length > this.maxUploadFilesCount) {
        files = files.slice(0, this.maxUploadFilesCount - this.uploadingFiles.length)
      }

      this.uploadingFiles.push(...files)
    },
    removeUploadingFile (index) {
      this.uploadingFiles.splice(index, 1)
    },
    uploaded () {
      this.uploadingFiles = false
      this.refreshPending = true
    }
  },
  created () {
  },
  mounted () {
  }
}
</script>

<style lang="scss" scoped>
</style>
