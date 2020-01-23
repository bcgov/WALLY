<template>
  <v-container class="pa-3 mt-3">
    <template v-if="assessmentWatershed">
      <div class="title mb-3">Assessment watershed</div>
      <div class="font-weight-bold mb-3">{{ assessmentWatershedName }}</div>
      <div v-if="assessmentWatershed.properties['AREA_HA']">Area: {{ assessmentWatershed.properties['AREA_HA'].toFixed(1) }} Ha</div>
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
    assessmentWatershed: null,
    hydrometricWatershed: null,
    geojsonLayersAdded: []
  }),
  computed: {
    assessmentWatershedName () {
      if (!this.assessmentWatershed) {
        return null
      }
      return this.assessmentWatershed.properties['GNIS_NAME_1'] || this.assessmentWatershed.properties['WATERSHED_FEATURE_ID']
    },
    ...mapGetters(['dataMartFeatureInfo', 'map'])
  },
  methods: {
    addSingleWatershedLayer (id = 'singleWatershed', data, color = '#088', opacity = 0.4) {
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
    fetchAssessmentWatershed () {
      const params = {
        point: JSON.stringify(this.dataMartFeatureInfo.geometry.coordinates)
      }
      ApiService.query(`/api/v1/aggregate/stats/assessment_watershed?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          if (data && data.features && data.features.length === 1) {
            this.assessmentWatershed = data.features[0]
            this.addSingleWatershedLayer('singleAssessmentWatershed', data.features[0])
            this.geojsonLayersAdded.push('singleAssessmentWatershed')
          }
        })
        .catch(e => {
          console.error(e)
        })
    },
    fetchHydrometricWatershed () {
      const params = {
        point: JSON.stringify(this.dataMartFeatureInfo.geometry.coordinates)
      }
      ApiService.query(`/api/v1/aggregate/stats/hydrometric_watershed?${qs.stringify(params)}`)
        .then(r => {
          const data = r.data
          if (data && data.features && data.features.length === 1) {
            this.hydrometricWatershed = data.features[0]
            this.addSingleWatershedLayer('singleHydrometricWatershed', data.features[0], '#ff5983', 0.3)
            this.geojsonLayersAdded.push('singleHydrometricWatershed')
          }
        })
        .catch(e => {
          console.error(e)
        })
    },
    resetGeoJSONLayers () {
      if (this.geojsonLayersAdded.length === 0) {
        return
      }

      for (let i = this.geojsonLayersAdded.length - 1; 1 >= 0; i--) {
        const layer = this.geojsonLayersAdded[i]
        this.map.removeLayer(layer)
        this.map.removeSource(layer)
        this.geojsonLayersAdded.splice(i, 1)
      }
    },
    createWatersheds () {
      this.resetGeoJSONLayers()
      this.fetchAssessmentWatershed()
      this.fetchHydrometricWatershed()
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
