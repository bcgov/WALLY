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
         Wells Nearby
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
      <WellsNearby
        :record="pointOfInterest"
      />
    </div>
    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8><p>Select a point of interest (e.g. a proposed well site) to find nearby wells.</p></v-col>
      <v-col class="text-right"><v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import WellsNearby from './WellsNearby.vue'

export default {
  name: 'WellsNearbyContainer',
  components: {
    WellsNearby
  },
  data: () => ({
    gwellsLayerAutomaticallyEnabled: false,
    breadcrumbs: []
  }),
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    enableGWellsLayer () {
      this.$store.dispatch('map/addMapLayer', 'groundwater_wells')
    },
    disableGWellsLayer () {
      this.$store.dispatch('map/removeMapLayer', 'groundwater_wells')
    },
    loadWellsNearby () {
      if (!this.isGwellsLayerEnabled) {
        this.gwellsLayerAutomaticallyEnabled = true
        this.enableGWellsLayer()
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
        text: 'Wells Nearby',
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
    isGwellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.loadWellsNearby()
      }
    }
  },
  mounted () {
    this.$store.commit('setInfoPanelVisibility', true)
    this.loadWellsNearby()
  },
  beforeDestroy () {
    if (this.gwellsLayerAutomaticallyEnabled) {
      this.disableGWellsLayer()
    }
  }
}
</script>

<style>

</style>
