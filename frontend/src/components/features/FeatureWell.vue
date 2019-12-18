<template>
  <v-card elevation=0 v-if="!wellLoading && well">

    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="aquiferTitle">Well {{ well.well_tag_number }}</div>
      <div class="grey--text text--darken-2 title">Groundwater well</div>
    <v-divider></v-divider>

      <v-list dense class="mx-0 px-0">
        <v-list-item class="feature-content">
          <v-list-item-content>Identification plate number</v-list-item-content>
          <v-list-item-content>{{well.identification_plate_number}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Address</v-list-item-content>
          <v-list-item-content>{{`${well.address || ''}${addressAndStreetProvided ? ', ' : ''}${well.SITE_AREA || ''}` }}</v-list-item-content>
        </v-list-item>

<!-- NOTE: this is commented because these fields are available from GWELLS but aren't currently on
  the DataBC set.  We should switch to GWELLS own data asap and use the following data in this component:
 -->

        <v-list-item>
          <v-list-item-content>Intended water use</v-list-item-content>
          <v-list-item-content>{{well.intended_water_use}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Finished well depth</v-list-item-content>
          <v-list-item-content>{{well.finished_well_depth}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Static water level</v-list-item-content>
          <v-list-item-content>{{well.static_water_level}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Well yield</v-list-item-content>
          <v-list-item-content>{{well.yield}} <span v-if="well.yield">{{well.yield_unit}}</span></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Artesian flow</v-list-item-content>
          <v-list-item-content>{{well.artesian_flow}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Artesian pressure</v-list-item-content>
          <v-list-item-content>{{well.artesian_pressure}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Licence status</v-list-item-content>
          <v-list-item-content>
            {{well.licenced_status}}
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Data source:</v-list-item-content>
          <v-list-item-content><a href="https://apps.nrs.gov.bc.ca/gwells/" target="_blank">Groundwater Wells and Aquifers</a></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <a :href="`https://apps.nrs.gov.bc.ca/gwells/well/${id}`" target="_blank">View this well on Groundwater Wells and Aquifers</a>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import ApiService from '../../services/ApiService'

export default {
  name: 'FeatureWell',
  props: {
    record: Object
  },
  data () {
    return {
      licenceLoading: false,
      wellLoading: false,
      well: {},
      well_licence: null,
      licence_error: null,
      wellError: null
    }
  },
  computed: {
    id () {
      return this.record.properties.well_tag_number
    },
    addressAndStreetProvided () {
      // returns true if both address and street were provided.  helpful for placing a comma between them
      // or displaying them one by one if only one was given.
      return this.well &&
        this.well.street_address &&
        this.well.city
    }
  },
  methods: {
    resetWell () {
      this.well = {}
      this.well_licence = null
      this.licence_error = null
    },
    fetchWell () {
      this.wellLoading = true
      ApiService.getRaw(`https://gwells-dev-pr-1495.pathfinder.gov.bc.ca/gwells/api/v1/wells/${this.id}`).then((r) => {
        this.well = r.data
      }).catch((e) => {
        this.wellError = e
      }).finally(() => {
        this.wellLoading = false
      })
    },
    fetchLicence () {
      this.licenceLoading = true

      ApiService.getRaw(`https://gwells-dev-pr-1495.pathfinder.gov.bc.ca/gwells/api/v1/wells/licensing?well_tag_number=${this.id}`).then((r) => {
        this.well_licence = r.data
      }).catch((e) => {
        this.licence_error = e
        // avoid an error popup here as this is just one section of data
      }).finally(() => {
        this.licenceLoading = false
      })
    }
  },
  watch: {
    id () {
      this.resetWell()
      this.fetchWell()
      this.fetchLicence()
    }
  },
  mounted () {
    this.resetWell()
    this.fetchWell()
    this.fetchLicence()
  }
}
</script>

<style>
</style>
