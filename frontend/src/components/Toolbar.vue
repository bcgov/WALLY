<template>
  <div>
    <v-toolbar fixed class="wally-toolbar" short>
      <v-toolbar-items class="py-2">
        <v-btn
          color="primary"
          @click.prevent="handleLayerSelectionState"
          :outlined="$route.name !== 'layer-selection'"
          width=128
        ><v-icon>layers</v-icon> Layers</v-btn>
      </v-toolbar-items>

      <div class="flex-grow-1"></div>
      <v-toolbar-items class="py-2">
          <v-select
            v-model="searchFeatureType"
            :items="searchOptions"
            outlined
            dense
            single-line
            color="primary"
            label="Filter by"
            class="search-types-select">
          </v-select>
        <div id="geocoder" class="mr-5 geocoder"></div>
      </v-toolbar-items>
    </v-toolbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Toolbar',
  data: () => ({
    searchFeatureType: null,
    searchOptions: [
      { text: 'All', value: null, placeholder: 'Search' },
      { text: 'Wells', value: 'groundwater_wells', placeholder: 'Search by well tag number' },
      { text: 'Water Licences', value: 'water_rights_licences', placeholder: 'Search by licence number or source name' },
      { text: 'Aquifers', value: 'aquifers', placeholder: 'Search by aquifer number' },
      { text: 'EcoCat Reports', value: 'ecocat_water_related_reports', placeholder: 'Search by report title' }
    ]
  }),
  computed: {
    ...mapGetters([
      'layerSelectionActive',
      'singleSelectionFeatures',
      'featureSelectionExists',
      'geocoder'
    ])
  },
  methods: {
    handleLayerSelectionState () {
      // if (!this.featureSelectionExists) {
      //   return this.$store.commit('setLayerSelectionActiveState', true)
      // }
      this.$store.commit('setLayerSelectionActiveState', !this.layerSelectionActive)

      if (this.$route.name === 'layer-selection') {
        return this.$router.go(-1)
      }
      return this.$router.push('/layers')
    },
    updateGeocoderType (featureType) {
      // update the search types (e.g. wells, aquifers etc) to be passed to the geocoder
      // component.
      // note: countries is the only option that can accept custom types.  the `types`
      // option is limited to place, poi, address etc.  This is intended to be
      // temporary to get feedback on whether this functionality will work for our users.
      this.geocoder.options.countries = featureType
    }
  },
  watch: {
    searchFeatureType (val) {
      this.updateGeocoderType(val)

      // find and update the the geocoder search box by its class name.
      const searchInput = document.getElementsByClassName('mapboxgl-ctrl-geocoder--input')
      if (searchInput) {
        searchInput[0].value = ''

        // set a contextual placeholder based on the search feature type
        searchInput[0].placeholder = this.searchOptions.find(opt => {
          return opt.value === val
        }).placeholder || 'Search'
      }
    }
  }
}
</script>

<style>
  .search-types-select {
    width: 12rem;
    border-radius: 4px 0px 0px 4px!important;
    border-width: 1px 1px 1px 0px;
  }
  .wally-toolbar {
    box-shadow: inset 0 -1px 0 grey;
    z-index: 3;
  }
  .mapboxgl-ctrl-geocoder {
    width: 164rem!important;
    min-height: 40px!important;
    border-width: 1px 1px 1px 0px;
    border-style: solid;
    border-color: rgba(0,0,0,.24);
    border-radius: 0px 4px 4px 0px!important;
  }
  #geocoder {
    z-index: 4;
  }
</style>
