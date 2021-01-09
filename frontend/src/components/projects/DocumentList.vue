<template>
  <v-list subheader v-if="files.length">
    <v-subheader>Files</v-subheader>
    <v-list-item
      v-for="item in documentsData"
      :key="item.project_document_id"
      class="pl-0"
    >
      <v-list-item-avatar class="ma-0">

      </v-list-item-avatar>

      <v-list-item-content class="py-2">
        <v-list-item-title v-text="item.filename"></v-list-item-title>
        <v-list-item-subtitle>{{
          'test'
        }}</v-list-item-subtitle>
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
  </v-list>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import moment from 'moment'

export default {
  name: 'Projects',
  components: {},
  props: {
    project_id: Number
  },
  data: () => ({
    loading: false,
    files: []
  }),
  computed: {
    ...mapGetters('map', ['map'])
  },
  methods: {
    ...mapGetters('map', ['isMapReady']),
    fetchDocumentsData () {
      this.loading = true
      moment()
      ApiService.query(`/api/v1/projects/${this.project_id}/documents/`)
        .then((r) => {
          console.log(r.data)
          this.files = r.data
          this.loading = false
        })
        .catch((e) => {
          this.loading = false
          console.error(e)
        })
    },
    formatDate (date) {
      return moment(date).format('MMM DD YYYY')
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.fetchDocumentsData()
      }
    }
  },
  mounted () {
    this.fetchDocumentsData()
    if (this.isMapReady()) {
    }
  },
  beforeDestroy () {}
}
</script>
