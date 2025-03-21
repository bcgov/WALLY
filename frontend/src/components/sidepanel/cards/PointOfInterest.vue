<template>
  <v-container class="pt-3">
    <v-toolbar flat>
      <v-hover v-slot:default="{ hover }">
      <v-banner width="100%">
        <v-avatar slot="icon" color="indigo">
          <v-icon
            icon="mdi-map-marker"
            color="white">
            mdi-map-marker
          </v-icon>
        </v-avatar>
        <v-toolbar-title>
          Point of interest
        </v-toolbar-title>
        <span class="subtitle-1 mr-2">{{coordinates}}</span>
        <v-tooltip bottom >
            <template v-slot:activator="{ on }" >
              <v-btn x-small v-on="on" v-on:click="clearSelections" v-show="isPointSelected && hover"
              color="red darken-4" outlined>
                <v-icon small light>mdi-trash-can-outline</v-icon> Clear
              </v-btn>
            </template>
            <span>Clear Point of Interest</span>
          </v-tooltip>
        </v-banner>
      </v-hover>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" v-on:click="exitFeature">
            <v-icon>close</v-icon>
          </v-btn>
        </template>
        <span>Exit</span>
      </v-tooltip>
    </v-toolbar>
    <v-row class="pa-5" v-if="!this.isPointSelected">
      <v-col cols=12 lg=8>
        <p>Zoom into an area of interest on the map and place a point. The search radius defaults to 1000 m and can be updated after you’ve made your selection.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPointOfInterest" color="primary" outlined>Draw point</v-btn>
      </v-col>
    </v-row>

    <FeatureAnalysis v-if="this.isPointSelected && pointOfInterest" />

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
      hover: false
    }
  },
  watch: {
    pointOfInterest (value) {
      if (value && value.geometry) {
        // Update router
        global.config.debug && console.log('[wally] updating POI route')
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
    loadFeature () {
      // Load Point of Interest feature from query
      if ((!this.pointOfInterest || !this.pointOfInterest.geometry) && this.$route.query.coordinates) {
        // load feature from coordinates
        const coordinates = this.$route.query.coordinates.map((x) => Number(x))

        const data = {
          coordinates,
          layerName: 'point-of-interest'
        }

        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      }
    },
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections', 'selectPointOfInterest'])
  },
  computed: {
    isPointSelected () {
      return this.pointOfInterest && this.pointOfInterest.geometry
    },
    coordinates () {
      return this.pointOfInterest && this.pointOfInterest.geometry && this.pointOfInterest.geometry.coordinates.map((x) => {
        return Number(x).toFixed(5)
      }).join(', ')
    },
    ...mapGetters(['pointOfInterest']),
    ...mapGetters('map', ['isMapReady', 'draw', 'isDrawingToolActive'])
  },
  mounted () {
    global.config.debug && console.log('[wally] is map ready?', this.isMapReady)
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
