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
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" x-small fab depressed light @click="openEditAllocationTableDialog">
                  <v-icon small color="primary">
                    mdi-tune
                  </v-icon>
                </v-btn>
              </template>
              <span>Configure monthly allocation coefficients</span>
            </v-tooltip>
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
          <v-col class="text-right">
             <v-btn @click="toggleLayerVisibility" color="primary" outlined>{{isLicencesLayerVisible ? 'Hide Points' : 'Show Points'}}</v-btn>
          </v-col>
        </div>
      </v-card>
    </div>

  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import ApiService from '../../../../services/ApiService'
import mapboxgl from 'mapbox-gl'

import Dialog from '../../../common/Dialog'
import { WatershedModelDescriptions } from '../../../../constants/descriptions'

import surfaceWaterMixin from '../mixins'
import MonthlyAllocationTable from './MonthlyAllocationTable.vue'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'WatershedDemand',
  mixins: [surfaceWaterMixin],
  components: {
    MonthlyAllocationTable,
    Dialog
  },
  props: ['watershedID'],
  data: () => ({
    licencesLoading: false,
    licenceData: null,
    approvalsData: null,
    licencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Quantity (m3/year)', value: 'qty', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      editingAllocationValues: false
    },
    purposeTypes: [],
    wmd: WatershedModelDescriptions,
    isLicencesLayerVisible: true
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['allocationValues', 'shortTermAllocationValues'])
  },
  methods: {
    ...mapActions('surfaceWater', ['initAllocationItemIfNotExists', 'initShortTermAllocationItemIfNotExists']),
    ...mapGetters('map', ['isMapReady']),
    ...mapMutations('surfaceWater', ['setLicencePlotData']),
    addLicencesLayer (id = 'waterLicences', data, color = '#00796b', opacity = 0.5, max = 100000000) {
      global.config.debug && console.log('licence data')
      global.config.debug && console.log(data)
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
      this.show.editingAllocationValues = false
      this.setDemandPlotData()
    },
    fetchDemandData () {
      this.licencesLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/licences`)
        .then(r => {
          this.licenceData = r.data
          // console.log('adding data to map')
          // console.log(r.data.licences)
          const max = Math.max(...r.data.licences.features.map(x => Number(x.properties.qty_m3_yr)))
          // adding null feature array breaks interpolation in layer setup
          if (r.data && r.data.licences) {
            this.addLicencesLayer('waterLicences', r.data.licences, '#00796b', 0.5, max)
          }
          // resets purposeTypes array and re-populates if any entries in list
          this.setPurposeTypes()

          this.licencesLoading = false
          this.setDemandPlotData()
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
    setDemandPlotData () {
      if (!this.licenceData) {
        return null
      }

      // Water Rights Licences Demand
      let allocationY = []
      let allocItemKey, monthlyQty
      // Get total quantity per month based on allocation values
      for (let i = 0; i < 12; i++) {
        monthlyQty = 0
        this.licenceData.total_qty_by_purpose.map(item => {
          allocItemKey = item.purpose.trim()
          this.initAllocationItemIfNotExists(allocItemKey)
          monthlyQty += this.computeQuantityForMonth(item.qty, this.allocationValues[allocItemKey], i + 1)
        })
        allocationY[i] = monthlyQty
      }
      this.setLicencePlotData(allocationY) // update store so availability vs demand graph gets new plot values
    },
    toggleLayerVisibility () {
      this.isLicencesLayerVisible = !this.isLicencesLayerVisible
      this.map.setLayoutProperty('waterLicences', 'visibility', this.isLicencesLayerVisible ? 'visible' : 'none')
      this.map.setLayoutProperty('water_rights_licences', 'visibility', this.isLicencesLayerVisible ? 'visible' : 'none')
    },
    getDemandData () {
      this.licenceData = null
      if (this.map.getLayer('waterLicences')) {
        this.map.removeLayer('waterLicences')
      }
      if (this.map.getSource('waterLicences')) {
        this.map.removeSource('waterLicences')
      }
      this.fetchDemandData()
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.getDemandData()
      }
    }
  },
  mounted () {
    if (this.isMapReady) {
      this.getDemandData()
    }
  },
  beforeDestroy () {
    if (this.map.getLayer('waterLicences')) {
      this.map.removeLayer('waterLicences')
      this.map.removeSource('waterLicences')
    }
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
