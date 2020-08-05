<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Comparative Runoff Models
    </v-card-title>
    <v-card-actions>
      <v-card-subtitle class="pr-0 pl-2">
        Source

      </v-card-subtitle>
      <v-btn v-on="on" small  depressed light class="ml-2"
             href="https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrometric-watershed-boundaries">

        <v-icon small>
          mdi-link-variant
        </v-icon>
        Hydrometric Watersheds (DataBC)
      </v-btn>
    </v-card-actions>
    <v-row class="pl-3 pr-3">
      <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Annual normalized runoff
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>000000.00 mm</strong>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Watershed area (highlighted area)
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>000000.00 sq. m</strong>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="pl-3 pr-3">
      <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Using normalized runoff from
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>Watershed Name</strong>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <img src="mockups/runoff.png" width="700"/>
    <v-divider class="mt-8 mb-8"></v-divider>
    <v-card-actions>
      <v-card-subtitle class="pr-0 pl-2">
        Source
      </v-card-subtitle>
      <v-btn v-on="on" small  depressed light class="ml-2"
             href="https://catalogue.data.gov.bc.ca/dataset/hydrology-normal-annual-runoff-isolines-1961-1990-historical">

        <v-icon small>
          mdi-link-variant
        </v-icon>
        Hydrology: Normal Annual Runoff Isolines (1961 - 1990) - Historical (DataBC)
      </v-btn>
    </v-card-actions>
    <v-row class="pl-3 pr-3">
      <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Average annual runoff (by isolines):
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>000000.00 mm</strong>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card flat outlined tile>
          <v-card-title>
            Watershed area
            <v-icon small class="ml-1">mdi-information-outline</v-icon>
          </v-card-title>
          <v-card-text class="info-blue">
            <strong>000000.00 sq. m</strong>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <img src="mockups/monthly_discharge.png" width="700"/>
  </v-card>
</template>

<script>
export default {
  name: 'ComparativeRunoffModels',
  components: {
    // ModelExplanations

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
