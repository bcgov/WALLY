<template>
  <div>
    <div v-if="watershedDetailsLoading">
      <v-progress-linear indeterminate show></v-progress-linear>
    </div>
    <v-tabs v-else>
      <v-tab>Watershed Details</v-tab>
      <!-- <v-tab>Climate</v-tab>
      <v-tab>Availability</v-tab>
      <v-tab>Demand</v-tab> -->
      <v-tab-item>
        <!-- <WatershedDetails :watershedID="watershedID" :record="record" :details="watershedDetails"/> -->
        <v-menu>
        <template v-slot:activator="{ on }">
          <v-btn
            color="grey darken-3"
            class="ml-3 selection-menu-buttons"
            tile
            text
            v-on="on"
          >
            Select Anchor <v-icon>keyboard_arrow_down</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in anchors"
            :key="index"
            active-class="font-weight-bold"
            @click="scrollMeTo(item.anchor)"
          >
            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
        <div>
          <MeanAnnualRunoff ref="anchor-mar" :watershedID="watershedID" :record="record" :details="watershedDetails"/>

          <WatershedAvailability ref="anchor-availability" :watershedID="watershedID" :allWatersheds="watersheds" :record="record" :details="watershedDetails"/>

          <WatershedClimate ref="anchor-climate" :watershedID="watershedID" :record="record" :details="watershedDetails"/>

          <!-- <WatershedDemand ref="anchor-demand" :watershedID="watershedID" :record="record" :details="watershedDetails"/> -->

          <!-- <div class="my-3" v-if="watershedArea">
            <span class="font-weight-bold">Area:</span>
            {{watershedArea.toFixed(1) }} sq. m ({{ (watershedArea / 1e6).toFixed(2)}} sq. km)
          </div> -->
        </div>
      </v-tab-item>
      <!-- <v-tab-item>
        <WatershedClimate :watershedID="watershedID" :record="record" :details="watershedDetails"/>
      </v-tab-item> -->
      <!-- <v-tab-item>
        <WatershedAvailability :watershedID="watershedID" :allWatersheds="watersheds" :record="record" :details="watershedDetails"/>
      </v-tab-item>
      <v-tab-item>
        <WatershedDemand :watershedID="watershedID" :record="record" :details="watershedDetails"/>
      </v-tab-item> -->
    </v-tabs>

    <!-- <SurficialGeology :watershedID="watershedID" :record="record"/> -->
  </div>
</template>

<script>
import ApiService from '../../../services/ApiService'

import WatershedClimate from './WatershedClimate'
import WatershedDemand from './WatershedDemand'
import WatershedAvailability from './WatershedAvailability'
import MeanAnnualRunoff from './MeanAnnualRunoff'
export default {
  name: 'WatershedDetails',
  props: ['watershedID', 'record', 'watersheds'],
  components: {
    WatershedClimate,
    WatershedDemand,
    WatershedAvailability,
    MeanAnnualRunoff
  },
  data: () => ({
    watershedDetails: null,
    watershedDetailsLoading: false,
    selectedAnchor: '',
    anchors: [
      {
        title: 'Mean Annual Runoff',
        anchor: 'anchor-mar'
      },
      {
        title: 'Availability',
        anchor: 'anchor-availability'
      },
      {
        title: 'Climate',
        anchor: 'anchor-climate'
      },
      {
        title: 'Demand',
        anchor: 'anchor-demand'
      },
    ]
  }),
  watch: {
    watershedID(val) {
      this.fetchWatershedDetails()
    }
  },
  computed: {
    watershedArea () {
      if (!this.record || !this.record.properties['FEATURE_AREA_SQM']) {
        return null
      }

      return Number(this.record.properties['FEATURE_AREA_SQM'])
    }
  },
  methods: {
    fetchWatershedDetails () {
      this.watershedDetailsLoading = true
      ApiService.query(`/api/v1/watersheds/${this.watershedID}`)
        .then(r => {
          this.watershedDetails = r.data
          console.log(this.watershedDetails)
          this.watershedDetailsLoading = false
        })
        .catch(e => {
          this.watershedDetailsLoading = false
          console.error(e)
        })
    },
    scrollMeTo(refName) {
      var element = this.$refs[refName];
      var top = element.offsetTop;

      window.scrollTo(0, top);
    }
  },
  mounted () {
    console.log(this.record)
    this.fetchWatershedDetails()
  }
}
</script>

<style>

</style>
