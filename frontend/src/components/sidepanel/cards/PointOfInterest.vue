<template>
  <v-container>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
        <v-toolbar-title>
          Point of interest
        </v-toolbar-title>
        {{coordinates}}
      </v-banner>
    </v-toolbar>
    <v-row class="pa-5" v-if="!this.isPointSelected">
      <v-col cols=12 lg=8>
        <p>Select a point on the map.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined>Draw point</v-btn>
      </v-col>
    </v-row>

    <FeatureAnalysis
      v-if="this.isPointSelected && dataMartFeatureInfo"
      :record="dataMartFeatureInfo"/>

  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import FeatureAnalysis from '../../analysis/FeatureAnalysis'

export default {
  name: 'PointOfInterest',
  components: {
    FeatureAnalysis
  },
  data () {
    return {
    }
  },
  watch: {
    dataMartFeatureInfo (value) {
      if (value && value.geometry) {
        // Update router
        console.log('updating POI route')
        this.$router.push({
          path: '/point-of-interest',
          query: { coordinates: value.geometry.coordinates }
        })
      }
    },
    isMapReady (value) {
      if (value) {
        this.loadFeature()
      }
    }
  },
  methods: {
    selectPoint () {
      this.setDrawMode('draw_point')
    },
    loadFeature () {
      // Load Point of Interest feature from query
      if ((!this.dataMartFeatureInfo || !this.dataMartFeatureInfo.geometry) && this.$route.query.coordinates) {
        // load feature from coordinates
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        let data = {
          coordinates: coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    ...mapActions('map', ['setDrawMode'])
  },
  computed: {
    isPointSelected () {
      return this.dataMartFeatureInfo && this.dataMartFeatureInfo.geometry
    },
    coordinates () {
      return this.dataMartFeatureInfo && this.dataMartFeatureInfo.geometry && this.dataMartFeatureInfo.geometry.coordinates.map((x) => {
        return Number(x).toFixed(5)
      }).join(', ')
    },
    ...mapGetters(['dataMartFeatureInfo']),
    ...mapGetters('map', ['isMapReady'])
  },
  mounted () {
    if (this.isMapReady) {
      this.loadFeature()
    }
  },
  beforeDestroy () {
  }
}
</script>

<style>

</style>
