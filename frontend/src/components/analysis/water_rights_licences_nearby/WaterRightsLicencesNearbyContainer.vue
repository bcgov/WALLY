<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
         Water Rights Licences Nearby
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
      v-if="pointOfInterest &&
            pointOfInterest.display_data_name === 'point_of_interest'">
      <div class="pa-3 mt-3">
        Point at {{ pointOfInterest.geometry.coordinates.map(x => x.toFixed(6)).join(', ') }}
      </div>
      <WaterRightsLicencesNearby
        :record="pointOfInterest"
      />
    </div>
    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8><p>Select a point of interest to find nearby water rights licences.</p></v-col>
      <v-col class="text-right"><v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import WaterRightsLicencesNearby from './WaterRightsLicencesNearby.vue'

export default {
  name: 'WaterRightsLicencesNearbyContainer',
  components: {
    WaterRightsLicencesNearby
  },
  data: () => ({
    licencesLayerAutomaticallyEnabled: false,
    breadcrumbs: []
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    enableLicencesLayer () {
      this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
    },
    disableLicencesLayer () {
      this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
    },
    loadWaterRightsLicencesNearby () {
      if (!this.isWaterRightsLicencesLayerEnabled) {
        this.licencesLayerAutomaticallyEnabled = true
        this.enableLicencesLayer()
      }
      this.setBreadcrumbs()
      this.loadFeature()
    },
    setBreadcrumbs () {
      this.breadcrumbs = [{
        text: 'Home',
        disabled: false,
        to: { path: '/' }
      },
      {
        text: 'Point of Interest',
        disabled: false,
        to: {
          path: '/point-of-interest',
          query: { coordinates: this.$route.query.coordinates }
        }
      }, {
        text: 'Water Rights Licences Nearby',
        disabled: true
      }]
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
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    isWaterRightsLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.loadWaterRightsLicencesNearby()
      }
    }
  },
  mounted () {
    this.$store.commit('setInfoPanelVisibility', true)
    this.loadWaterRightsLicencesNearby()
  },
  beforeDestroy () {
    if (this.licencesLayerAutomaticallyEnabled) {
      this.disableLicencesLayer()
    }
  }
}
</script>

<style>

</style>
