<template>
  <v-container>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-chart-bar"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Analyze surface water availability
        </v-toolbar-title>
      </v-banner>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" v-on:click="exitFeature">
            <v-icon>close</v-icon>
          </v-btn>
        </template>
        <span>Exit</span>
      </v-tooltip>
    </v-toolbar>
    <div
    v-if="pointOfInterest && pointOfInterest.display_data_name === 'point_of_interest'">
      <div>
          <v-expansion-panels>
            <v-expansion-panel>
              <v-expansion-panel-header>
                Instructions, Methodology, and Data Sources
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-card flat>
                  <v-card-text>
                    <SurfaceWaterInstructions></SurfaceWaterInstructions>
                  </v-card-text>
                </v-card>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
      </div>
      <SurfaceWaterV2 v-if="this.app.config && this.app.config.surface_water_design_v2"></SurfaceWaterV2>
    </div>
    <div v-else>
      <v-row class="mt-3">
        <v-col cols=12 lg=8>
          <p class="pl-3">Select a point of interest to determine water availability.</p>
        </v-col>
        <v-col class="text-right">
          <v-btn @click="selectPointOfInterest" color="primary" outlined>Select a point</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card>
            <v-card-title>Instructions, Methodology, and Data Sources</v-card-title>
            <v-card-text>
              <SurfaceWaterInstructions></SurfaceWaterInstructions>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import SurfaceWaterV2 from './SurfaceWaterV2'
import SurfaceWaterInstructions from './SurfaceWaterInstructions'

export default {
  name: 'SurfaceWaterContainer',
  components: {
    SurfaceWaterV2,
    SurfaceWaterInstructions
  },
  data: () => ({
    licencesLayerAutomaticallyEnabled: false,
    hydatLayerAutomaticallyEnabled: false,
    applicationsLayerAutomaticallyEnabled: false,
    fishLayerAutomaticallyEnabled: false,
    approvalLayerAutomaticallyEnabled: false
  }),
  methods: {
    enableApplicationsLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_rights_applications')
    },
    disableApplicationsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_rights_applications')
    },
    enableLicencesLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
    },
    disableLicencesLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
    },
    enableHydatLayer () {
      this.$store.dispatch('map/addMapLayer', 'hydrometric_stream_flow')
    },
    disableHydatLayer () {
      this.$store.dispatch('map/removeMapLayer', 'hydrometric_stream_flow')
    },
    enableFishLayer () {
      this.$store.dispatch('map/addMapLayer', 'fish_observations')
    },
    disableFishLayer () {
      this.$store.dispatch('map/removeMapLayer', 'fish_observations')
    },
    enableApprovalsLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_approval_points')
    },
    disableApprovalsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_approval_points')
    },
    loadSurfaceWaterAnalysis () {
      if (!this.isHydatLayerEnabled) {
        this.hydatLayerAutomaticallyEnabled = true
        this.enableHydatLayer()
      }
      if (!this.isApplicationsLayerEnabled) {
        this.applicationsLayerAutomaticallyEnabled = true
        this.enableApplicationsLayer()
      }
      if (!this.isLicencesLayerEnabled) {
        this.licencesLayerAutomaticallyEnabled = true
        this.enableLicencesLayer()
      }
      if (!this.isFishLayerEnabled) {
        this.fishLayerAutomaticallyEnabled = true
        this.enableFishLayer()
      }
      if (!this.isApprovalsLayerEnabled) {
        this.approvalLayerAutomaticallyEnabled = true
        this.enableApprovalsLayer()
      }
      this.loadFeature()
    },
    loadFeature () {
      if ((!this.pointOfInterest || !this.pointOfInterest.geometry) && this.$route.query.coordinates) {
        // load feature from coordinates
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        let data = {
          coordinates: coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'selectPointOfInterest']),
    ...mapActions(['exitFeature'])
  },
  computed: {
    isLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    isApplicationsLayerEnabled () {
      return this.isMapLayerActive('water_rights_applications')
    },
    isHydatLayerEnabled () {
      return this.isMapLayerActive('hydrometric_stream_flow')
    },
    isFishLayerEnabled () {
      return this.isMapLayerActive('fish_observations')
    },
    isApprovalsLayerEnabled () {
      return this.isMapLayerActive('water_approval_points')
    },
    ...mapGetters('map', ['isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest', 'app'])
  },
  watch: {
    pointOfInterest (value) {
      if (value && value.geometry) {
        // Update router
        global.config.debug && console.log('[wally] updating POI route')
        this.$router.push({
          query: { ...this.$route.query, coordinates: value.geometry.coordinates }
        })
      }
    },
    isMapReady (value) {
      if (value) {
        this.clearSelections()
        this.loadSurfaceWaterAnalysis()
      }
    }
  },
  mounted () {
    this.loadSurfaceWaterAnalysis()
  },
  beforeDestroy () {
    if (this.hydatLayerAutomaticallyEnabled) {
      this.disableHydatLayer()
    }
    if (this.licencesLayerAutomaticallyEnabled) {
      this.disableLicencesLayer()
    }
    if (this.applicationsLayerAutomaticallyEnabled) {
      this.disableApplicationsLayer()
    }
    if (this.fishLayerAutomaticallyEnabled) {
      this.disableFishLayer()
    }
    if (this.approvalLayerAutomaticallyEnabled) {
      this.disableApprovalsLayer()
    }
  }
}
</script>

<style>

</style>
