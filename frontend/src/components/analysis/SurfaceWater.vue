<template>
  <v-container class="pa-3 mt-3">
    <template v-if="watersheds && watersheds.length">
      <div class="title mb-3">Watersheds</div>
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
      <WatershedDetails v-if="selectedWatershed" :watershedID="selectedWatershed" :record="selectedWatershedRecord"/>
    </template>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import qs from 'querystring'

import WatershedDetails from './WatershedDetails'

export default {
  name: 'SurfaceWaterDetails',
  components: {
    WatershedDetails
  },
  data: () => ({
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: []
  }),
  watch: {
    selectedWatershed (v) {
      this.filterWatershed(v)
    }
  },
  computed: {
    selectedWatershedRecord () {
      if (!this.selectedWatershed || this.watersheds) {
        return null
      }
      return this.watersheds.find((ws) => ws.id === this.selectedWatershed)
    },
    watershedOptions () {
      return this.watersheds.map((w, i) => ({
        label: w.properties['GNIS_NAME_1'] || w.properties['SOURCE_NAME'] || `Watershed ${i + 1}`,
        value: w.id
      }))
    },
    ...mapGetters(['dataMartFeatureInfo', 'map'])
  },
  methods: {
    filterWatershed (id) {
      this.geojsonLayersAdded.forEach((layerID) => {
        this.map.setLayoutProperty(
          layerID,
          'visibility',
          layerID.indexOf(`ws-${id}`) > -1 ? 'visible' : 'none'
        )
      })
    },
    addSingleWatershedLayer (id = 'watershedsAtLocation', data, color = '#088', opacity = 0.4) {
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
      })
    },
    fetchWatersheds () {
      const params = {
        point: JSON.stringify(this.dataMartFeatureInfo.geometry.coordinates)
      }
      ApiService.query(`/api/v1/aggregate/watersheds?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          this.watersheds = data.features
          this.watersheds.forEach((ws, i) => {
            this.addSingleWatershedLayer(`ws-${ws.id}`, ws)
            this.geojsonLayersAdded.push(`ws-${ws.id}`)
          })
        })
        .catch(e => {
          console.error(e)
        })
    },
    resetGeoJSONLayers () {
      this.watersheds.forEach((wsId, i) => {
        this.map.removeLayer(`ws-${wsId}`)
        this.map.removeSource(`ws-${wsId}`)
      })
      this.watersheds = []
    },
    createWatersheds () {
      this.fetchWatersheds()
    }
  },
  mounted () {
    this.createWatersheds()
  },
  beforeDestroy () {
  }
}
</script>

<style>

</style>
