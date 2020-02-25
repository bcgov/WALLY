<template>
  <v-container class="pa-3 mt-3">
    <v-row v-if="watershedLoading">
      <v-col>
        <v-progress-linear show indeterminate></v-progress-linear>
      </v-col>
    </v-row>
    <template v-if="watersheds && watersheds.length">
      <v-row>
        <v-col cols=12 md=8><div class="title mb-3">Watersheds</div></v-col>
        <v-col cols=12 md=4 class="text-right">
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
        <WatershedDetails :record="selectedWatershedRecord" :watersheds="watersheds" :watershedID="selectedWatershed" ></WatershedDetails>
      </div>
    </template>
  </v-container>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import ApiService from '../../../services/ApiService'
import qs from 'querystring'

import WatershedDetails from './WatershedDetails'

export default {
  name: 'SurfaceWaterDetails',
  components: {
    WatershedDetails
  },
  data: () => ({
    infoTabs: null,
    watershedLoading: false,
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: [],
    includePOIPolygon: false
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
      console.log(data)
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
          })
          this.watershedLoading = false
        })
        .catch(e => {
          console.error(e)
          this.watershedLoading = false
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
