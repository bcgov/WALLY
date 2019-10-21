<template>
  <div>
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

      <v-list v-if="!loadingFeature">
        <template v-for="(value, name, index) in getHighlightProperties(dataMartFeatureInfo)">
          <v-hover v-slot:default="{ hover }" v-bind:key="`item-{$value}${index}`">
            <v-card
              class="pl-3 mb-2 pt-2 pb-2"
              :elevation="hover ? 12 : 2"
            >
              <span><b>{{ humanReadable(name) }}: </b></span>
              <span>{{ value }}</span>
            </v-card>
          </v-hover>
          <v-divider :key="`divider-${index}`"></v-divider>
        </template>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import EventBus from '../../services/EventBus'

import StreamStation from '../features/FeatureStreamStation'
import Well from '../features/FeatureWell'
import Aquifer from '../features/FeatureAquifer'
import EcoCat from '../features/FeatureEcocat'

export default {
  name: 'SingleSelectedFeature',
  components: {
    StreamStation,
    Well,
    EcoCat,
    Aquifer
  },
  props: {

  },
  data: () => ({
    featureComponents: {
      hydrometric_stream_flow: StreamStation,
      aquifers: Aquifer,
      groundwater_wells: Well,
      ecocat_water_related_reports: EcoCat
    }
  }),
  computed: {
    ...mapGetters([
      'loadingFeature',
      'featureError',
      'getMapLayer',
      'dataMartFeatureInfo',
      'singleSelectionFeatures'
    ])
  },
  methods: {
    handleCloseSingleFeature () {
      this.$store.commit('resetDataMartFeatureInfo')
      EventBus.$emit('highlight:clear')
    },
    humanReadable: (val) => humanReadable(val),
    getHighlightProperties (info) {
      let layer = this.getMapLayer(info.display_data_name)
      if (layer != null) {
        let highlightFields = layer.highlight_columns
        let obj = {}
        highlightFields.forEach((field) => {
          obj[field] = info.properties[field]
        })
        return obj
      }
      return {}
    }
  }
}
</script>

<style>

</style>
