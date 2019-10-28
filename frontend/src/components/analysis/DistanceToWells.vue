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
        </v-data-table>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-expansion-panels class="mt-5 elevation-0" multiple>
          <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header disable-icon-rotate class="grey--text text--darken-4 subtitle-1">
              Where does this information come from?
              <template v-slot:actions>
                <v-icon color="primary">mdi-help-circle-outline</v-icon>
              </template>

            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p>Data on this page comes from <a href="https://apps.nrs.gov.bc.ca/gwells/" target="_blank">Groundwater Wells and Aquifers</a>.</p>
              <dl>
                <dt>Reported yield</dt>
                <dd>Estimated by the well driller during construction by conducting a well yield test. US gallons per minute.</dd>
                <dt>Static water level</dt>
                <dd>The level (from the top of the casing) to which water will naturally rise in a well without pumping, measured in feet (ft btoc).</dd>
                <dt>Top of screen</dt>
                <dd>The depth (from ground level) to the top of the uppermost reported screen segment. This figure is automatically calculated using data provided in construction reports.</dd>
                <dt>Finished well depth</dt>
                <dd>The depth at which the well was 'finished'. It can be shallower from the total well depth which is the total depth at which the well was drilled. The finished depth is represented in units of feet bgl (below ground level).</dd>
                <dt>SWL to top of screen</dt>
                <dd>The distance from the static water level to top of screen (see definition above), in feet.</dd>
                <dt>SWL to bottom of well</dt>
                <dd>The distance from the static water level to the finished well depth (see definition above), in feet.</dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'
import EventBus from '../../services/EventBus'

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
      { text: 'Static water level (ft btoc)', value: 'static_water_level', align: 'right' },
      { text: 'Top of screen (ft bgl)', value: 'top_of_screen', align: 'right' },
      { text: 'Finished well depth (ft bgl)', value: 'finished_well_depth', align: 'right' },
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
    enableWellsLayer () {
      this.$store.commit('addMapLayer', 'groundwater_wells')
    },
    fetchWells: debounce(function () {
      this.showCircle()
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
    },
    showCircle () {
      const options = { steps: 32, units: 'kilometers', properties: { display_data_name: 'user_search_radius' } }
      const radius = this.radius / 1000
      const shape = circle(this.coordinates, radius, options)
      shape.id = 'user_search_radius'

      // remove old shapes
      EventBus.$emit('draw.remove', shape.id)

      // add the new one
      EventBus.$emit('draw:add', shape)
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
