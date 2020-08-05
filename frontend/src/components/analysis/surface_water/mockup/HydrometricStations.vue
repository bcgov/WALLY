<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
     Hydrometric Stations
    </v-card-title>
    <v-card-text>
      <p class="text--disabled">No hydrometric stream flow stations found in this area</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'HydrometricStations',
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
