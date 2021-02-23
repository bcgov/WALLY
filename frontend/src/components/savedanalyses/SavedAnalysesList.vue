<template>
    <v-card flat tile min-height="250" class="d-flex flex-column">
        <FileBrowserConfirmDialog ref="confirm"></FileBrowserConfirmDialog>
        <v-card-text v-if="savedAnalyses.length > 0" class="grow">
            <v-card-title class="my-3">My Saved Analyses</v-card-title>
            <v-data-table
              id="saved-analysis-table"
              :headers="headers"
              :items-per-page="10"
              item-key="saved_analysis_uuid"
              :items="savedAnalyses">
              <template v-slot:item="{ item }">
                <tr>
                  <td class="text-left v-data-table__divider"><span>{{item.name}}</span></td>
                  <td class="text-center v-data-table__divider"><span>{{formattedDate(item.create_date)}}</span></td>
                  <td class="text-center v-data-table__divider"><span>{{item.description}}</span></td>
                  <td class="text-right v-data-table__divider"><span>{{featureNames[item.feature_type]}}</span></td>
                  <td class="text-center"><v-icon medium @click="deleteItem(item)">mdi-delete-outline</v-icon></td>
                  <td class="text-center"><v-icon medium @click="editItem(item)">mdi-edit-outline</v-icon></td>
                  <td class="text-center"><v-icon medium @click="runAnalysis(item)">mdi-application-import</v-icon></td>
                </tr>
              </template>
            </v-data-table>
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
        </v-toolbar>
    </v-card>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
import FileBrowserConfirmDialog from '../filebrowser/FileBrowserConfirmDialog.vue'
import qs from 'querystring'
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
      filter: '',
      featureNames: {
        'section': 'Cross Section',
        'upstream-downstream': 'Upstream Downstream',
        'surface-water': 'Surface Water',
        'assign-demand': 'Hydraulic Connectivity'
      },
      headers: [
        { text: 'Name', value: 'name', align: 'start', divider: true },
        { text: 'Created', value: 'create_date', align: 'center', divider: true },
        { text: 'Description', value: 'description', align: 'center', divider: true },
        { text: 'Feature type', value: 'feature_type', align: 'end', divider: true },
        { text: 'Run', value: 'action', align: 'center', sortable: false },
        { text: 'Delete', value: 'action', align: 'center', sortable: false }
      ]
    }
  },
  computed: {
    ...mapGetters(['savedAnalyses', 'pointOfInterest']),
    ...mapGetters('map', ['map', 'isMapReady', 'selectPointOfInterest']),
    ...mapMutations(['setPointOfInterest', 'resetPointOfInterest'])
    // analyses () {
    //   return this.savedAnalyses.filter(
    //     item => item.name.includes(this.filter)
    //   )
    // }
  },
  methods: {
    ...mapActions(['getSavedAnalyses', 'deleteSavedAnalysis', 'runSavedAnalysis']),
    ...mapActions('map', ['addFeaturePOIFromCoordinates']),
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
    async editItem (item) {
      let confirmed = await this.$refs.confirm.open(
        'Edit',
        `Are you sure<br>you want to delete this analysis?<br><em>${item.name}</em>`
      )
      if (confirmed && item.saved_analysis_uuid) {
        this.editSavedAnalysis(item.saved_analysis_uuid)
      }
    },
    runAnalysis (item) {
      this.map.fitBounds(item.map_bounds)
      let coordinates = item.geometry.coordinates
      const featureType = item.feature_type
      let params = {
        coordinates: coordinates[0]
      }
      // params for feature types: section
      if (featureType === 'section') {
        params = {
          section_line_A: coordinates[0],
          section_line_B: coordinates[1]
        }
      }
      // push to the saved analysis route
      this.$router.push({
        path: item.feature_type + '?' + qs.stringify(params)
      })
      // Update the selected Point of Interest in the store
      const data = {
        coordinates: coordinates[0],
        layerName: 'point-of-interest'
      }
      this.addFeaturePOIFromCoordinates(data)
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
