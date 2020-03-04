<template>
  <v-container class="pa-3 mt-3">
    <v-row v-if="watershedLoading">
      <v-col>
        <v-progress-linear show indeterminate></v-progress-linear>
      </v-col>
    </v-row>
    <v-banner one-line>
      <v-avatar
        slot="icon"
        color="blue accent-4"
        size="40"
      >
        <v-icon
          icon="mdi-exclamation"
          color="white"
        >
          mdi-exclamation
        </v-icon>
      </v-avatar>

      This modelling output has not been peer reviewed and is still considered experimental. Use the values generated with your own discretion.

    </v-banner>
    <template v-if="watersheds && watersheds.length">
      <v-row>
        <!-- <v-col cols=12 md=8><div class="title mb-3">Watersheds</div></v-col> -->
        <v-col cols=12 md=12 class="text-right">
          <v-btn outlined color="primary" @click="resetWatershed">Reset</v-btn>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col cols=12 md=6>Select watershed:</v-col>
        <v-col cols=12 md=6>
          <v-select
            v-model="selectedWatershed"
            :items="watershedOptions"
            :menu-props="{ maxHeight: '400' }"
            label="Select"
            item-text="label"
            item-value="value"
            hint="Available watersheds at this location"
          ></v-select>
        </v-col>
      </v-row>
      <v-row no-gutters class="pa-0 ma-0" v-if="selectedWatershed.startsWith('generated')">
        <v-col>
          <v-checkbox v-model="includePOIPolygon" label="Include area around point (estimated catchment areas only)"></v-checkbox>
        </v-col>
      </v-row>

      <div v-if="selectedWatershed">
        <!-- <WatershedDetails :record="selectedWatershedRecord" :watersheds="watersheds" :watershedID="selectedWatershed" ></WatershedDetails> -->
        <div v-if="watershedDetailsLoading">
          <v-progress-linear indeterminate show></v-progress-linear>
        </div>
        <div v-else>
          <div>Watershed Details</div>
          <div>
            <MeanAnnualRunoff ref="anchor-mar" :watershedID="selectedWatershed" :record="selectedWatershedRecord" :allWatersheds="watersheds" :details="watershedDetails"/>
            <WatershedAvailability ref="anchor-availability" :watershedID="selectedWatershed" :allWatersheds="watersheds" :record="selectedWatershedRecord" :details="watershedDetails"/>
          </div>
        </div>

      </div>
    </template>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'
import WatershedAvailability from './WatershedAvailability'
import MeanAnnualRunoff from './MeanAnnualRunoff'
// import WatershedDetails from './WatershedDetails'

export default {
  name: 'SurfaceWaterDetails',
  components: {
    WatershedAvailability,
    MeanAnnualRunoff
  },
  data: () => ({
    infoTabs: null,
    watershedLoading: false,
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: [],
    includePOIPolygon: false,
    watershedDetails: null,
    watershedDetailsLoading: false
  }),
  watch: {
    selectedWatershed (v) {
      this.filterWatershed(v)
    },
    includePOIPolygon () {
      this.recalculateWatershed()
    }
  },
  computed: {
    selectedWatershedRecord () {
      if (!this.selectedWatershed || !this.watersheds) {
        return null
      }
      return this.watersheds.find((ws) => ws.id === this.selectedWatershed)
    },
    watershedOptions () {
      return this.watersheds.map((w, i) => ({
        label: w.properties['GNIS_NAME_1'] || w.properties['SOURCE_NAME'] || w.properties['name'] || `Watershed ${i + 1}`,
        value: w.id
      }))
    },
    ...mapGetters(['pointOfInterest']),
    ...mapGetters('map', ['map'])
  },
  methods: {
    resetWatershed () {
      this.$store.dispatch('map/clearSelections')
    },
    filterWatershed (id) {
      this.geojsonLayersAdded.forEach((layerID) => {
        this.map.setLayoutProperty(
          layerID,
          'visibility',
          layerID.indexOf(`ws-${id}`) > -1 ? 'visible' : 'none'
        )
      })
    },
    addSingleWatershedLayer (id = 'watershedsAtLocation', data, color = '#088', opacity = 0.3) {
      this.map.addLayer({
        id: id,
        type: 'fill',
        source: {
          type: 'geojson',
          data: data
        },
        layout: {
          visibility: 'none'
        },
        paint: {
          'fill-color': color,
          'fill-outline-color': '#003366',
          'fill-opacity': opacity
        }
      }, 'water_rights_licences')
    },
    fetchWatersheds () {
      this.watershedLoading = true
      const params = {
        point: JSON.stringify(this.pointOfInterest.geometry.coordinates),
        include_self: this.includePOIPolygon
      }
      ApiService.query(`/api/v1/watersheds/?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          this.watersheds = data.features
          this.watersheds.forEach((ws, i) => {
            if (i === 0) this.selectedWatershed = ws.id
            this.addSingleWatershedLayer(`ws-${ws.id}`, ws)
            this.geojsonLayersAdded.push(`ws-${ws.id}`)
            this.fetchWatershedDetails()
          })
          this.watershedLoading = false
        })
        .catch(e => {
          console.error(e)
          this.watershedLoading = false
        })
    },
    fetchWatershedDetails () {
      this.watershedDetailsLoading = true
      this.watershedDetails = null
      ApiService.query(`/api/v1/watersheds/${this.selectedWatershed}`)
        .then(r => {
          this.watershedDetailsLoading = false
          if (!r.data) {
            return
          }
          this.watershedDetails = r.data
        })
        .catch(e => {
          this.watershedDetailsLoading = false
          console.error(e)
        })
    },
    resetGeoJSONLayers () {
      this.watersheds.forEach((ws, i) => {
        this.map.removeLayer(`ws-${ws.id}`)
        this.map.removeSource(`ws-${ws.id}`)
      })
      this.watersheds = []
      this.geojsonLayersAdded = []
      this.selectedWatershed = null
    },
    recalculateWatershed () {
      this.resetGeoJSONLayers()
      this.fetchWatersheds()
    },
    ...mapMutations('map', [
      'setMode'
    ])
  },
  mounted () {
    this.setMode({ type: 'analyze', name: 'surface_water' })
    this.fetchWatersheds()
  },
  beforeDestroy () {
    this.resetGeoJSONLayers()
    this.setMode({ type: 'interactive', name: '' })
  }
}
</script>

<style>

</style>
