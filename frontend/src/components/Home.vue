<template>
  <div class="home">
    <v-row no-gutters>
      <v-col order="1" order-md="0" cols="12" :md="panelWidth">
        <Sidebar></Sidebar>
      </v-col>
      <v-col order="0" order-md="1" cols="12" :md="12 - panelWidth">
        <Map></Map>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Map from '../components/map/Map.vue'
import Sidebar from '../components/sidebar/Sidebar.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'Home',
  components: {
    Map,
    Sidebar
  },
  computed: {
    displayLayerSelection () {
      // determines whether or not layer selection should be displayed.
      // this function allows a mix of both user action (clicking on Layers button)
      // and automatic (there's nothing else to display after clearing selections etc.
      // so default to layer select)

      // return true if either layer selection has been manually activated, or if there are no
      // features selected
      return this.layerSelectionActive || !this.featureSelectionExists
    },
    panelWidth () {
      if (!this.displayLayerSelection &&
           (this.isSingleSelectedFeature || this.isMultipleSelectedFeatures)) {
        return 5
      }
      return 4
    },
    panelName () {
      if (this.displayLayerSelection) {
        return 'Layers'
      } else if (this.isSingleSelectedFeature) {
        return 'Feature Info'
      } else if (this.isMultipleSelectedFeatures) {
        return 'Analysis'
      } else {
        return 'Expand'
      }
    },
    isSingleSelectedFeature () {
      return this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name
    },
    isMultipleSelectedFeatures () {
      return this.dataMartFeatures && this.dataMartFeatures.length
    },
    // isEmptySelection () {
    //   return !this.isSingleSelection && !this.isMultipleSelection
    // },
    // isSingleUserDefinedPointSelection () {
    //   return this.isSingleSelection && this.dataMartFeatureInfo.display_data_name === 'user_defined_point'
    // },
    // isSingleSelection () {
    //   return this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name !== undefined
    // },
    // isMultipleSelection () {
    //   return this.dataMartFeatures && this.dataMartFeatures.length > 0 &&
    //     this.dataMartFeatureInfo.display_data_name === undefined
    // },

    ...mapGetters([
      'isMapLayerActive',
      'isDataMartActive',
      'loadingFeature',
      'featureError',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'selectionBoundingBox',
      'getCategories',
      'layerSelectionActive',
      'singleSelectionFeatures',
      'loadingMultipleFeatures',
      'featureSelectionExists'
    ])
  }
}
</script>
<style lang="scss">
.home {
  height: calc(100vh - 120px);
}
.content-wrap {
  width: 100%;
  height: calc(100vh - 120px);
}

.content-panel {
  overflow: auto;
  height: calc(100vh - 120px);

}
/* Custom animations for router-view transitions */
.expand-x-enter, .expand-x-leave-to {
  width: 0;
}
$expand-transition: "width 1s ease-in-out, opacity 03s ease 0.5s";
.expand-x-enter-active, .expand-x-leave-active {
  -webkit-transition: $expand-transition;
  -moz-transition: $expand-transition;
  -o-transition: $expand-transition;
  transition: $expand-transition;
  transition-duration: 0.3s;
  overflow: hidden;
}
.expand-x-enter-to, .expand-x-leave { width: 100%; }
</style>
