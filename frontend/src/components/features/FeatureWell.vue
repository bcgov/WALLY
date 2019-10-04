<template>
  <v-card elevation=0>

    <v-card-text>
      <div class="grey--text text--darken-4 title" id="aquiferTitle">Well {{ record.properties.WELL_TAG_NUMBER }}</div>
      <div class="grey--text text--darken-2 subtitle-1 mt-0 mb-2">Groundwater well</div>
    <v-divider></v-divider>

      <v-list dense class="mx-0 px-0">
        <v-list-item>
          <v-list-item-content>Identification plate number</v-list-item-content>
          <v-list-item-content>{{record.properties.WELL_IDENTIFICATION_PLATE_NO}}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Address</v-list-item-content>
          <v-list-item-content>{{`${record.properties.SITE_STREET || ''}${addressAndStreetProvided ? ', ' : ''}${record.properties.SITE_AREA || ''}` }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Well use</v-list-item-content>
          <v-list-item-content>{{record.properties.WELL_USE_NAME}}</v-list-item-content>
        </v-list-item>
<!-- NOTE: this is commented because these fields are available from GWELLS but aren't currently on
  the DataBC set.  We should switch to GWELLS own data asap and use the following data in this component:
 -->

        <!-- <v-list-item>
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
        </v-list-item> -->

        <v-list-item>
          <v-list-item-content>Licence status</v-list-item-content>
          <v-list-item-content>
            {{record.properties.WELL_LICENCE_GENERAL_STATUS}}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Data source:</v-list-item-content>
          <v-list-item-content><a href="https://catalogue.data.gov.bc.ca/dataset/ground-water-wells">DataBC Groundwater Wells</a></v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <a :href="record.properties.WELL_DETAIL_URL" target="_blank">View this well on Groundwater Wells and Aquifers</a>
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
      loading: false,
      well: null,
      well_licence: null,
      licence_error: null
    }
  },
  computed: {
    id () {
      return this.record.properties.WELL_ID
    },
    addressAndStreetProvided () {
      // returns true if both address and street were provided.  helpful for placing a comma between them
      // or displaying them one by one if only one was given.
      return this.record &&
        this.record.properties &&
        this.record.properties.SITE_STREET &&
        this.record.properties.SITE_AREA
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

      ApiService.getRaw(`https://apps.nrs.gov.bc.ca/gwells/api/v1/wells/licensing?well_tag_number=${this.id}`).then((r) => {
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
