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

        <span>Total annual approved quantity:</span> {{ shortTermLicenceData.total_qty | formatNumber }} m3/year

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
      { text: 'Approval Number', value: 'APPROVAL_FILE_NUMBER', sortable: true },
      { text: 'Works', value: 'WORKS_DESCRIPTION' },
      { text: 'Start Date', value: 'APPROVAL_START_DATE' },
      { text: 'Expiry Date', value: 'APPROVAL_EXPIRY_DATE' },
      { text: 'Quantity (m3/year)', value: 'qty_m3_yr', align: 'end' },
      { text: '', value: 'action', sortable: false }
    ],
    show: {
      shortTermAllocationTable: false
    },
    wmd: WatershedModelDescriptions,
    isLayerVisible: true,
    emptyMonths: [0,0,0,0,0,0,0,0,0,0,0,0]
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
      // console.log(data)
      this.map.addLayer({
        id: id,
        type: 'circle',
        source: {
          type: 'geojson',
          data: data
        },
        paint: {
          'circle-color': color,
          'circle-radius': 10,
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
          this.setShortTermLicencePlotData(this.emptyMonths)
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

      console.log("updating short term data")
      console.log(this.shortTermAllocationValues)

      // Get total short term quantity per month based on short term allocation values
      // many points are duplicate records so we only save one allocation record for
      // each approval file number 
      for (let i = 0; i < 12; i++) {
        shortTermMonthlyQty = 0
        features.map(item => {
          let properties = item.properties
          allocItemKey = properties.APPROVAL_FILE_NUMBER
          this.initShortTermAllocationItemIfNotExists(allocItemKey)
          shortTermMonthlyQty += this.computeQuantityForMonth(properties.qty_m3_yr, this.shortTermAllocationValues[allocItemKey], i + 1)
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
    if (this.map.getLayer('waterApprovals')) {
      this.map.removeLayer('waterApprovals')
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
