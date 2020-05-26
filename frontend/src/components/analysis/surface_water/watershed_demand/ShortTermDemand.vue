<template>
  <div>
    <div class="titleSub my-5">Watershed Approved Short Term Quantities</div>
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
        <v-dialog v-model="show.editingShortTermAllocationValues" persistent>
          <ShortTermMonthlyAllocationTable
            :allocation-items="shortTermLicenceData"
            key-field="approvalNumber"
            @close="closeEditShortTermAllocationTableDialog"/>
        </v-dialog>

        <span>Total annual approved quantity:</span> {{ shortTermLicenceData.total_qty | formatNumber }} m3/year

        <Dialog v-bind="wmd.shortTermDemand"/>

        <div class="my-5">
          <div class="mb-3">Short Term Water Approval Points:</div>
          <v-data-table
            :items="tableItemData"
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
    shortTermLicenceData: {},
    shortTermPurposeHeaders: [
      { text: 'Approval Number', value: 'approvalNumber', sortable: true },
      { text: 'Quantity (m3/year)', value: 'qty', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      editingShortTermAllocationValues: false
    },
    wmd: WatershedModelDescriptions,
    isLayerVisible: true
  }),
  computed: {
    ...mapGetters('map', ['map']),
    ...mapGetters('surfaceWater', ['shortTermAllocationValues']),
    tableItemData() {
      if(this.shortTermLicenceData && this.shortTermLicenceData.approvals) {
        return this.shortTermLicenceData.approvals.features
      } else {
        return []
      }
    }
  },
  watch: {
    watershedID () {
      this.shortTermLicenceData = {}
      this.map.removeLayer('waterApprovals')
      this.map.removeSource('waterApprovals')
      this.fetchShortTermLicenceData()
    }
  },
  methods: {
    ...mapActions('surfaceWater', ['initShortTermAllocationItemIfNotExists']),
    ...mapMutations('surfaceWater', ['setShortTermLicencePlotData']),
    addApprovalsLayer (id = 'waterApprovals', data, color = '#FFE41A', opacity = 0.5, max = 100000000) {
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
      }, 'waterLicences') // Render on top of waterLicences

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
              <dt>Quantity:</dt> <dd>${qty} m3/year</dd>
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
      this.show.editingShortTermAllocationValues = true
    },
    closeEditShortTermAllocationTableDialog () {
      this.updateShortTermData()
      this.show.editingShortTermAllocationValues = false
    },
    fetchShortTermLicenceData () {
      this.approvalsLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}/approvals`)
        .then(r => {
          this.shortTermLicenceData = r.data
          console.log(r.data)
          const max = Math.max(...r.data.approvals.features.map(x => Number(x.properties.qty_m3_yr)))
          // adding null feature array breaks interpolation in layer setup
          if (r.data && r.data.approvals && r.data.approvals.length > 0) {
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
      if (!this.shortTermLicenceData) {
        return null
      }

      // Short Term Approvals Demand
      let shortTermAllocationY = []
      let allocItemKey, shortTermMonthlyQty
      // Get total short term quantity per month based on short term allocation values
      for (let i = 0; i < 12; i++) {
        shortTermMonthlyQty = 0
        this.shortTermLicenceData.map(item => {
          allocItemKey = item.approvalNumber + ' - ' + item.sourceName
          this.initShortTermAllocationItemIfNotExists(allocItemKey)
          shortTermMonthlyQty += this.computeQuantityForMonth(item.qty, this.shortTermAllocationValues[allocItemKey], i + 1)
        })
        shortTermAllocationY[i] = shortTermMonthlyQty
      }

      this.setShortTermLicencePlotData(shortTermAllocationY) // update store so availability vs demand graph gets new plot values
    },
    toggleLayerVisibility () {
      this.isLayerVisible = !this.isLayerVisible
      this.map.setLayoutProperty('waterApprovals', 'visibility', this.isLayerVisible ? 'visible' : 'none')
      this.map.setLayoutProperty('water_approval_points', 'visibility', this.isLayerVisible ? 'visible' : 'none')
    }
  },
  mounted () {
    this.fetchShortTermLicenceData()
  },
  beforeDestroy () {
    this.map.removeLayer('waterApprovals')
    this.map.removeSource('waterApprovals')
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
