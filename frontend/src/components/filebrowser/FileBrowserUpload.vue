<template>
    <v-overlay :absolute="true">
        <v-card flat light class="mx-auto" :loading="loading">
            <v-card-text class="py-3 text-center">
                <div>
                    <span class="grey--text">Upload to:</span>
                    <v-chip color="info" class="mx-1">Project</v-chip>
                    <v-chip color="info" class="mx-1">{{selectedProject.name}}</v-chip>
                    <div class="grey--text">Accepted file types: .gif .jpg .jpeg .txt .geojson .json
                           .png .pdf .doc .docx .csv .xlsx .kml</div>
                </div>
                <div v-if="maxUploadFilesCount">
                    <span class="grey--text">Max files count: {{ maxUploadFilesCount }}</span>
                </div>
                <div v-if="maxUploadFileSize">
                    <span class="grey--text">Max file size: {{ formatBytes(maxUploadFileSize) }}</span>
                </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-text v-if="listItems.length" class="pa-0 files-list-wrapper">
                <v-list two-line v-if="listItems.length">
                    <v-list-item v-for="(file, index) in listItems" :key="index" link>
                        <v-list-item-avatar>
                            <v-img v-if="file.preview" :src="file.preview"></v-img>
                            <v-icon
                                v-else
                                v-text="icons[file.extension] || 'mdi-file'"
                                class="mdi-36px"
                                color="grey lighten-1"
                            ></v-icon>
                        </v-list-item-avatar>
                        <v-list-item-content>
                            <v-list-item-title v-text="file.name"></v-list-item-title>
                            <v-list-item-subtitle>{{ formatBytes(file.size) }} - {{ file.type }}</v-list-item-subtitle>
                        </v-list-item-content>
                        <v-list-item-action>
                            <v-btn icon @click="remove(index)">
                                <v-icon color="grey lighten-1">mdi-close</v-icon>
                            </v-btn>
                        </v-list-item-action>
                    </v-list-item>
                </v-list>
            </v-card-text>
            <v-card-text v-else class="py-6 text-center">
                <v-btn @click="$refs.inputUpload.click()">
                    <v-icon left>mdi-plus-circle</v-icon>Add files
                </v-btn>
            </v-card-text>
            <v-divider></v-divider>
            <v-toolbar dense flat>
                <div class="grow"></div>
                <v-btn text @click="cancel" class="mx-1">Cancel</v-btn>
                <v-btn depressed color="warning" @click="clear" class="mx-1" :disabled="!files">
                    <v-icon>mdi-close</v-icon>Clear
                </v-btn>
                <v-btn
                    :disabled="listItems.length >= maxUploadFilesCount"
                    depressed
                    color="info"
                    @click="$refs.inputUpload.click()"
                    class="mx-1"
                >
                    <v-icon left>mdi-plus-circle</v-icon>Add Files
                    <input
                        v-show="false"
                        ref="inputUpload"
                        type="file"
                        multiple
                        @change="add"
                    />
                </v-btn>
                <v-btn depressed color="success" @click="upload" class="ml-1" :disabled="!files">
                    Upload
                    <v-icon right>mdi-upload-outline</v-icon>
                </v-btn>
            </v-toolbar>
            <v-overlay :value="uploading" :absolute="true" color="white" opacity="0.9">
                <v-progress-linear v-model="progress" height="25" striped rounded reactive>
                    <strong>{{ Math.ceil(progress) }}%</strong>
                </v-progress-linear>
            </v-overlay>
        </v-card>
    </v-overlay>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import { formatBytes } from '../../common/utils/fileUtils'

const imageMimeTypes = ['image/png', 'image/jpeg']

export default {
  props: {
    endpoint: Object,
    files: { type: Array, default: () => [] },
    icons: Object,
    maxUploadFilesCount: { type: Number, default: 25 },
    maxUploadFileSize: { type: Number, default: 1000000 }
  },
  data () {
    return {
      loading: false,
      uploading: false,
      progress: 0,
      listItems: []
    }
  },
  computed: {
    ...mapGetters(['selectedProject'])
  },
  methods: {
    ...mapActions(['getProjects', 'getProjectFiles']),
    formatBytes,

    async filesMap (files) {
      const promises = Array.from(files).map(file => {
        const result = {
          name: file.name,
          type: file.type,
          size: file.size,
          extension: file.name.split('.').pop()
        }
        return new Promise(resolve => {
          if (!imageMimeTypes.includes(result.type)) {
            return resolve(result)
          }
          const reader = new FileReader()
          reader.onload = function (e) {
            result.preview = e.target.result
            resolve(result)
          }
          reader.readAsDataURL(file)
        })
      })

      return Promise.all(promises)
    },

    async add (event) {
      const files = Array.from(event.target.files)
      this.$emit('add-files', files)
      this.$refs.inputUpload.value = ''
    },

    remove (index) {
      this.$emit('remove-file', index)
      this.listItems.splice(index, 1)
    },

    clear () {
      this.$emit('clear-files')
      this.listItems = []
    },

    cancel () {
      this.$emit('cancel')
    },

    async upload () {
      const formData = new FormData()

      // files
      for (const file of this.files) {
        formData.append('files', file, file.name)
      }

      const url = `/api/v1/projects/${this.selectedProject.project_uuid}/documents`

      const config = {
        url,
        method: 'post',
        data: formData,
        onUploadProgress: progressEvent => {
          this.progress =
                        (progressEvent.loaded / progressEvent.total) * 100
        }
      }

      try {
        this.uploading = true
        const response = await ApiService.request(config)
        console.log('uploaded response', response)
        this.uploading = false
        this.$emit('uploaded')
        this.getProjects()
        this.getProjectFiles(this.selectedProject.project_uuid)
      } catch (e) {
        console.error(e)
        this.uploading = false
      }
    }
  },
  watch: {
    files: {
      deep: true,
      immediate: true,
      async handler () {
        this.loading = true
        this.listItems = await this.filesMap(this.files)
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .v-overlay__content {
    width: 90%;
    max-width: 500px;

    .files-list-wrapper {
        max-height: 250px;
        overflow-y: auto;
    }
}
</style>
