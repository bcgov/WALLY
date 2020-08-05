<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Fish Inventory Data Queries
    </v-card-title>
    <v-card-text>
      <v-card-subtitle class="pr-0 pl-2">
        Search the Fish Inventory Data Queries database using the following watershed codes
      </v-card-subtitle>
      <v-btn v-on="on" small  depressed light class="ml-2"
             href="http://a100.gov.bc.ca/pub/fidq/viewSingleWaterbody.do?searchCriteria.watershedCode=900-004300-70100-41500">

        <v-icon small>
          mdi-link-variant
        </v-icon>
        Query: 900-004300-70100-41500
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'FIDQ',
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
