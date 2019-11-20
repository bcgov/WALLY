<template>
  <v-container class="pa-0 ma-0">
    <v-row no-gutters>
      <v-col cols="12" md="4" align-self="center">
        <v-text-field
          label="Search radius (m)"
          placeholder="1000"
          :rules="[inputRules.number, inputRules.max, inputRules.required]"
          v-model="radius"
        ></v-text-field>
      </v-col>
      <v-col cols="12" offset-md="1" md="4" align-self="center" v-if="!isLicencesLayerEnabled">
        <div class="caption"><a href="#" @click.prevent="enableLicencesLayer">Enable water rights licences map layer</a></div>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.POD" class="mx-2" :label="`POD (${subtypeCounts.POD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.PWD" class="mx-2" :label="`PWD (${subtypeCounts.PWD})`"></v-checkbox>
      </v-col>
      <v-col cols="12" md="4">
        <v-checkbox v-model="tableOptions.subtypes.PG" class="mx-2" :label="`PG (${subtypeCounts.PG})`"></v-checkbox>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <v-checkbox v-model="tableOptions.applications" class="mx-2" :label="`Water Rights Applications (${applicationCount})`"></v-checkbox>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-data-table
          :loading="loading"
          :headers="headers"
          :items="filteredLicences"
        >
          <template v-slot:item.distance="{ item }">
            <span>{{item.distance.toFixed(1)}}</span>
          </template>
          <template v-slot:item.QUANTITY="{ item }">
            <span v-if="item.QUANTITY" >{{item.QUANTITY.toFixed(3)}} {{item.QUANTITY_UNITS}}</span>
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
              <p>Data on this page comes from <a href="https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public" target="_blank">Water Rights Licences (public)</a>.</p>
              <dl>
                <dt>Licence number</dt>
                <dd>Licence number is the authorization number referenced in the water licence document, e.g., 121173.</dd>
                <dt>POD number</dt>
                <dd>POD number is the unique identifier for a Point of Diversion, e.g., PW189413. Each POD can have multiple licences associated with it.</dd>
                <dt>Purpose use</dt>
                <dd>Purpose use is the use of water authorized by the licence, e.g. Industrial.</dd>
                <dt>Quantity</dt>
                <dd>Quantity is the maximum quantity of water that is authorized to be diverted for the purpose use, e.g., 500 m3/day.</dd>
                <dt>POD subtype</dt>
                <dd>
                  POD subtype distinguishes the different POD types, i.e., POD (a surface water point of diversion), PWD (a point of well diversion that diverts groundwater),
                  or PG (a point of groundwater diversion that diverts groundwater such as a dugout, ditch or quarry).
                </dd>
              </dl>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import qs from 'querystring'
import ApiService from '../../services/ApiService'
import debounce from 'lodash.debounce'
import circle from '@turf/circle'
import EventBus from '../../services/EventBus'

export default {
  name: 'WaterRightsLicencesNearby',
  props: ['record'],
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
      { text: 'Distance', value: 'distance', align: 'right' },
      { text: 'Application status', value: 'APPLICATION_STATUS', align: 'right' },
      { text: 'Application number', value: 'APPLICATION_JOB_NUMBER', align: 'right' },
      { text: 'Licence number', value: 'LICENCE_NUMBER', align: 'right' },
      { text: 'POD number', value: 'POD_NUMBER', align: 'right' },
      { text: 'POD subtype', value: 'POD_SUBTYPE', align: 'right', filterable: true },
      { text: 'Purpose use', value: 'PURPOSE_USE' },
      { text: 'Quantity', value: 'QUANTITY', align: 'right' }
    ],
    tableOptions: {
      applications: true,
      subtypes: {
        PWD: true,
        POD: true,
        PG: true
      }

    }
  }),
  computed: {
    isLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    coordinates () {
      return this.record.geometry.coordinates
    },
    filteredLicences () {
      let licences = this.results

      const subtypes = this.tableOptions.subtypes

      // loop through subtypes in tableOptions and if any subtype is disabled (false value),
      // filter it out of the licences array.
      for (const key of Object.keys(subtypes)) {
        // check if this subtype key is disabled.
        if (!subtypes[key]) {
          licences = licences.filter(x => x.POD_SUBTYPE !== key)
        }
      }

      if (!this.tableOptions.applications) {
        licences = licences.filter(x => !x.APPLICATION_JOB_NUMBER)
      }

      return licences
    },
    applicationCount () {
      return this.results.filter(x => !!x.APPLICATION_JOB_NUMBER).length
    },
    subtypeCounts () {
      // counts each subtype in the results
      let licences = this.results
      const subtypes = this.tableOptions.subtypes

      let counts = {}

      // loop through the subtypes, and count the number of each type.
      for (const key of Object.keys(subtypes)) {
        counts[key] = licences.filter(x => x.POD_SUBTYPE === key).length
      }
      return counts
    },
    ...mapGetters(['isMapLayerActive'])
  },
  methods: {
    enableLicencesLayer () {
      this.$store.commit('addMapLayer', 'water_rights_licences')
      this.$store.commit('addMapLayer', 'water_rights_applications')
    },
    fetchLicences: debounce(function () {
      this.showCircle()
      this.loading = true
      if (!this.radiusIsValid(this.radius)) {
        return
      }

      const params = {
        radius: parseFloat(this.radius),
        point: JSON.stringify(this.coordinates)
      }
      ApiService.query(`/api/v1/analysis/licences/nearby?${qs.stringify(params)}`).then((r) => {
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
      EventBus.$emit('shapes:reset')

      // add the new one
      EventBus.$emit('shapes:add', shape)
    }
  },
  watch: {
    record: {
      handler () {
        this.fetchLicences()
      },
      deep: true
    },
    coordinates () {
      this.fetchLicences()
    },
    radius (value) {
      this.fetchLicences()
    }
  },
  mounted () {
    this.fetchLicences()
  },
  beforeDestroy () {
    EventBus.$emit('shapes:reset')
  }
}
</script>

<style>

</style>
