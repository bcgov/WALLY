<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
     Watershed Monthly Discharge
      <v-icon small class="ml-1">mdi-information-outline</v-icon>
    </v-card-title>
    <v-card-text>
      <img src="mockups/watershed_monthly_discharge.png" width="800"/>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'MonthlyDischarge',
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
