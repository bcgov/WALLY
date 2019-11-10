<template>
  <div>
    <v-toolbar flat>
      <v-banner color="indigo"
                icon="mdi-map-marker"
                icon-color="white"
                width="100%"
      >
      <v-toolbar-title>
        Point Coordinates
      </v-toolbar-title>
        {{coordinates}}
      </v-banner>
    </v-toolbar>
    <v-row class="pt-10">
      <v-col v-for="(item, i) in this.analysisItems" v-bind:key="i">
        <v-card tile outlined>
          <v-card-actions v-for="(action, j) in item.actions" v-bind:key="j">
            <v-btn
              text
              color="indigo accent-4"
              @click="goToAnalysis(action.analysis)"
            >
             {{action.text}}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import router from '../../router.js'

export default {
  name: 'FeatureUserDefined',
  props: ['record'],
  data: () => ({
    radius: 1000,
    analysisItems: [
      {
        layer: 'Groundwater Wells',
        actions: [
          {
            text: 'Find wells near this point',
            analysis: 'wellsByDistance'
          }
        ]
      },
      {
        layer: 'Water Licences',
        actions: [
          {
            text: 'Find water licences near this point',
            analysis: 'wellsByDistance'
          }
        ]
      }
    ]
  }),
  computed: {
    ...mapGetters([
      'dataMartFeatureInfo'
    ]),
    coordinates () {
      // TODO: it's showing as longlat instead of latlong
      return this.record.geometry.coordinates.map((x) => {
        return x.toFixed(5)
      }).join(', ')
    }
  },
  methods: {
    goToAnalysis(analysis) {
      switch (analysis) {
        case 'wellsByDistance':
          router.push('/analysis/wells-by-distance/' + this.coordinates)
      }
    }
  }
}
</script>

<style>

</style>
