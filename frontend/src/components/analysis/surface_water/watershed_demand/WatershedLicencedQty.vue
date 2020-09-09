<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Licenced Quantity
    </v-card-title>
    <v-card-text v-if="licencesLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="licenceData">
      <h3>Water Rights Licences</h3>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Total annual licenced quantity
              <Dialog v-bind="wmd.waterRightsLicenceDemand"/>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>{{ licenceData.total_qty.toFixed(1) | formatNumber }} m³/year</strong>
              <span class="caption ml-1 disabled">(**note: change to m³/s?)</span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-data-table
        :headers="licencePurposeHeaders"
        :items="licenceData.total_qty_by_purpose"
        :single-expand="singleExpand"
        :expanded.sync="expanded"
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

      <v-dialog v-model="show.editingAllocationValues" persistent>
        <MonthlyAllocationTable
          :allocation-items="licenceData.total_qty_by_purpose"
          key-field="purpose"
          @close="closeEditAllocationTableDialog"/>
      </v-dialog>

      <v-card-actions>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small depressed light>
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

      <v-divider class="mt-8 mb-8"></v-divider>
      <!-- Water approval points -->
      <h3>Water Approval Points (Short Term Licences)</h3>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Total annual approved quantity
              <v-icon small class="ml-1">mdi-information-outline</v-icon>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>000000.00 m³/year</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-data-table
        :headers="approvalHeaders"
        :items="approvalPoints"
        item-key="useType"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <h4>Short Term Water Approval Points</h4>
          </v-toolbar>
        </template>
      </v-data-table>
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
          <span>Configure short term monthly allocation coefficients</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small  depressed light class="ml-2" @click="toggleWaterApprovalPointsLayerVisibility">
              <v-icon small>
                layers
              </v-icon>
              {{ isWaterApprovalPointsLayerVisible ? 'Hide' : 'Show'}} points on map
            </v-btn>
          </template>
          <span>{{ isWaterApprovalPointsLayerVisible ? 'Hide' : 'Show'}} Water Approval Points Layer</span>
        </v-tooltip>
      </v-card-actions>

      <v-divider class="mt-8 mb-8"></v-divider>
      <!-- Availability vs Licensed Quantity -->
      <h3>Availability vs Licensed Quantity</h3>
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              How to read this graph
              <!--              <v-icon small class="ml-1">mdi-information-outline</v-icon>-->
            </v-card-title>
            <v-card-text class="info-blue">
              <strong>
                This graph shows available water after allocation from existing surface water licences, as determined by subtracting licensed quantities (including any adjusted monthly allocation values) from the estimated discharge for each month.
              </strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <img src="mockups/available_vs_monthly.png" width="800" />
      </v-row>

      <!--      <v-card-actions>-->
      <!--        <v-tooltip bottom>-->
      <!--          <template v-slot:activator="{ on }">-->
      <!--            <v-btn v-on="on" small depressed light>-->
      <!--              <v-icon small color="primary">-->
      <!--                mdi-tune-->
      <!--              </v-icon>-->
      <!--              Monthly allocation coefficients-->
      <!--            </v-btn>-->
      <!--          </template>-->
      <!--          <span>Configure short term monthly allocation coefficients</span>-->
      <!--        </v-tooltip>-->
      <!--        <v-tooltip bottom>-->
      <!--          <template v-slot:activator="{ on }">-->
      <!--            <v-btn v-on="on" small  depressed light class="ml-2">-->
      <!--              <v-icon small>-->
      <!--                layers-->
      <!--              </v-icon>-->
      <!--              Hide points on map-->
      <!--            </v-btn>-->
      <!--          </template>-->
      <!--          <span>Hide Water Approval Points Layer</span>-->
      <!--        </v-tooltip>-->
      <!--      </v-card-actions>-->
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
  name: 'WatershedLicencedQty',
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
    show: {
      editingAllocationValues: false
    },
    purposeTypes: [],
    wmd: WatershedModelDescriptions,
    isLicencesLayerVisible: true,
    isWaterApprovalPointsLayerVisible: true,
    singleExpand: false,
    expanded: [],
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
    toggleWaterLicenceLayerVisibility () {
      if (this.isLicencesLayerVisible) {
        this.$store.dispatch('map/removeMapLayer', 'water_rights_licences')
        this.$store.dispatch('map/removeMapLayer', 'waterLicences')
      } else {
        this.$store.dispatch('map/addMapLayer', 'water_rights_licences')
        this.$store.dispatch('map/addMapLayer', 'waterLicences')
      }

      this.isLicencesLayerVisible = !this.isLicencesLayerVisible

      // TODO: Can we take this out? This code just hides the layer points on the map but keeps it in the map legend
      // this.map.setLayoutProperty('waterLicences', 'visibility', this.isLicencesLayerVisible ? 'visible' : 'none')
      // this.map.setLayoutProperty('water_rights_licences', 'visibility', this.isLicencesLayerVisible ? 'visible' : 'none')
    },
    toggleWaterApprovalPointsLayerVisibility () {
      if (this.isWaterApprovalPointsLayerVisible) {
        this.$store.dispatch('map/removeMapLayer', 'water_approval_points')
      } else {
        this.$store.dispatch('map/addMapLayer', 'water_approval_points')
      }

      this.isWaterApprovalPointsLayerVisible = !this.isWaterApprovalPointsLayerVisible
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
      console.log('1')
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
