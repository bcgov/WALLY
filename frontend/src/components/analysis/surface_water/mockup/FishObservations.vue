<template>
  <v-card flat>
    <v-card-title
      class="title mt-5 ml-3 mr-3 pa-1 mb-2"
      dark>
      Watershed Fish Observations
    </v-card-title>
    <v-card-actions>
      <v-card-subtitle class="pr-0 pl-2">
        Source

      </v-card-subtitle>
      <v-btn v-on="on" small  depressed light class="ml-2"
             href="https://catalogue.data.gov.bc.ca/dataset/known-bc-fish-observations-and-bc-fish-distributions">

        <v-icon small>
          mdi-link-variant
        </v-icon>
        Known BC Fish Observations and BC Fish Distributions (DataBC)
      </v-btn>
    </v-card-actions>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="items"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <h4>Watershed Fish Observations</h4>
          </v-toolbar>
        </template>
      </v-data-table>
    </v-card>
  </v-card>
</template>

<script>
export default {
  name: 'FishObservations',
  components: {
  },
  data: () => ({
    headers: [
      {
        text: 'Fish Species',
        value: 'fishSpecies'
      },
      {
        text: 'Observation Count',
        value: 'observationCount'
      },
      {
        text: 'Life Stages Observed',
        value: 'lifeStagesObserved'
      },
      {
        text: 'First Observation Date',
        value: 'firstObsDate'
      },
      {
        text: 'Last Observation Date',
        value: 'lastObsDate'
      }
    ],
    items: [
      {
        fishSpecies: 'Cutthroat Trout',
        observationCount: 1,
        lifeStagesObserved: '',
        firstObsDate: 'yyyy-mm-dd',
        lastObsDate: 'yyyy-mm-dd'
      },
      {
        fishSpecies: 'Steelhead',
        observationCount: 1,
        lifeStagesObserved: '',
        firstObsDate: 'yyyy-mm-dd',
        lastObsDate: 'yyyy-mm-dd'
      },
      {
        fishSpecies: 'Coho Salmon',
        observationCount: 1,
        lifeStagesObserved: '',
        firstObsDate: 'yyyy-mm-dd',
        lastObsDate: 'yyyy-mm-dd'
      }
    ]
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
