<template>
  <v-card v-if="this.surface_water_design_v2" class="watershedInfo" flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Inventory of Streamflow Report
    </v-card-title>
    <v-card-text>
      <div v-if="loading">
        <v-progress-linear show indeterminate></v-progress-linear>
      </div>
      <div v-else-if="reportLink">
        <p>
          Visit EcoCat to access the <a :href="reportLink" target="_blank">{{ reportName }}</a> information and its associated data files for this area.
        </p>
      </div>
      <div v-else>
        <p class="text--disabled">No streamflow inventory report found for this region.</p>
      </div>
    </v-card-text>
  </v-card>
  <v-card v-else flat class="my-5 py-5">
    <p class="title font-weight-bold">Inventory of Streamflow Report</p>
    <div v-if="reportLink">

    </div>
    <p v-else class="text--disabled">No streamflow inventory report found for this region.</p>
  </v-card>
</template>
<script>
import qs from 'querystring'
import ApiService from '../../../../services/ApiService'

export default {
  name: 'StreamflowInventory',
  components: {
  },
  props: ['coordinates', 'generatedWatershedID', 'surface_water_design_v2'],
  data: () => ({
    reportLink: null,
    reportName: null,
    hydrologicZone: null,
    loading: true
  }),
  methods: {
    fetchReportLink () {
      const params = {
        point: JSON.stringify(this.coordinates),
        generated_watershed_id: this.generatedWatershedID
      }
      this.loading = true
      ApiService.query(`/api/v1/watersheds/streamflow_inventory?${qs.stringify(params)}`).then((r) => {
        const data = r.data
        this.reportLink = data.report_link
        this.reportName = data.report_name
        this.hydrologicZone = data.hydrologic_zone
        this.loading = false
      }).catch((e) => {
        this.loading = false
        console.error(e)
      })
    }
  },
  mounted () {
    this.fetchReportLink()
  }

}
</script>
