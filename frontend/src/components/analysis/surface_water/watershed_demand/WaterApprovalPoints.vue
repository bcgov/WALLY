<template>
  <v-card flat>
    <v-card-text class="pb-0">
      <h3>Water Approval Points (Short Term Licences)</h3>
    </v-card-text>
    <v-card-text v-if="approvalsLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </v-card-text>
    <v-card-text v-if="shortTermLicenceData">
      <v-row>
        <v-col>
          <v-card flat outlined tile>
            <v-card-title>
              Total annual approved quantity
              <Dialog v-bind="wmd.shortTermDemand"/>
            </v-card-title>
            <v-card-text class="info-blue">
              <strong> {{ shortTermLicenceData.total_qty | formatNumber }} m³/year</strong>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-data-table
        :items="shortTermFeatures"
        :headers="shortTermPurposeHeaders"
        sort-by="qty"
        sort-desc
      >
        <template v-slot:top>
          <v-toolbar flat>
            <h4>Short Term Water Approval Points</h4>
          </v-toolbar>
        </template>
        <template v-slot:item.qty="{ item }">
          {{ item.qty | formatNumber }}
        </template>
      </v-data-table>

      <v-dialog v-model="show.shortTermAllocationTable" persistent>
        <ShortTermMonthlyAllocationTable
          :allocation-items="shortTermFeatures"
          key-field="APPROVAL_FILE_NUMBER"
          @close="closeShortTermAllocation"/>
      </v-dialog>

      <v-card-actions>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" small depressed light @click="openEditShortTermAllocationTableDialog">
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
            <v-btn v-on="on" small  depressed light class="ml-2" @click="toggleLayerVisibility">
              <v-icon small>
                layers
              </v-icon>
              {{ isLayerVisible ? 'Hide' : 'Show'}} points on map
            </v-btn>
          </template>
          <span>{{ isLayerVisible ? 'Hide' : 'Show'}} Water Approval Points Layer</span>
        </v-tooltip>
      </v-card-actions>

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
import ShortTermMonthlyAllocationTable from './ShortTermMonthlyAllocationTable.vue'

const popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false
})

export default {
  name: 'ShortTermDemand',
  mixins: [surfaceWaterMixin],
  components: {
    ShortTermMonthlyAllocationTable,
    Dialog
  },
  props: ['watershedID'],
  data: () => ({
    approvalsLoading: false,
    shortTermLicenceData: null,
    shortTermPurposeHeaders: [
      { text: 'Approval Number', value: 'APPROVAL_FILE_NUMBER', sortable: true },
      { text: 'Works', value: 'WORKS_DESCRIPTION' },
      { text: 'Start Date', value: 'APPROVAL_START_DATE' },
      { text: 'Expiry Date', value: 'APPROVAL_EXPIRY_DATE' },
      { text: 'Quantity (m³/year)', value: 'qty_m3_yr', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      shortTermAllocationTable: false
    },
    wmd: WatershedModelDescriptions,
    isLayerVisible: true
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['shortTermAllocationValues']),
    shortTermFeatures () {
      if (this.shortTermLicenceData && this.shortTermLicenceData.approvals) {
        return this.shortTermLicenceData.approvals.features.map((f) => {
          return f.properties
        })
      } else {
        return []
      }
    }
  },
  methods: {
    ...mapActions('surfaceWater', ['initShortTermAllocationItemIfNotExists']),
    ...mapGetters('map', ['isMapReady']),
    ...mapMutations('surfaceWater', ['setShortTermLicencePlotData']),
    addApprovalsLayer (id = 'waterApprovals', data, color = '#FFE41A', opacity = 0.5, max = 100000000) {
      if (this.map.getLayer('waterApprovals')) {
        return
      }

      this.map.addSource('waterApprovals', {
        'type': 'geojson',
        'data': data
      })

      this.map.addLayer({
        id: 'waterApprovalsCoverPoints',
        type: 'circle',
        source: 'waterApprovals',
        paint: {
          'circle-color': color,
          'circle-radius': 5,
          'circle-opacity': 1,
          'circle-stroke-width': 2,
          'circle-stroke-color': '#ffffff'
        }
      })

      this.map.addLayer({
        id: id,
        type: 'circle',
        source: 'waterApprovals',
        paint: {
          'circle-color': color,
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['number', ['get', 'qty_m³_yr'], 0],
            0,
            10,
            max,
            max > 1000000 ? 50 : 25
          ],
          'circle-opacity': opacity
        }
      }, 'waterApprovalsCoverPoints')

      this.map.on('mouseenter', id, (e) => {
        // Change the cursor style as a UI indicator.
        this.map.getCanvas().style.cursor = 'pointer'

        let coordinates = e.features[0].geometry.coordinates.slice()
        let approvalNumber = e.features[0].properties['APPROVAL_FILE_NUMBER']
        let sourceName = e.features[0].properties['SOURCE']
        let qty = e.features[0].properties['qty_m3_yr']
        let worksDescription = e.features[0].properties['WORKS_DESCRIPTION']
        let startDate = e.features[0].properties['APPROVAL_START_DATE']
        let expiryDate = e.features[0].properties['APPROVAL_EXPIRY_DATE']

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
              <dt>Approval file no.:</dt> <dd>${approvalNumber}</dd>
              <dt>Source:</dt> <dd>${sourceName}</dd>
              <dt>Quantity:</dt> <dd>${qty} m³/year</dd>
              <dt>Works Description:</dt> <dd>${worksDescription}</dd>
              <dt>Start Date:</dt> <dd>${startDate}</dd>
              <dt>Expiry Date:</dt> <dd>${expiryDate}</dd>
            </dl>

          `)
          .addTo(this.map)
      })

      this.map.on('mouseleave', id, () => {
        this.map.getCanvas().style.cursor = ''
        popup.remove()
      })
    },
    openEditShortTermAllocationTableDialog () {
      this.show.shortTermAllocationTable = true
    },
    closeShortTermAllocation () {
      this.show.shortTermAllocationTable = false
      this.updateShortTermData()
    },
    fetchShortTermLicenceData () {
      this.approvalsLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/approvals`)
        .then(r => {
          this.shortTermLicenceData = r.data
          // console.log(r.data)
          const max = Math.max(...r.data.approvals.features.map(x => Number(x.properties.qty_m3_yr)))
          // adding null feature array breaks interpolation in layer setup
          if (r.data && r.data.approvals) {
            this.addApprovalsLayer('waterApprovals', r.data.approvals, '#FFE41A', 0.5, max)
          }
          this.approvalsLoading = false
          this.updateShortTermData()
        })
        .catch(e => {
          this.approvalsLoading = false
          console.error(e)
        })
    },
    updateShortTermData () {
      if (!this.shortTermLicenceData ||
          !this.shortTermLicenceData.approvals ||
          !this.shortTermLicenceData.approvals.features) {
        return null
      }

      let features = this.shortTermLicenceData.approvals.features

      // Short Term Approvals Demand
      let shortTermAllocationY = []
      let allocItemKey, shortTermMonthlyQty

      global.config.debug && console.log('updating short term data')
      global.config.debug && console.log(this.shortTermAllocationValues)

      // Get total short term quantity per month based on short term allocation values
      // many points are duplicate records so we only save one allocation record for
      // each approval file number
      for (let i = 0; i < 12; i++) {
        shortTermMonthlyQty = 0
        features.map(item => {
          let properties = item.properties
          allocItemKey = properties.APPROVAL_FILE_NUMBER
          this.initShortTermAllocationItemIfNotExists(allocItemKey)
          shortTermMonthlyQty += this.computeQuantityForMonth(properties.qty_m3_yr || 0, this.shortTermAllocationValues[allocItemKey], i + 1)
        })
        shortTermAllocationY[i] = shortTermMonthlyQty
      }

      this.setShortTermLicencePlotData(shortTermAllocationY) // update store so availability vs demand graph gets new plot values
    },
    toggleLayerVisibility () {
      this.isLayerVisible = !this.isLayerVisible
      this.map.setLayoutProperty('waterApprovals', 'visibility', this.isLayerVisible ? 'visible' : 'none')
      this.map.setLayoutProperty('waterApprovalsCoverPoints', 'visibility', this.isLayerVisible ? 'visible' : 'none')
      this.map.setLayoutProperty('water_approval_points', 'visibility', this.isLayerVisible ? 'visible' : 'none')
    },
    getWaterApprovals () {
      this.shortTermLicenceData = null
      this.setShortTermLicencePlotData(null)
      if (this.map.getLayer('waterApprovals')) {
        this.map.removeLayer('waterApprovals')
      }
      if (this.map.getLayer('waterApprovalsCoverPoints')) {
        this.map.removeLayer('waterApprovalsCoverPoints')
      }
      if (this.map.getSource('waterApprovals')) {
        this.map.removeSource('waterApprovals')
      }
      this.fetchShortTermLicenceData()
    }
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.getWaterApprovals()
      }
    }
  },
  mounted () {
    if (this.isMapReady()) {
      this.getWaterApprovals()
    }
  },
  beforeDestroy () {
    if (this.map.getLayer('waterApprovals')) {
      this.map.removeLayer('waterApprovals')
    }
    if (this.map.getLayer('waterApprovalsCoverPoints')) {
      this.map.removeLayer('waterApprovalsCoverPoints')
    }
    if (this.map.getSource('waterApprovals')) {
      this.map.removeSource('waterApprovals')
    }
  }
}
</script>
