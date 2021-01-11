<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbs">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <v-toolbar flat>
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-map-marker"
            color="white">
            mdi-map-marker
          </v-icon>
        </v-avatar>
        <v-toolbar-title>
         First Nations Areas Nearby
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
      <FirstNationsAreasNearby
        :record="pointOfInterest"
      />
    </div>
    <v-row class="pa-5" v-else>
      <v-col cols=12 lg=8><p>Select a point of interest to find nearby First Nations Communities, Treaty Areas and Lands.</p></v-col>
      <v-col class="text-right"><v-btn @click="selectPointOfInterest" color="primary" outlined>Draw point</v-btn></v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import FirstNationsAreasNearby from './FirstNationsAreasNearby.vue'

export default {
  name: 'FirstNationsAreasNearbyContainer',
  components: {
    FirstNationsAreasNearby
  },
  data: () => ({
    breadcrumbs: []
  }),
  methods: {
    loadFirstNationsAreasNearby () {
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
        text: 'First Nations Areas Nearby',
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
    ...mapActions('map', ['setDrawMode', 'selectPointOfInterest'])
  },
  computed: {
    ...mapGetters('map', ['draw', 'isMapLayerActive', 'isMapReady']),
    ...mapGetters(['pointOfInterest'])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.loadFirstNationsAreasNearby()
      }
    }
  },
  mounted () {
    this.$store.commit('setInfoPanelVisibility', true)
    this.loadFirstNationsAreasNearby()
  },
  beforeDestroy () {
  }
}
</script>

<style>

</style>
