<template>
  <v-container>
    <v-toolbar flat>
      <v-hover v-slot:default="{ hover }">
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
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
        <p>Select a point on the map.</p>
      </v-col>
      <v-col class="text-right">
        <v-btn @click="selectPoint" color="primary" outlined :disabled="buttonClicked">Draw point</v-btn>
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
      hover: false,
      buttonClicked: false
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
      this.buttonClicked = true
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
    ...mapActions(['exitFeature']),
    ...mapActions('map', ['setDrawMode', 'clearSelections'])
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
    ...mapGetters('map', ['isMapReady', 'draw', 'isDrawingToolActive'])
  },
  mounted () {
    console.log('is map ready?', this.isMapReady)
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
