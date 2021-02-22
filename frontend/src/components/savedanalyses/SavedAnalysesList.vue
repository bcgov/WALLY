<template>
    <v-card flat tile min-height="250" class="d-flex flex-column">
        <FileBrowserConfirmDialog ref="confirm"></FileBrowserConfirmDialog>
        <v-card-subtitle>Analysis Description: </v-card-subtitle>
        <v-card-text v-if="savedAnalyses.length > 0" class="grow">
            <v-list subheader v-if="savedAnalyses.length > 0">
                <v-subheader>Saved Analyses</v-subheader>
                <v-list-item
                    v-for="item in savedAnalyses"
                    :key="item.saved_analysis_uuid"
                    class="pl-0"
                >
                    <v-list-item-content class="py-2">
                        <v-list-item-title v-text="item.name"></v-list-item-title>
                        <v-list-item-title v-text="item.description"></v-list-item-title>
                        <v-list-item-subtitle>{{ formattedDate(item.create_date) }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-content class="py-2">
                        <v-list-item-title v-text="item.feature_type"></v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action>
                        <v-btn
                          icon
                          @click.stop="runAnalysis(item)"
                        >
                          <v-icon>mdi-refresh</v-icon>
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
        >No save analyses found</v-card-text>
        <v-card-text
            v-else
            class="grow d-flex justify-center align-center grey--text py-5"
        >Create your first saved analysis by performing an analysis from one of WALLY's features.</v-card-text>
        <v-divider ></v-divider>
        <v-toolbar v-if="savedAnalyses.length" dense flat class="shrink">
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
import { mapActions, mapGetters } from 'vuex'
import FileBrowserConfirmDialog from '../filebrowser/FileBrowserConfirmDialog.vue'
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
    ...mapGetters(['savedAnalyses']),
    ...mapGetters('map', ['map', 'isMapReady'])
    // analyses () {
    //   return this.savedAnalyses.filter(
    //     item => item.name.includes(this.filter)
    //   )
    // }
  },
  methods: {
    ...mapActions(['getSavedAnalyses', 'deleteSavedAnalysis', 'runSavedAnalysis']),
    formattedDate (date) {
      return moment(date).format('DD MMM YYYY')
    },
    async deleteItem (item) {
      let confirmed = await this.$refs.confirm.open(
        'Delete',
        `Are you sure<br>you want to delete this analysis?<br><em>${item.name}</em>`
      )
      if (confirmed && item.saved_analysis_uuid) {
        this.deleteSavedAnalysis(item.saved_analysis_uuid)
      }
    },
    runAnalysis (item) {
      console.log(item)
      console.log(this.$route.query)
      this.map.fitBounds(item.map_bounds)
      let coordinates = item.geometry.coordinates
      this.$router.push({
        path: item.feature_type,
        query: {
          'section_line_A': coordinates[0],
          'section_line_B': coordinates[1]
        }
      })
      // this.runSavedAnalysis(item)
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.getSavedAnalyses()
      }
    }
  },
  created () {
    this.getSavedAnalyses()
  }
}
</script>

<style lang="scss" scoped>
.v-card {
    height: 100%;
}
</style>
