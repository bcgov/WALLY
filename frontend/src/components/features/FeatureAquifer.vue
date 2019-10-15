<template>
  <v-card elevation=0>
    <v-card-text>
      <div class="grey--text text--darken-4 headline" id="aquiferTitle">{{ record.properties.AQNAME }}</div>
      <div class="grey--text text--darken-2 title mt-0 mb-2">Aquifer</div>
      <v-divider></v-divider>
      <v-list dense class="mx-0 px-0">

        <v-list-item class="feature-content">
          <v-list-item-content>Aquifer name</v-list-item-content>
          <v-list-item-content>{{record.properties.AQNAME}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Litho stratigraphic unit</v-list-item-content>
          <v-list-item-content>{{record.properties.LITHO_STRATOGRAPHIC_UNIT}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Descriptive location</v-list-item-content>
          <v-list-item-content>{{record.properties.DESCRIPTIVE_LOCATION}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Vulnerability</v-list-item-content>
          <v-list-item-content>{{record.properties.VULNERABILITY}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Material type</v-list-item-content>
          <v-list-item-content>{{record.properties.AQUIFER_MATERIALS}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Subtype</v-list-item-content>
          <v-list-item-content>{{record.properties.AQUIFER_SUBTYPE_CODE}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Productivity</v-list-item-content>
          <v-list-item-content>{{record.properties.PRODUCTIVITY}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Size (km²)</v-list-item-content>
          <v-list-item-content>{{(record.properties.FEATURE_AREA_SQM / 1000000).toFixed(1)}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Demand</v-list-item-content>
          <v-list-item-content>{{record.properties.DEMAND}}</v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>Data source:</v-list-item-content>
          <v-list-item-content><a href="https://catalogue.data.gov.bc.ca/dataset/ground-water-aquifers">DataBC Aquifers</a></v-list-item-content>
        </v-list-item>
        <v-list-item class="feature-content">
          <v-list-item-content>
            <a :href="`https://apps.nrs.gov.bc.ca/gwells/aquifers/${Number(record.properties.AQ_TAG)}`" target="_blank">View this aquifer on Groundwater Wells and Aquifers</a>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <section class="mt-5">
        <div class="grey--text text--darken-4 title">
          Water licences associated with this aquifer <a v-if="!isWaterLicencesLayerEnabled" href="#" @click.prevent="enableWaterLicencesLayer" class="caption">(enable Water Rights Licences map layer)</a>
        </div>
        <v-divider></v-divider>
        <v-data-table dense :headers="licenceHeaders" :items="licenceItems" item-key="name" class="mt-3"></v-data-table>
      </section>
      <section class="mt-5">
        <div class="grey--text text--darken-4 title">
          Groundwater wells associated with this aquifer <a v-if="!isWellsLayerEnabled" href="#" @click.prevent="enableWellsLayer" class="caption">(enable Groundwater Wells map layer)</a>
        </div>
        <v-divider></v-divider>
        <v-data-table dense :headers="wellTableHeaders" :items="wellTableItems" item-key="name" class="mt-3"></v-data-table>
      </section>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import ApiService from '../../services/ApiService'

export default {
  name: 'FeatureAquifer',
  props: {
    record: Object
  },
  data () {
    return {
      loading: false,
      aquifer: null,
      licenceHeaders: [
        {
          text: 'Well tag number',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: 'Total yield (US Gal / yr)', value: 'protein' },
        { text: 'Licence date', value: 'carbs' }
      ],
      wellTableHeaders: [
        {
          text: 'Licence number',
          align: 'left',
          sortable: false,
          value: 'name'
        },
        { text: 'Licence (if applicable)', value: 'protein' },
        { text: 'Depth (ft)', value: 'calories' },
        { text: 'Well yield (USGPM)', value: 'fat' },
        { text: 'Last report date', value: 'carbs' }
      ],
      wellTableItems: [
        {
          name: '4332',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%'
        },
        {
          name: '123',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: '1%'
        }
      ],
      licenceItems: [
        {
          name: '4332',
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: '1%'
        },
        {
          name: '123',
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: '1%'
        }
      ]
    }
  },
  computed: {
    id () {
      return this.record.properties.n
    },
    isWellsLayerEnabled () {
      return this.isMapLayerActive('groundwater_wells')
    },
    isWaterLicencesLayerEnabled () {
      return this.isMapLayerActive('water_rights_licences')
    },
    ...mapGetters(['isMapLayerActive'])
  },
  methods: {
    enableWellsLayer () {
      this.$store.commit('addMapLayer', 'groundwater_wells')
    },
    enableWaterLicencesLayer () {
      this.$store.commit('addMapLayer', 'water_rights_licences')
    }
  }
}
</script>

<style>

</style>
