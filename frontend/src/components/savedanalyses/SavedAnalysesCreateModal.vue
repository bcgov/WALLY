<template>
  <v-dialog v-model="dialog" width="650" v-if="app.config && app.config.saved_analysis">
    <template v-slot:activator="{ on, attrs }">
        <v-btn
          outlined
          color="primary"
          v-bind="attrs"
          v-on="on"
          class='mx-2 p-3'
        >
          <v-icon class='mr-1'>mdi-folder-plus-outline</v-icon>
          Save Analysis
        </v-btn>
    </template>
    <v-card shaped>
      <v-card-title class="headline grey lighten-3" primary-title>
          Save Analysis
      </v-card-title>
      <v-alert
        v-if="success"
        dense
        text
        type="success"
        class="mt-2"
      >
        Saved analysis created <strong>successfully!</strong>
        </v-alert>
      <v-card-text class="mt-4">
        <v-row>
          <v-col cols="12" md="12" align-self="center">
            <v-text-field
              label="Save Analysis Name"
              placeholder="Enter a name for this saved analysis"
              v-model="name"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-text-field
              label="Save Analysis Description"
              placeholder="Enter a description of the analysis"
              v-model="description"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          outlined
          @click="createSavedAnalysis"
          color="primary"
          :disabled="loading"
        >
          <div v-if="!loading">
            Save
          </div>
          <v-progress-circular
            v-if="loading"
            indeterminate
            size=24
            class="ml-1"
            color="primary"
          ></v-progress-circular>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
export default {
  name: 'SavedAnalysesCreateModal',
  props: {
    geometry: {},
    featureType: String
  },
  data: () => ({
    loading: false,
    dialog: false,
    success: false,
    name: '',
    description: ''
  }),
  computed: {
    ...mapGetters('map', ['map', 'activeMapLayers']),
    ...mapGetters(['app'])
  },
  methods: {
    ...mapActions(['getSavedAnalyses']),
    createSavedAnalysis () {
      if (this.name.length < 3) {
        // TODO add user notify that at least 3 characters
        // are needed for a analysis name
        return
      }
      this.loading = true
      const bounds = this.map.getBounds()
      const ne = bounds._ne
      const sw = bounds._sw
      const mapBounds = [[ne.lng, ne.lat], [sw.lng, sw.lat]]
      const zoom = this.map.getZoom()

      const params = {
        name: this.name,
        description: this.description,
        geometry: this.geometry,
        feature_type: this.featureType,
        map_layers: this.activeMapLayers.map((l) => {
          return { map_layer: l.display_data_name }
        }),
        map_bounds: mapBounds,
        zoom_level: zoom
      }

      console.log(params)

      ApiService.post(`/api/v1/saved_analyses`, params)
        .then((res) => {
          this.name = ''
          this.description = ''
          this.loading = false
          this.success = true
          this.getSavedAnalyses()
        })
        .catch((error) => {
          this.loading = false
          this.success = false
          console.error(error)
        })
        .finally((res) => {
          setTimeout(() => {
            this.dialog = false
            this.success = false
          }, 2000)
        })
    }
  }
}
</script>

<style>
</style>
