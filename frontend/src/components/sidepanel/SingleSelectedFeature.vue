<template>
  <v-container>
    <div v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name">
      <v-row>
        <v-col cols=2>
          <v-btn
            fab
            class="elevation-1"
            small
            id="closeSingleSelectedFeature"
            @click="handleCloseSingleFeature"
          ><v-icon>arrow_back</v-icon></v-btn>
        </v-col>
      </v-row>

      <!-- custom components for features with visualizations etc. -->
      <component
        v-if="dataMartFeatureInfo && Object.keys(featureComponents).includes(dataMartFeatureInfo.display_data_name)"
        :is="featureComponents[dataMartFeatureInfo.display_data_name]"
        :record="dataMartFeatureInfo"
      />

      <!-- fallback generic feature panel for layers that do not have a custom component. Data displayed will be from
          the "highlight_columns" field of the layer catalogue.
        -->
      <v-card v-else>
        <v-card-title class="subheading font-weight-bold">{{ humanReadable(dataMartFeatureInfo.display_data_name) }}</v-card-title>

        <v-divider></v-divider>

        <div v-if="featureError != ''" class="mx-3 mt-5">
          <v-alert
            border="right"
            colored-border
            type="warning"
            elevation="2"
          >
            {{featureError}}
          </v-alert>
        </div>

        <div v-if="loadingFeature">
          <template v-for="n in 10">
            <v-skeleton-loader type="list-item" v-bind:key="`${n}-item`"/><v-divider v-bind:key="`${n}-divider`"/>
          </template>
        </div>

      <v-card-text v-if="!loadingFeature">
        <v-list dense class="mx-0 px-0">
          <template v-for="(value, name, index) in getHighlightProperties(dataMartFeatureInfo)">
            <v-list-item :key="`featureProperty${index}`">
              <v-list-item-content>{{ humanReadable(name) }}</v-list-item-content>
              <v-list-item-content>{{ value }}</v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-card-text>
    </v-card>
    <FeatureAnalysis
      v-if="pointOfInterest"
      :record="pointOfInterest"></FeatureAnalysis>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

import { humanReadable } from '../../common/helpers'

import FeatureStreamStation from '../features/FeatureStreamStation'
import FeatureWell from '../features/FeatureWell'
import FeatureAquifer from '../features/FeatureAquifer'
import FeatureLicence from '../features/FeatureLicence'
import FeatureEcocat from '../features/FeatureEcocat'
import UserDefinedPoint from '../features/FeatureUserDefinedPoint'
import UserDefinedLine from '../features/FeatureUserDefinedLine'
import FeatureCommunityLocation from '../features/FeatureCommunityLocation'
import FeatureAnalysis from '../analysis/FeatureAnalysis'

export default {
  name: 'SingleSelectedFeature',
  components: {
    FeatureStreamStation,
    FeatureWell,
    FeatureEcocat,
    FeatureAquifer,
    FeatureLicence,
    UserDefinedPoint,
    UserDefinedLine,
    FeatureAnalysis,
    FeatureCommunityLocation
  },
  props: {

  },
  data: () => ({
    featureComponents: {
      hydrometric_stream_flow: FeatureStreamStation,
      aquifers: FeatureAquifer,
      water_rights_licences: FeatureLicence,
      groundwater_wells: FeatureWell,
      ecocat_water_related_reports: FeatureEcocat,
      point_of_interest: UserDefinedPoint,
      user_defined_line: UserDefinedLine,
      fn_community_locations: FeatureCommunityLocation
    }
  }),
  computed: {
    ...mapGetters('map', [
      'getMapLayer',
      'map',
      'isMapReady'
    ]),
    ...mapGetters([
      'loadingFeature',
      'featureError',
      'singleSelectionFeatures',
      'dataMartFeatureInfo',
      'pointOfInterest'
    ])
  },
  watch: {
    isMapReady (value) {
      if (value) {
        this.loadFeature()
      }
    }
  },
  methods: {
    handleCloseSingleFeature () {
      // close the feature panel and reset the feature stored in dataMartStore.
      // if this is a drawn point, send the event to clear the user selections.
      if (this.dataMartFeatureInfo.display_data_name === 'point_of_interest') {
        this.$store.commit('map/replaceOldFeatures', null)
      }
      this.$store.commit('resetDataMartFeatureInfo')
      this.$store.dispatch('map/clearHighlightLayer')

      if (this.$store.getters.dataMartFeatures && this.$store.getters.dataMartFeatures.length) {
        this.$router.push({ name: 'multiple-features' })
      }
    },
    humanReadable: (val) => humanReadable(val),
    getHighlightProperties (info) {
      const layer = this.getMapLayer(info.display_data_name)
      if (layer != null) {
        const highlightFields = layer.highlight_columns
        const obj = {}
        highlightFields.forEach((field) => {
          obj[field] = info.properties[field]
        })
        return obj
      }
      return {}
    },
    loadFeature () {
      if ((!!this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name) || !this.$route.query.location) {
        // feature already exists
        return
      }

      const coordinates = this.$route.query.location.split(',').map((x) => Number(x))
      const data = {
        coordinates,
        layerName: this.$route.query.layer
      }

      if (this.$route.query.layer === 'point_of_interest') {
        this.$store.dispatch('map/addFeaturePOIFromCoordinates', data)
      } else {
        this.$router.push('/')
      }
    }
  },
  mounted () {
  }
}
</script>

<style>

</style>
