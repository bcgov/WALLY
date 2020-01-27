<template>
  <div>
    <div class="title my-5">Water Rights Licences</div>
    <div v-if="licenceData">
      <span class="font-weight-bold">Total annual licenced quantity:</span> {{ licenceData.total_qty.toFixed(1) }} m3/year
      <div class="my-5">
        <div class="font-weight-bold mb-3">Annual licenced quantity by use type:</div>
        <v-data-table
          :items="licenceData.total_qty_by_purpose"
          :headers="licencePurposeHeaders"
          sort-by="qty"
          sort-desc
        >
          <template v-slot:item.qty="{ item }">
            {{ item.qty.toFixed(1) }}
          </template>
        </v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'
export default {
  name: 'SurfaceWaterDemand',
  components: {
  },
  props: ['watershedID', 'record'],
  data: () => ({
    licenceData: null,
    licencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Quantity (m3/year)', value: 'qty' }
    ]
  }),
  computed: {
    ...mapGetters(['map'])
  },
  watch: {
    watershedID () {
      this.licenceData = null
      this.map.removeLayer('waterLicences')
      this.map.removeSource('waterLicences')
      this.fetchLicenceData()
    }
  },
  methods: {
    addSingleWatershedLayer (id = 'waterLicences', data, color = '#00e676', opacity = 0.5, max = 100000000) {
      this.map.addLayer({
        id: id,
        type: 'circle',
        source: {
          type: 'geojson',
          data: data
        },
        paint: {
          'circle-color': color,
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['number', ['get', 'qty_m3_yr'], 0],
            0,
            10,
            max,
            max > 1000000 ? 50 : 25
          ],
          'circle-opacity': opacity
        }
      }, 'water_rights_licences')
    },
    fetchLicenceData () {
      ApiService.query(`/api/v1/aggregate/watersheds/${this.watershedID}/licences`)
        .then(r => {
          this.licenceData = r.data
          console.log('adding data to map')
          const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
          this.addSingleWatershedLayer('waterLicences', r.data.licences, '#00e676', 0.5, max)
        })
        .catch(e => {
          console.error(e)
        })
    }
  },
  mounted () {
    this.fetchLicenceData()
  },
  beforeDestroy () {
    this.map.removeLayer('waterLicences')
    this.map.removeSource('waterLicences')
  }
}
</script>

<style>

</style>
