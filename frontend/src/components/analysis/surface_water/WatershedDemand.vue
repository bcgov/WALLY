<template>
  <div>
    <div class="title my-5">Watershed Demand</div>
    <div v-if="licencesLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="licenceData">
      <div class="font-weight-bold my-3">Water Rights Licences</div>

      <span>Total annual licenced quantity:</span> {{ licenceData.total_qty.toFixed(1) }} m3/year
      <div class="my-5">
        <div class="mb-3">
          Annual licenced quantity by use type:
          <v-btn  icon @click="show.licencesInfo = true">
            <v-icon>info</v-icon>
          </v-btn>
        </div>
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
      <v-dialog v-model="show.licencesInfo" max-width="400">
        <v-card>
          <v-card-title class="headline">
            Annual licenced quantity
          </v-card-title>
          <v-card-text>
            Morbi eros orci, euismod id dignissim sodales, consequat quis ipsum. Nam a eleifend tellus. Morbi faucibus varius vestibulum. Vestibulum non molestie odio. Pellentesque eget sollicitudin est. Morbi ac mollis enim. Nulla facilisi.
          </v-card-text>
          <v-card-actions>
            <v-btn color="green darken-1" text @click="openEditAllocationTableDialog">
              <v-icon small>
                mdi-tune
              </v-icon>
              Allocation values
            </v-btn>
            <v-btn text @click="show.licencesInfo = false">Cancel</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <MonthlyAllocationTable
        :edit="show.editingAllocationValues"
        :qtyByPurpose="licenceData.total_qty_by_purpose"
        @close="closeEditAllocationTableDialog"/>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../../services/ApiService'
import mapboxgl from 'mapbox-gl'

import MonthlyAllocationTable from './watershed_demand/MonthlyAllocationTable'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'SurfaceWaterDemand',
  components: {
    MonthlyAllocationTable
  },
  props: ['watershedID', 'record'],
  data: () => ({
    licencesLoading: false,
    licenceData: null,
    licencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Quantity (m3/year)', value: 'qty' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      editingAllocationValues: false,
      licencesInfo: false
    },
    purposeTypes: []
  }),
  computed: {
    ...mapGetters('map', ['map'])
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
      this.show.licencesInfo = false
    },
    closeEditAllocationTableDialog () {
      this.show.editingAllocationValues = false
    },
    fetchLicenceData () {
      this.licencesLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/licences`)
        .then(r => {
          this.licenceData = r.data
          console.log('adding data to map')
          const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
          this.addLicencesLayer('waterLicences', r.data.licences, '#00e676', 0.5, max)
          this.setPurposeTypes()
          this.licencesLoading = false
        })
        .catch(e => {
          this.licencesLoading = false
          console.error(e)
        })
    },
    setPurposeTypes () {
      // console.log(this.licenceData.total_qty_by_purpose)
      this.purposeTypes = []
      this.licenceData.total_qty_by_purpose.forEach(item => {
        console.log(item)
        this.purposeTypes.push(item.purpose)
      })
      console.log(this.purposeTypes)
    },
    computeQuantityPerMonth (qtyPerYear, allocValues) {
      // alloc values must be empty or length 12
      let defaultAllocValue = 1
      let monthlyQty = []
      let allocFraction

      for (let i = 0; i < 12; i++) {
        if (allocValues.length === 0) {
          allocFraction = defaultAllocValue
        } else {
          allocFraction = allocValues[i]
        }
        monthlyQty.push(qtyPerYear * (allocFraction / 12))
      }
      return monthlyQty
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
