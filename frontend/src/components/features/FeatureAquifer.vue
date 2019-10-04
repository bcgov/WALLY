<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 title" id="aquiferTitle">{{ record.properties.AQNAME }}</div>
      <div class="grey--text text--darken-2 subtitle-1 mt-0 mb-2">Aquifer</div>
      <v-divider></v-divider>
      <v-list dense class="mx-0 px-0">

        <v-list-item>
          <v-list-item-content>Aquifer name</v-list-item-content>
          <v-list-item-content>{{record.properties.AQNAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Litho stratigraphic unit</v-list-item-content>
          <v-list-item-content>{{record.properties.LITHO_STRATOGRAPHIC_UNIT}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Descriptive location</v-list-item-content>
          <v-list-item-content>{{record.properties.DESCRIPTIVE_LOCATION}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Vulnerability</v-list-item-content>
          <v-list-item-content>{{record.properties.VULNERABILITY}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Material type</v-list-item-content>
          <v-list-item-content>{{record.properties.AQUIFER_MATERIALS}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Subtype</v-list-item-content>
          <v-list-item-content>{{record.properties.AQUIFER_SUBTYPE_CODE}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Productivity</v-list-item-content>
          <v-list-item-content>{{record.properties.PRODUCTIVITY}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Size (km²)</v-list-item-content>
          <v-list-item-content>{{(record.properties.FEATURE_AREA_SQM / 1000000).toFixed(1)}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Demand</v-list-item-content>
          <v-list-item-content>{{record.properties.DEMAND}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Data source:</v-list-item-content>
          <v-list-item-content><a href="https://catalogue.data.gov.bc.ca/dataset/ground-water-aquifers">DataBC Aquifers</a></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <a :href="`https://apps.nrs.gov.bc.ca/gwells/aquifers/${Number(record.properties.AQ_TAG)}`" target="_blank">View this aquifer on Groundwater Wells and Aquifers</a>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'

export default {
  name: 'FeatureAquifer',
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      well: null
    }
  },
  computed: {
    id () {
      return this.record.properties.n
    }
  },
  methods: {
    resetWell () {
      this.well = null
    },
    fetchRecord () {
      this.loading = true
      this.resetWell()

      ApiService.getRaw(`https://apps.nrs.gov.bc.ca/gwells/api/v1/wells/${this.record.properties.n}`).then((r) => {
        this.well = r.data
      }).catch((e) => {
        this.error = e
        console.error(e)
      }).finally(() => {
        this.loading = false
      })
    }
  },
  watch: {
    id () {
      // this.fetchRecord()
    }
  },
  mounted () {
    // this.fetchRecord()
  }
}
</script>

<style>

</style>
