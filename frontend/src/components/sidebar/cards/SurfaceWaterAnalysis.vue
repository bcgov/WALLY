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
    </v-toolbar>
    <div
    v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name === 'point_of_interest'">
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
import SurfaceWater from '../../analysis/SurfaceWater/SurfaceWater'

export default {
  name: 'SurfaceWaterAnalysis',
  components: {
    SurfaceWater
  },
  data: () => ({
    licencesLayerAutomaticallyEnabled: false,
    hydatLayerAutomaticallyEnabled: false,
    applicationsLayerAutomaticallyEnabled: false
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
    ...mapActions('map', ['setDrawMode'])
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
    ...mapGetters('map', ['isMapLayerActive']),
    ...mapGetters(['dataMartFeatureInfo'])
  },
  mounted () {
    this.selectPoint()
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
  },
  beforeDestroy () {
    // this.setDrawMode('simple_select')
    if (this.hydatLayerAutomaticallyEnabled) {
      this.disableHydatLayer()
    }
    if (this.licencesLayerAutomaticallyEnabled) {
      this.disableLicencesLayer()
    }
    if (this.applicationsLayerAutomaticallyEnabled) {
      this.disableApplicationsLayer()
    }
  }
}
</script>

<style>

</style>
