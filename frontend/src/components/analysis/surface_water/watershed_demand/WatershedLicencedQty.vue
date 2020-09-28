<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Licenced Quantity
    </v-card-title>

    <WaterRightsLicences :modelOutputs="modelOutputs"
                         :watershedID="watershedID"/>

    <v-card-text>
      <v-divider class="mt-3 mb-3"></v-divider>
    </v-card-text>

    <WaterApprovalPoints :watershedID="watershedID"/>

    <v-card-text>
      <v-divider class="mt-3 mb-3"></v-divider>
    </v-card-text>

    <AvailabilityVsLicencedQty />
  </v-card>
</template>

<script>
import WaterRightsLicences from './WaterRightsLicences'
import WaterApprovalPoints from './WaterApprovalPoints'
import AvailabilityVsLicencedQty from './AvailabilityVsLicencedQty'

export default {
  name: 'WatershedLicencedQty',
  components: {
    WaterRightsLicences,
    WaterApprovalPoints,
    AvailabilityVsLicencedQty
  },
  props: ['watershedID', 'modelOutputs'],
  data: () => ({

  }),
  computed: {
  },
  methods: {
  },
  watch: {
  },
  mounted () {
  },
  beforeDestroy () {

  }
}
</script>
