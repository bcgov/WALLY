<template>
  <div>
    <div class="titleSub my-5">Watershed Licenced Quantity</div>
    <div v-if="licencesLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="licenceData">
      <v-card flat>
        <v-card-title class="pl-0">
          Water Rights Licences
          <v-card-actions>
            <v-btn x-small fab depressed light @click="openEditAllocationTableDialog">
              <v-icon small color="primary">
                mdi-tune
              </v-icon>
            </v-btn>
          </v-card-actions>
        </v-card-title>
        <v-dialog v-model="show.editingAllocationValues" persistent>
          <MonthlyAllocationTable
            :allocation-items="licenceData.total_qty_by_purpose"
            key-field="purpose"
            @close="closeEditAllocationTableDialog"/>
        </v-dialog>

        <span>Total annual licenced quantity:</span> {{ licenceData.total_qty.toFixed(1) | formatNumber }} m3/year

        <Dialog v-bind="wmd.availabilityVsDemand"/>

        <div class="my-5">
          <div class="mb-3">Annual licenced quantity by use type:</div>
          <v-data-table
            :items="licenceData.total_qty_by_purpose"
            :headers="licencePurposeHeaders"
            sort-by="qty"
            sort-desc
          >
            <template v-slot:item.qty="{ item }">
              {{ item.qty.toFixed(1) | formatNumber }}
            </template>
          </v-data-table>
        </div>

        <Plotly v-if="availability && licenceData"
                :layout="demandAvailabilityLayout()"
                :data="demandAvailabilityData"
        ></Plotly>

      </v-card>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ApiService from '../../../services/ApiService'
import mapboxgl from 'mapbox-gl'
import { Plotly } from 'vue-plotly'
import Dialog from '../../common/Dialog'
import { WatershedModelDescriptions } from '../../../constants/descriptions'

import surfaceWaterMixin from './mixins'
import MonthlyAllocationTable from './watershed_demand/MonthlyAllocationTable.vue'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'WatershedDemand',
  mixins: [surfaceWaterMixin],
  components: {
    MonthlyAllocationTable,
    Plotly,
    Dialog
  },
  props: ['watershedID', 'record', 'availability'],
  data: () => ({
    licencesLoading: false,
    licenceData: null,
    licencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Quantity (m3/year)', value: 'qty', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      editingAllocationValues: false
    },
    purposeTypes: [],
    months: { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 },
    monthHeaders: [
      { text: 'Jan', value: 'm1' },
      { text: 'Feb', value: 'm2' },
      { text: 'Mar', value: 'm3' },
      { text: 'Apr', value: 'm4' },
      { text: 'May', value: 'm5' },
      { text: 'Jun', value: 'm6' },
      { text: 'Jul', value: 'm7' },
      { text: 'Aug', value: 'm8' },
      { text: 'Sep', value: 'm9' },
      { text: 'Oct', value: 'm10' },
      { text: 'Nov', value: 'm11' },
      { text: 'Dec', value: 'm12' }
    ],
    demandAvailabilityData: [],
    wmd: WatershedModelDescriptions
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['allocationValues'])

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
    ...mapActions('surfaceWater', ['loadAllocationItemsFromStorage', 'initAllocationItemIfNotExists']),
    demandAvailabilityLayout () {
      return {
        barmode: 'stack',
        title: 'Availability vs Licenced Quantity',
        xaxis: {
          tickformat: '%B'
        },
        yaxis: {
          title: 'Volume (m^3)'
        }
      }
    },
    addLicencesLayer (id = 'waterLicences', data, color = '#00e676', opacity = 0.5, max = 100000000) {
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

      this.map.on('mouseenter', id, (e) => {
      // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        let coordinates = e.features[0].geometry.coordinates.slice()
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
            <dl>
              <dt>Licence no.:</dt> <dd>${licenceNumber}</dd>
              <dt>Primary licensee:</dt> <dd>${licenseeName}</dd>
              <dt>Source:</dt> <dd>${sourceName}</dd>
              <dt>Quantity:</dt> <dd>${qty} m3/year</dd>
              <dt>Purpose use:</dt> <dd>${purpose}</dd>
            </dl>

          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', id, () => {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
      })
    },
    openEditAllocationTableDialog () {
      this.show.editingAllocationValues = true
    },
    closeEditAllocationTableDialog () {
      // TODO: Distribute quantity based on alloc values
      this.setDemandAvailabilityData()
      this.show.editingAllocationValues = false
    },
    fetchLicenceData () {
      this.licencesLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/licences`)
        .then(r => {
          this.licenceData = r.data
          // console.log('adding data to map')
          const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
          this.addLicencesLayer('waterLicences', r.data.licences, '#00e676', 0.5, max)
          this.setPurposeTypes()
          this.licencesLoading = false
          this.setDemandAvailabilityData()
        })
        .catch(e => {
          this.licencesLoading = false
          console.error(e)
        })
    },
    setPurposeTypes () {
      this.purposeTypes = []
      this.licenceData.total_qty_by_purpose.forEach(item => {
        this.purposeTypes.push(item.purpose)
      })
    },
    setDemandAvailabilityData () {
      if (!this.licenceData || !this.availability) {
        return null
      }
      let mar = this.availability.reduce((a, b) => a + b, 0) / 12
      const availabilityData = {
        type: 'bar',
        name: 'Available Water',
        y: this.availability.map((val) => { return val - (this.licenceData.total_qty / 12) }),
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3'
      }

      let y = []
      let allocItemKey, monthlyQty

      // Get total quantity per month based on allocation values
      for (let i = 0; i < 12; i++) {
        monthlyQty = 0
        this.licenceData.total_qty_by_purpose.map(item => {
          allocItemKey = item.purpose.trim()
          this.initAllocationItemIfNotExists(allocItemKey)
          monthlyQty += this.computeQuantityForMonth(item.qty, this.allocationValues[allocItemKey], i + 1)
        })
        y[i] = monthlyQty
      }

      const licencePlotData = {
        type: 'bar',
        name: 'Monthly Licenced Quantity',
        y: y,
        x: this.monthHeaders.map((h) => h.text),
        hovertemplate: '%{y:.2f} m^3'
      }

      const mad30 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '20% MAD',
        y: Array(12).fill(mar * 0.2),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#5ab190' }
      }
      const mad20 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '15% MAD',
        y: Array(12).fill(mar * 0.15),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fec925' }
      }
      const mad10 = {
        type: 'line',
        mode: 'lines',
        hoverinfo: 'skip',
        name: '10% MAD',
        y: Array(12).fill(mar * 0.1),
        x: this.monthHeaders.map((h) => h.text),
        line: { color: '#fa1e44' }
      }
      this.demandAvailabilityData = [availabilityData, licencePlotData, mad10, mad20, mad30]
    }
  },
  mounted () {
    this.fetchLicenceData()
    this.loadAllocationItemsFromStorage()
  },
  beforeDestroy () {
    this.map.removeLayer('waterLicences')
    this.map.removeSource('waterLicences')
  }
}
</script>

<style>
.titleSub {
  color: #202124;
  font-weight: bold;
  font-size: 20px;
}
</style>
