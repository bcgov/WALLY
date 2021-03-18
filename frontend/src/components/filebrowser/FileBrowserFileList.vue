<template>
    <v-card flat tile min-height="250" class="d-flex flex-column">
        <FileBrowserConfirmDialog ref="confirm"></FileBrowserConfirmDialog>
        <v-card-subtitle v-if="selectedProject.description">Project Description: {{selectedProject.description}}</v-card-subtitle>
        <v-card-text v-if="files.length > 0" class="grow">
            <v-list subheader v-if="files.length > 0">
                <v-subheader>Files</v-subheader>
                <v-list-item
                    v-for="item in files"
                    :key="item.project_document_uuid"
                    class="pl-0"
                >
                    <v-list-item-avatar class="ma-0">
                        <v-icon>{{ icons[fileExtension(item.filename)] || icons['other'] }}</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content class="py-2">
                        <v-list-item-title v-text="item.filename"></v-list-item-title>
                        <v-list-item-subtitle>{{ formattedDate(item.create_date) }}</v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                        <v-btn
                          icon
                          @click.stop="downloadItem(item)"
                          :disabled="downloadingFile"
                        >
                          <v-icon v-if="!downloadingFile" color="grey lighten-1">mdi-download</v-icon>
                          <v-progress-circular
                            v-if="downloadingFile"
                            indeterminate
                            size=16
                            class="mr-1"
                            color="secondary"
                          ></v-progress-circular>
                        </v-btn>
                    </v-list-item-action>
                    <v-list-item-action>
                        <v-btn icon @click.stop="deleteItem(item)">
                          <v-icon color="grey lighten-1">mdi-delete-outline</v-icon>
                        </v-btn>
                    </v-list-item-action>
                </v-list-item>
            </v-list>
        </v-card-text>
        <v-card-text
            v-else-if="filter"
            class="grow d-flex justify-center align-center grey--text py-5"
        >No project files found</v-card-text>
        <v-card-text
            v-else
            class="grow d-flex justify-center align-center grey--text py-5"
        >Select a project or add some files.</v-card-text>
        <v-divider ></v-divider>
        <v-toolbar v-if="files.length" dense flat class="shrink">
        </v-toolbar>
        <v-toolbar  dense flat class="shrink">
            <v-text-field
              solo
              flat
              hide-details
              label="Filter"
              v-model="filter"
              prepend-inner-icon="mdi-filter-outline"
              class="ml-n3"
            ></v-text-field>
            <v-btn icon v-if="false">
              <v-icon>mdi-eye-settings-outline</v-icon>
            </v-btn>
            <!-- <v-btn icon>
              <v-icon>mdi-download</v-icon>
            </v-btn> -->
            <!-- <v-btn icon @click="load">
              <v-icon>mdi-refresh</v-icon>
            </v-btn> -->
        </v-toolbar>
    </v-card>
</template>

<script>
import FileBrowserConfirmDialog from './FileBrowserConfirmDialog.vue'
import { mapActions, mapGetters } from 'vuex'
import moment from 'moment'

export default {
  props: {
    icons: Object,
    refreshPending: Boolean
  },
  components: {
    FileBrowserConfirmDialog
  },
  data () {
    return {
      items: [],
      filter: ''
    }
  },
  computed: {
    ...mapGetters(['selectedProject', 'projectFiles', 'downloadingFile']),
    files () {
      return this.projectFiles.filter(
        item => item.filename.includes(this.filter)
      )
    }
  },
  methods: {
    ...mapActions(['deleteProjectDocument', 'downloadProjectDocument', 'getProjectFiles']),
    formattedDate (date) {
      return moment(date).format('DD MMM YYYY')
    },
    fileExtension (filename) {
      return filename.split('.').pop().toLowerCase()
    },
    async deleteItem (item) {
      let confirmed = await this.$refs.confirm.open(
        'Delete',
        `Are you sure<br>you want to delete this file?<br><em>${item.filename}</em>`
      )

      if (confirmed && item.project_document_uuid) {
        this.deleteProjectDocument(item.project_document_uuid)
      }
    },
    downloadItem (item) {
      this.downloadProjectDocument({ projectDocumentUUID: item.project_document_uuid, filename: item.filename })
    }
  },
  watch: {
    selectedProject (project) {
      if (project) {
        this.getProjectFiles(project.project_uuid)
      }
    },
    downloadingFile (value) {
      if (!value) {
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.v-card {
    height: 100%;
}
</style>
