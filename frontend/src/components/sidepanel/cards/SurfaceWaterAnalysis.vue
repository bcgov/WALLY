<template>
  <v-container class="pt-5">
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-vector-line"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Surface water
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
      <SurfaceWater></SurfaceWater>
    </div>
    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8>
        <p>Select a point of interest.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined>Select point</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import SurfaceWater from '../../analysis/surface_water/SurfaceWater'

export default {
  name: 'SurfaceWaterAnalysis',
  components: {
    SurfaceWater
  },
  data: () => ({
    licencesLayerAutomaticallyEnabled: false,
    hydatLayerAutomaticallyEnabled: false,
    applicationsLayerAutomaticallyEnabled: false,
    fishLayerAutomaticallyEnabled: false,
    approvalLayerAutomaticallyEnabled: false
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
    },
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
    ...mapActions('map', ['setDrawMode', 'clearSelections']),
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
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    pointOfInterest (value) {
      if (value && value.geometry) {
        // Update router
        global.config.debug && console.log('[wally] updating POI route')
        this.$router.push({
          path: '/surface-water',
          query: { coordinates: value.geometry.coordinates }
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
