<template>
  <div>
    <div v-if="approvalsLoading">
      <v-progress-linear show indeterminate></v-progress-linear>
    </div>
    <div v-if="shortTermLicenceData">
      <v-card flat>
        <v-card-title class="pl-0">
          Water Approval Points (Short Term Licences)
          <v-card-actions>
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" x-small fab depressed light @click="openEditShortTermAllocationTableDialog">
                  <v-icon small color="primary">
                    mdi-tune
                  </v-icon>
                </v-btn>
              </template>
              <span>Configure short term monthly allocation coefficients</span>
            </v-tooltip>
          </v-card-actions>

        </v-card-title>
        <v-dialog v-model="show.shortTermAllocationTable" persistent>
          <ShortTermMonthlyAllocationTable
            :allocation-items="shortTermFeatures"
            key-field="APPROVAL_FILE_NUMBER"
            @close="closeShortTermAllocation"/>
        </v-dialog>

        <span>Total annual approved quantity:</span> {{ shortTermLicenceData.total_qty | formatNumber }} m³/year

        <Dialog v-bind="wmd.shortTermDemand"/>

        <div class="my-5">
          <div class="mb-3">Short Term Water Approval Points:</div>
          <v-data-table
            :items="shortTermFeatures"
            :headers="shortTermPurposeHeaders"
            sort-by="qty"
            sort-desc
          >
            <template v-slot:item.qty="{ item }">
              {{ item.qty | formatNumber }}
            </template>
          </v-data-table>
          <v-col class="text-right">
             <v-btn @click="toggleLayerVisibility" color="primary" outlined>{{isLayerVisible ? 'Hide Points' : 'Show Points'}}</v-btn>
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
import qs from 'querystring'
import Dialog from '../../../common/Dialog'
import { WatershedModelDescriptions } from '../../../../constants/descriptions'

import surfaceWaterMixin from '../mixins'
import ShortTermMonthlyAllocationTable from './ShortTermMonthlyAllocationTable.vue'
import { geojsonFC } from '../../../../common/mapbox/features'

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
  props: ['watershedID', 'generatedWatershedID'],
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
      this.map.addSource('waterApprovals', geojsonFC(data))

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
        id,
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

        const coordinates = e.features[0].geometry.coordinates.slice()
        const approvalNumber = e.features[0].properties.APPROVAL_FILE_NUMBER
        const sourceName = e.features[0].properties.SOURCE
        const qty = e.features[0].properties.qty_m3_yr
        const worksDescription = e.features[0].properties.WORKS_DESCRIPTION
        const startDate = e.features[0].properties.APPROVAL_START_DATE
        const expiryDate = e.features[0].properties.APPROVAL_EXPIRY_DATE

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
      const params = {
        generated_watershed_id: this.generatedWatershedID
      }
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/approvals?${qs.stringify(params)}`)
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

      const features = this.shortTermLicenceData.approvals.features

      // Short Term Approvals Demand
      const shortTermAllocationY = []
      let allocItemKey, shortTermMonthlyQty

      global.config.debug && console.log('updating short term data')
      global.config.debug && console.log(this.shortTermAllocationValues)

      // Get total short term quantity per month based on short term allocation values
      // many points are duplicate records so we only save one allocation record for
      // each approval file number
      for (let i = 0; i < 12; i++) {
        shortTermMonthlyQty = 0
        features.map(item => {
          const properties = item.properties
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

<style>
.titleSub {
  color: #202124;
  font-weight: bold;
  font-size: 20px;
}
</style>
