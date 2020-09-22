<template>
  <v-card flat>
    <v-card-text class="pb-0">
      <h3>Water Rights Licences</h3>
    </v-card-text>
    <v-card-text v-if="licencesLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="licenceData" class="pt-0">
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Total annual licenced quantity
              <Dialog v-bind="wmd.waterRightsLicenceDemand"/>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ licenceData.total_qty.toFixed(1) | formatNumber }} m³/year</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <div class="subtitle font-weight-bold">Current Licences</div>
      <p>
        Total quantities and individual licence data in this table only reflect current licences.
        See "Canceled, Expired and Inactive Licences" below for inactive licences.
      </p>
      <v-data-table
        :headers="licencePurposeHeaders"
        :items="licenceData.total_qty_by_purpose.filter(x => x.licences && x.licences.length)"
        :single-expand="singleExpandLicences"
        :expanded.sync="expandedActiveLicences"
        item-key="purpose"
        show-expand
        @click:row="clearLicenceHighlight"
      >
        <!--        <template v-slot:top>-->
        <!--          <v-toolbar flat>-->
        <!--            <h4>Total annual licenced quantity: {{ licenceData.total_qty.toFixed(1) | formatNumber }} m³/year </h4>-->
        <!--          </v-toolbar>-->
        <!--        </template>-->
        <template v-slot:[`item.qty_sec`]="{ item }">
          {{ (item.qty / secInYear).toFixed(6) | formatNumber }}
        </template>
        <template v-slot:[`item.qty`]="{ item }">
          {{ item.qty.toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.min`]="{ item }">
          {{ Math.min.apply(Math, item.licences.map((o) =>  o.properties.quantityPerYear )).toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.max`]="{ item }">
          {{ Math.max.apply(Math, item.licences.map((o) => o.properties.quantityPerYear )).toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.count`]="{ item }">
          {{ item.licences.length }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <WatershedIndividualLicences :licences="item.licences"/>
          </td>
        </template>
      </v-data-table>

      <div class="subtitle font-weight-bold">Canceled, Expired and Inactive Licences</div>

      <v-data-table
        :headers="inactiveLicencePurposeHeaders"
        :items="licenceData.total_qty_by_purpose.filter(x => x.inactive_licences && x.inactive_licences.length)"
        :single-expand="singleExpandInactiveLicences"
        :expanded.sync="expandedInactiveLicences"
        item-key="purpose"
        show-expand
      >
        <template v-slot:[`item.qty_sec`]="{ item }">
          {{ (item.qty / secInYear).toFixed(6) }}
        </template>
        <template v-slot:[`item.qty`]="{ item }">
          {{ item.qty.toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.min`]="{ item }">
          {{ Math.min.apply(Math, item.inactive_licences.map((o) =>  o.properties.quantityPerYear )).toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.max`]="{ item }">
          {{ Math.max.apply(Math, item.inactive_licences.map((o) => o.properties.quantityPerYear )).toFixed(0) | formatNumber }}
        </template>
        <template v-slot:[`item.count`]="{ item }">
          {{ item.inactive_licences.length }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <WatershedIndividualLicences :licences="item.inactive_licences"/>
          </td>
        </template>
      </v-data-table>

      <v-dialog v-model="show.editingAllocationValues" persistent>
        <MonthlyAllocationTable
          :allocation-items="licenceData.total_qty_by_purpose"
          key-field="purpose"
          @close="closeEditAllocationTableDialog"/>
      </v-dialog>

      <v-card-actions>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small depressed light @click="openEditAllocationTableDialog">
              <v-icon small color="primary">
                mdi-tune
              </v-icon>
              Monthly allocation coefficients
            </v-btn>
          </template>
          <span>Configure monthly allocation coefficients</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small  depressed light class="ml-2" @click="toggleWaterLicenceLayerVisibility">
              <v-icon small>
                layers
              </v-icon>
              {{ isLicencesLayerVisible ? 'Hide' : 'Show'}} points on map
            </v-btn>
          </template>
          <span>{{ isLicencesLayerVisible ? 'Hide' : 'Show'}} Water Rights Licences Layer</span>
        </v-tooltip>
      </v-card-actions>
    </v-card-text>
    <v-card-text v-else-if="!licencesLoading">
      No licences found
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'
import ApiService from '../../../../services/ApiService'
import mapboxgl from 'mapbox-gl'

import Dialog from '../../../common/Dialog'
import { WatershedModelDescriptions } from '../../../../constants/descriptions'

import surfaceWaterMixin from '../mixins'
import MonthlyAllocationTable from './MonthlyAllocationTable.vue'
import WatershedIndividualLicences from './WatershedIndividualLicences.vue'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'WaterRightsLicences',
  mixins: [surfaceWaterMixin],
  components: {
    MonthlyAllocationTable,
    WatershedIndividualLicences,
    Dialog
  },
  props: ['watershedID'],
  data: () => ({
    licencesLoading: false,
    licenceData: null,
    approvalsData: null,
    licencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Quantity (m³/sec)', value: 'qty_sec', align: 'end' },
      { text: 'Quantity (m³/year)', value: 'qty', align: 'end' },
      { text: 'Min Use (m³/year)', value: 'min', align: 'end' },
      { text: 'Max Use (m³/year)', value: 'max', align: 'end' },
      { text: '# Licences', value: 'count', align: 'center' },
      { text: '', value: 'data-table-expand' }
    ],
    inactiveLicencePurposeHeaders: [
      { text: 'Use type', value: 'purpose', sortable: true },
      { text: 'Min Use (m³/year)', value: 'min', align: 'end' },
      { text: 'Max Use (m³/year)', value: 'max', align: 'end' },
      { text: '# Licences', value: 'count', align: 'center' },
      { text: '', value: 'data-table-expand' }
    ],
    show: {
      editingAllocationValues: false
    },
    purposeTypes: [],
    wmd: WatershedModelDescriptions,
    isLicencesLayerVisible: true,
    singleExpandLicences: false,
    singleExpandInactiveLicences: false,
    expandedActiveLicences: [],
    expandedInactiveLicences: [],
    secInYear: 31536000
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['allocationValues', 'shortTermAllocationValues'])
  },
  methods: {
    ...mapActions('surfaceWater', ['initAllocationItemIfNotExists', 'initShortTermAllocationItemIfNotExists']),
    ...mapGetters('map', ['isMapReady']),
    ...mapMutations('surfaceWater', ['setLicencePlotData']),
    ...mapMutations('map', ['updateHighlightFeatureData']),
    addLicencesLayer (id = 'waterLicences', data, color = '#00796b', opacity = 0.5, max = 100000000) {
      global.config.debug && console.log('licence data')
      global.config.debug && console.log(data)

      if (this.map.getLayer('waterLicences')) {
        return
      }

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
        let qty = e.features[0].properties['qty_m3_yr']
        if (qty) { qty = qty.toFixed(1) } // fix on null value
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
              <dt>Quantity:</dt> <dd>${qty} m³/year</dd>
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
          // An empty feature array can't be interpolated by mapbox-gl
          if (r.data && r.data.licences && r.data.licences.length > 0) {
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
    toggleWaterLicenceLayerVisibility () {
      if (this.isLicencesLayerVisible) {
        this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
      } else {
        this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
      }

      if (this.licenceData && this.licenceData.total_qty_by_purpose && this.licenceData.total_qty_by_purpose.length > 0) {
        this.map.setLayoutProperty('waterLicences', 'visibility', this.isLicencesLayerVisible ? 'none' : 'visible')
      }
      this.isLicencesLayerVisible = !this.isLicencesLayerVisible
    },
    getDemandData () {
      this.licenceData = null
      this.setLicencePlotData(null)
      if (this.map.getLayer('waterLicences')) {
        this.map.removeLayer('waterLicences')
      }
      if (this.map.getSource('waterLicences')) {
        this.map.removeSource('waterLicences')
      }
      this.fetchDemandData()
    },
    clearLicenceHighlight (value) {
      this.updateHighlightFeatureData({})
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
    if (this.isMapReady()) {
      this.getDemandData()
    }
  },
  beforeDestroy () {
    if (this.map.getLayer('waterLicences')) {
      this.map.removeLayer('waterLicences')
      this.map.removeSource('waterLicences')
    }
    this.updateHighlightFeatureData({})
  }
}
</script>
