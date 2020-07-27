<template>
  <v-card flat class="my-5 py-5">
    <p class="title font-weight-bold">Inventory of Streamflow Report</p>
    <div v-if="reportLink">
      <p>
        Visit EcoCat to access the <a :href="reportLink" target="_blank">{{ reportName }}</a> information and its associated data files for this area.
      </p>
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
  props: ['coordinates'],
  data: () => ({
    reportLink: null,
    reportName: null,
    hydrologicZone: null
  }),
  methods: {
    fetchReportLink () {
      const params = {
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/watersheds/streamflow_inventory?${qs.stringify(params)}`).then((r) => {
        const data = r.data
        this.reportLink = data.report_link
        this.reportName = data.report_name
        this.hydrologicZone = data.hydrologic_zone
      })
    }
  },
  mounted () {
    this.fetchReportLink()
  }

}
</script>
