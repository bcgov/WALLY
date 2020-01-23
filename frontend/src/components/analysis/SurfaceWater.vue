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
            hint="Available watersheds at this location"
          ></v-select>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'
import qs from 'querystring'

export default {
  name: 'SurfaceWaterDetails',
  data: () => ({
    selectedWatershed: null,
    assessmentWatershed: null,
    hydrometricWatershed: null,
    watersheds: [],
    geojsonLayersAdded: []
  }),
  computed: {
    watershedOptions () {
      return this.watersheds.map((w, i) => w.properties['GNIS_NAME_1'] || w.properties['SOURCE_NAME'] || `Watershed option ${i + 1}`)
    },
    ...mapGetters(['dataMartFeatureInfo', 'map'])
  },
  methods: {
    addSingleWatershedLayer (id = 'watershedsAtLocation', data, color = '#088', opacity = 0.4) {
      this.map.addLayer({
        id: id,
        type: 'fill',
        source: {
          type: 'geojson',
          data: data
        },
        layout: {},
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
      ApiService.query(`/api/v1/aggregate/stats/watersheds?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          this.watersheds = data.features
          this.addSingleWatershedLayer('watershedsAtLocation', data)
          this.geojsonLayersAdded = ['watershedsAtLocation']
        })
        .catch(e => {
          console.error(e)
        })
    },
    resetGeoJSONLayers () {
      if (this.geojsonLayersAdded.length === 0) {
        return
      }
      console.log(this.geojsonLayersAdded.length)
      for (let i = this.geojsonLayersAdded.length - 1; 1 >= 0; i--) {
        console.log(i)
        const layer = this.geojsonLayersAdded[i]
        if (layer) {
          this.map.removeLayer(layer)
          this.map.removeSource(layer)
          this.geojsonLayersAdded.splice(i, 1)
        }
      }
    },
    createWatersheds () {
      this.fetchWatersheds()
    }
  },
  watch: {
    // dataMartFeatureInfo: {
    //   deep: true,
    //   handler () {
    //     this.createWatersheds()
    //   }
    // }
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
