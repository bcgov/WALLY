<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
     Inventory of Streamflow Report
    </v-card-title>
    <v-card-text>
      <div>
        <p>
          Visit EcoCat to access the
          <a href="https://a100.gov.bc.ca/pub/acat/public/viewReport.do?reportId=53344" target="_blank">
          Inventory of Streamflow in the South Coast and West Coast Regions
          </a> information and its associated data files for this area.
        </p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'StreamflowReport',
  components: {
  },
  data: () => ({

  }),
  mounted () {
  },
  beforeDestroy () {
  }
}
</script>

<style>
  .v-list-item__content, .v-select__selection{
    text-transform: capitalize;
  }
  #surfaceWaterDesign .info-blue .v-icon{
    color: teal;
  }
  #surfaceWaterDesign .v-card__title{
    font-size: 1rem
  }
  #surfaceWaterDesign .v-alert{
    font-size: .9rem
  }
</style>
