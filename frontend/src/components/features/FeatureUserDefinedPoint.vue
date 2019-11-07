<template>
    <v-card
      class="mx-auto"
    >
      <v-card-text>
        <div>Point</div>
        <p class="display-1 text--primary">
          {{coordinates}}
        </p>
        <p>coordinates</p>
        <div class="text--primary">
          well meaning and kindly.<br>
          "a benevolent smile"
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn
          text
          color="deep-purple accent-4"
          @click="goToDistanceToWells()"
        >
          Find wells near this point
        </v-btn>
        <br/>
        <v-btn
        text
        color="deep-purple accent-4"
        to="/"
      >
        Find streams near this point
      </v-btn>
      </v-card-actions>
    </v-card>
<!--  <v-sheet class="pt-5">-->

<!--    <div class="headline">Point</div>-->
<!--    <dl>-->
<!--      <dt>Coordinates:</dt>-->
<!--      <dl>{{coordinates}}</dl>-->
<!--    </dl>-->
<!--    <v-expansion-panels class="mt-5" multiple>-->
<!--      <v-expansion-panel>-->
<!--        <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">Find wells near this point</v-expansion-panel-header>-->
<!--        <v-expansion-panel-content>-->
<!--          <WellsByDistance :record="record" :coordinates="this.record.geometry.coordinates"></WellsByDistance>-->
<!--        </v-expansion-panel-content>-->
<!--      </v-expansion-panel>-->
<!--      <v-expansion-panel>-->
<!--        <v-expansion-panel-header class="grey&#45;&#45;text text&#45;&#45;darken-4 subtitle-1">Find streams near this point</v-expansion-panel-header>-->
<!--        <v-expansion-panel-content>-->
<!--          <v-row>-->
<!--            <v-col cols="12" md="4">-->
<!--              <v-text-field-->
<!--                label="Search radius (m)"-->
<!--                placeholder="1000"-->
<!--                v-model="radius"-->
<!--              ></v-text-field>-->
<!--            </v-col>-->
<!--          </v-row>-->
<!--        </v-expansion-panel-content>-->
<!--      </v-expansion-panel>-->
<!--    </v-expansion-panels>-->
<!--  </v-sheet>-->
</template>

<script>
import { mapGetters } from 'vuex'
import WellsByDistance from '../analysis/WellsByDistance'
import router from '../../router.js'
export default {
  name: 'FeatureUserDefined',
  components: {
    WellsByDistance
  },
  props: ['record'],
  data: () => ({
    radius: 1000
  }),
  computed: {
    ...mapGetters([
      'dataMartFeatureInfo'
    ]),
    coordinates () {
      // TODO: it's showing as longlat instead of latlong
      console.log(this.record)
      return this.record.geometry.coordinates.map((x) => {
        return x.toFixed(5)
      }).join(', ')
    }
  },
  methods: {
    goToDistanceToWells () {
      router.push('/analysis/wells-by-distance/' + this.coordinates)
    }
  }
}
</script>

<style>

</style>
