<template>
  <div>
    <v-row>
      <v-col cols="12" md="4" align-self="center">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isWellsLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableWellsLayer">Enable groundwater wells map layer</a></div>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :loading="loading"
          :headers="headers"
          :items="results"
        >
          <template v-slot:item.distance="{ item }">
            <span>{{item.distance.toFixed(1)}}</span>
          </template>
          <template v-slot:item.top_of_screen="{ item }">
            <span>{{calculateTopOfScreens(item.screen_set)}}</span>
          </template>
          <template v-slot:item.swl_to_screen="{ item }">
            <span v-if="item.screen_set && item.screen_set.length && item.static_water_level">
              {{ calculateTopOfScreens(item.screen_set) - Number(item.static_water_level) }}
            </span>
          </template>
          <template v-slot:item.swl_to_bottom_of_well="{ item }">
            <span v-if="item.finished_well_depth && item.static_water_level">
              {{  Number(item.finished_well_depth) - Number(item.static_water_level) }}
            </span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'

export default {
  name: 'DistanceToWells',
  props: ['record', 'coordinates'],
  data: () => ({
    inputRules: {
      required: value => !!value || 'Required',
      number: value => !Number.isNaN(parseFloat(value)) || 'Invalid number',
      max: value => value <= 10000 || 'Radius must be between 0 and 10000 m'
    },
    radius: 1000,
    results: [],
    loading: false,
    headers: [
      { text: 'Well tag number', value: 'well_tag_number', align: 'right' },
      { text: 'Distance (m)', value: 'distance', align: 'right' },
      { text: 'Reported yield (USGPM)', value: 'well_yield', align: 'right' },
      { text: 'Static water level (ft)', value: 'static_water_level', align: 'right' },
      { text: 'Top of screen (ft)', value: 'top_of_screen', align: 'right' },
      { text: 'Finished well depth (ft)', value: 'finished_well_depth', align: 'right' },
      { text: 'SWL to top of screen (ft)', value: 'swl_to_screen', align: 'right' },
      { text: 'SWL to bottom of well (ft)', value: 'swl_to_bottom_of_well', align: 'right' }

    ]
  }),
  computed: {
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    ...mapGetters(['isMapLayerActive'])
  },
  methods: {
    calculateTopOfScreens (screenSet) {
      console.log(screenSet)
      if (!screenSet || !screenSet.length) {
        return null
      }
      // get the "top" value of all the screens and return the minimum.
      // explicitly check against "null" here because 0 is a valid value,
      // but we may see "null" from time to time.
      const screenTops = screenSet.map((x) => x.start).filter((x) => x !== null && x !== undefined)
      console.log(screenTops)
      return Math.min(...screenTops)
    },
    enableWellsLayer () {
      this.$store.commit('addMapLayer', 'groundwater_wells')
    },
    fetchWells: debounce(function () {
      this.loading = true
      if (!this.radiusIsValid(this.radius)) {
        return
      }

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/wells/nearby?${qs.stringify(params)}`).then((r) => {
        this.results = r.data
      }).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }, 500),
    radiusIsValid (val) {
      let invalid = Object.keys(this.inputRules).some((k) => {
        return this.inputRules[k](val) !== true
      })
      return !invalid
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchWells()
      },
      deep: true
    },
    coordinates () {
      this.fetchWells()
    },
    radius (value) {
      this.fetchWells()
    }
  },
  mounted () {
    this.fetchWells()
  }
}
</script>

<style>

</style>
