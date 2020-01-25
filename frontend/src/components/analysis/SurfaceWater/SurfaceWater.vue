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
      <div v-if="selectedWatershed">
        <WatershedInputs :watershedID="selectedWatershed" :record="selectedWatershedRecord"/>
        <WatershedDemand :watershedID="selectedWatershed" :record="selectedWatershedRecord"/>
      </div>

    </template>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import mapboxgl from 'mapbox-gl'
import ApiService from '../../../services/ApiService'
import centroid from '@turf/centroid'
import qs from 'querystring'

import WatershedInputs from './WatershedInputs'
import WatershedDemand from './WatershedDemand'

export default {
  name: 'SurfaceWaterDetails',
  components: {
    WatershedInputs,
    WatershedDemand
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
      let popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false
      })

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

      this.map.on('mouseenter', 'places', function (e) {
      // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        let coordinates = centroid(e.features[0].geometry).coordinates.slice()
        let licenceNumber = e.features[0].properties['LICENCE_NUMBER']
        let licenseeName = e.features[0].properties['PRIMARY_LICENSEE_NAME']
        let sourceName = e.features[0].properties['SOURCE_NAME']
        let qty = e.features[0].properties['qty_m3_yr'].toFixed(1)
        let purpose = e.features[0].properties['PURPOSE_USE']

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup
          .setLngLat(coordinates)
          .setHTML(`
            <p></p>
            <p>Licence no.: ${licenceNumber}</p>
            <p>Primary licensee: ${licenseeName}</p>
            <p>Source: ${sourceName}</p>
            <p>${qty} m3/year</p>
            <p>Purpose use: ${purpose}</p>
          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', 'places', function () {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
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
      this.watersheds.forEach((ws, i) => {
        this.map.removeLayer(`ws-${ws.id}`)
        this.map.removeSource(`ws-${ws.id}`)
      })
      this.watersheds = []
      this.geojsonLayersAdded = []
    },
    createWatersheds () {
      this.fetchWatersheds()
    }
  },
  mounted () {
    this.createWatersheds()
  },
  beforeDestroy () {
    this.resetGeoJSONLayers()
  }
}
</script>

<style>

</style>
