<template>
  <v-card>

    <v-card-text>
      <div class="grey--text text--darken-4 title" id="aquiferTitle">Well {{ record.properties.well_tag_number }}</div>
      <div class="grey--text text--darken-2 subtitle-1 mt-0 mb-2">Groundwater well</div>
    <v-divider></v-divider>

      <v-list dense class="mx-0 px-0">
        <v-list-item>
          <v-list-item-content>
            <a :href="`https://apps.nrs.gov.bc.ca/gwells/well/${Number(record.properties.well_tag_number)}`" target="_blank">View this well on Groundwater Wells and Aquifers</a>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Identification plate number</v-list-item-content>
          <v-list-item-content>{{record.properties.identification_plate_number}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Address</v-list-item-content>
          <v-list-item-content>{{record.properties.street_address}} <span v-if="record.properties.city">, {{record.properties.city}}</span></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Intended water use</v-list-item-content>
          <v-list-item-content>{{record.properties.intended_water_use}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Finished well depth</v-list-item-content>
          <v-list-item-content>{{record.properties.finished_well_depth}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Static water level</v-list-item-content>
          <v-list-item-content>{{record.properties.static_water_level}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Well yield</v-list-item-content>
          <v-list-item-content>{{record.properties.yield}} <span v-if="record.properties.yield">{{record.properties.yield_unit}}</span></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Artesian flow</v-list-item-content>
          <v-list-item-content>{{record.properties.artesian_flow}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Artesian pressure</v-list-item-content>
          <v-list-item-content>{{record.properties.artesian_pressure}}</v-list-item-content>
        </v-list-item>
        <!-- NOTE: GWELLS CORS settings only allow api requests from *.gov.bc.ca addresses. This will work on staging/prod,
              needs to be addressed in GWELLS to work locally.
        -->
        <v-list-item>
          <v-list-item-content>Licence status</v-list-item-content>
          <v-list-item-content v-if="well_licence">
            {{well_licence.status}} <span v-if="well_licence.number">({{well_licence.number}})</span>
          </v-list-item-content>
          <v-list-item-content v-else-if="licence_error">Licence status unavailable</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'

export default {
  name: 'WellFeatureCard',
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      well: null,
      well_licence: null,
      licence_error: null
    }
  },
  computed: {
    id () {
      return this.record.properties.well_tag_number
    }
  },
  methods: {
    resetWell () {
      this.well_licence = null
      this.licence_error = null
    },
    fetchLicence () {
      this.loading = true
      this.resetWell()

      ApiService.getRaw(`https://apps.nrs.gov.bc.ca/gwells/api/v1/wells/licensing?well_tag_number=${this.record.properties.well_tag_number}`).then((r) => {
        this.well_licence = r.data
      }).catch((e) => {
        this.licence_error = e
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }
  },
  watch: {
    id () {
      this.fetchLicence()
    }
  },
  mounted () {
    this.fetchLicence()
  }
}
</script>

<style>

</style>
