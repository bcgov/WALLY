<template>
    <v-card flat tile min-height="380" class="d-flex flex-column">
        <confirm ref="confirm"></confirm>
        <!-- <v-card-text
            v-if="!path"
            class="grow d-flex justify-center align-center grey--text"
        >Select a folder or a file</v-card-text> -->
        <!-- <v-card-text
            class="grow d-flex justify-center align-center"
        >File: {{ path }}</v-card-text> -->
        <v-card-text v-if="activeFiles.length > 0" class="grow">
            <!-- <v-list subheader v-if="dirs.length">
                <v-subheader>Folders</v-subheader>
                <v-list-item
                    v-for="item in dirs"
                    :key="item.basename"
                    class="pl-0"
                >
                    <v-list-item-avatar class="ma-0">
                        <v-icon>mdi-folder-outline</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content class="py-2">
                        <v-list-item-title v-text="item.basename"></v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action>
                        <v-btn icon @click.stop="deleteItem(item)">
                            <v-icon color="grey lighten-1">mdi-delete-outline</v-icon>
                        </v-btn>
                        <v-btn icon v-if="false">
                            <v-icon color="grey lighten-1">mdi-information</v-icon>
                        </v-btn>
                    </v-list-item-action>
                </v-list-item>
            </v-list> -->
            <!-- <v-divider v-if="dirs.length && files.length"></v-divider> -->
            <v-list subheader v-if="activeFiles">
                <v-subheader>Files</v-subheader>
                <v-list-item
                    v-for="item in activeFiles"
                    :key="item.basename"
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
                        <v-btn icon @click.stop="downloadItem(item)">
                          <v-icon color="grey lighten-1">mdi-download</v-icon>
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
        >No files or folders found</v-card-text>
        <v-card-text
            v-else
            class="grow d-flex justify-center align-center grey--text py-5"
        >The project is empty</v-card-text>
        <v-divider ></v-divider>
        <v-toolbar v-if="activeFiles.length" dense flat class="shrink">
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
            <v-btn icon>
              <v-icon>mdi-download</v-icon>
            </v-btn>
            <!-- <v-btn icon @click="load">
              <v-icon>mdi-refresh</v-icon>
            </v-btn> -->
        </v-toolbar>
    </v-card>
</template>

<script>
// import { formatBytes } from './util'
import Confirm from './Confirm.vue'
import { mapActions, mapGetters } from 'vuex'
import moment from 'moment'

export default {
  props: {
    icons: Object,
    endpoints: Object,
    refreshPending: Boolean
  },
  components: {
    Confirm
  },
  data () {
    return {
      items: [],
      filter: ''
    }
  },
  computed: {
    ...mapGetters(['selectedProjectItem', 'activeFiles'])
  },
  methods: {
    ...mapActions(['deleteProjectDocument', 'downloadProjectDocument']),
    formattedDate (date) {
      return moment(date).format('DD MMM YYYY')
    },
    fileExtension (filename) {
      return filename.split('.').pop().toLowerCase()
    },
    async deleteItem (item) {
      let confirmed = await this.$refs.confirm.open(
        'Delete',
        `Are you sure<br>you want to delete this ${
          item.type === 'dir' ? 'folder' : 'file'
        }?<br><em>${item.basename}</em>`
      )

      if (confirmed && item.project_document_id) {
        this.deleteProjectDocument(item.project_document_id)
        // this.$emit('loading', true)
        // await ApiService.post(config)
        // this.$emit('file-deleted')
        // this.$emit('loading', false)
      }
    },
    downloadItem (item) {
      this.downloadProjectDocument({ projectDocumentId: item.project_document_id, filename: item.filename })
    }
  },
  watch: {
    // async refreshPending () {
    //   if (this.refreshPending) {
    //     await this.load()
    //     this.$emit('refreshed')
    //   }
    // }
  }
}
</script>

<style lang="scss" scoped>
.v-card {
    height: 100%;
}
</style>
