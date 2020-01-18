<template>
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
    <input class="disabled-search-placeholder mapboxgl-ctrl-geocoder" disabled placeholder="Choose a type of feature to search for" v-if="searchDisabled"/>
    <div id="geocoder" class="mr-5 geocoder" v-show="!searchDisabled"></div>
  </v-toolbar-items>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'GeocoderSearch',
  data: () => ({
    searchFeatureType: null,
    searchOptions: [
      { text: 'Select search', value: null, placeholder: 'Choose a type of feature to search for', disableSearch: true },
      { text: 'Parcel (PID)', value: 'cadastral', placeholder: 'Search by PID' },
      { text: 'Well tag number', value: 'groundwater_wells', placeholder: 'Search by well tag number' },
      { text: 'Coordinates', value: 'coordinates', placeholder: 'Find a location (example: -123, 51)' },
      { text: 'Water Licences', value: 'water_rights_licences', placeholder: 'Search by licence or file number' },
      { text: 'Aquifers', value: 'aquifers', placeholder: 'Search by aquifer number' },
      { text: 'EcoCat Reports', value: 'ecocat_water_related_reports', placeholder: 'Search by report title' }
    ]
  }),
  computed: {
    searchDisabled () {
      return this.searchOptions.find(x => x.value === this.searchFeatureType).disableSearch || false
    },
    ...mapGetters('map', [
      'geocoder'
    ])
  },
  methods: {
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
    position: relative;
  }
  .mapboxgl-ctrl-geocoder {
    width: 164rem!important;
    min-height: 40px!important;
    border-width: 1px 1px 1px 0px;
    border-style: solid;
    border-color: rgba(0,0,0,.24);
    border-radius: 0px 4px 4px 0px!important;
  }
  .disabled-search-placeholder {
    padding-left: 10px;
    width: 380px!important;
    margin-right: 20px;
  }
  #geocoder {
    z-index: 4;
    position: relative;
  }
</style>
