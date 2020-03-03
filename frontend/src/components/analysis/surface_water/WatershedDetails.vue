<template>
  <div ref="anchor-parent">
    <div v-if="watershedDetailsLoading">
      <v-progress-linear indeterminate show></v-progress-linear>
    </div>
    <div v-else>
      <div>Watershed Details</div>
      <div>
        <MeanAnnualRunoff ref="anchor-mar" :watershedID="watershedID" :record="record" :allWatersheds="watersheds" :details="watershedDetails"/>
        <WatershedAvailability ref="anchor-availability" :watershedID="watershedID" :allWatersheds="watersheds" :record="record" :details="watershedDetails"/>
        <WatershedClimate ref="anchor-climate" :watershedID="watershedID" :record="record" :details="watershedDetails"/>
        <SurficialGeology :watershedID="watershedID" :record="record"/>
      </div>
    </div>
  </div>
</template>

<script>
import ApiService from '../../../services/ApiService'

import WatershedClimate from './WatershedClimate'
import WatershedAvailability from './WatershedAvailability'
import MeanAnnualRunoff from './MeanAnnualRunoff'
export default {
  name: 'WatershedDetails',
  props: ['watershedID', 'record', 'watersheds'],
  components: {
    WatershedClimate,
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
      }
    ]
  }),
  watch: {
    watershedID (val) {
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
      this.watershedDetails = null
      ApiService.query(`/api/v1/watersheds/${this.watershedID}`)
        .then(r => {
          this.watershedDetailsLoading = false
          if (!r.data) {
            return
          }
          this.watershedDetails = r.data
        })
        .catch(e => {
          this.watershedDetailsLoading = false
          console.error(e)
        })
    },
    scrollMeTo (refName) {
      var element = this.$refs[refName]
      var top = element.$el.offsetTop
      this.$refs["anchor-parent"].scrollTo(0, top)
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
