<template>
  <div id="app-overlay">
    <InfoSheetAdjustable :panelName=this.panelName>
      <router-view></router-view>
    </InfoSheetAdjustable>
  </div>
</template>
<style lang="scss">
  #app-overlay{
  }
</style>
<script>
import { mapGetters } from 'vuex'
import InfoSheet from './InfoSheetResponsive'
import InfoSheetAdjustable from './InfoSheetAdjustable'
import MapLayers from '../map/MapLayers'
import SingleSelectedFeature from '../sidebar/SingleSelectedFeature'
import MultipleSelectedFeatures from '../sidebar/MultipleSelectedFeatures'

export default {
  name: 'Overlay',
  components: {
    InfoSheetAdjustable
  },
  props: {
  },
  data: () => {
    return {
      // panelWidth: 500
    }
  },
  computed: {
    ...mapGetters('map', [
      'isMapLayerActive',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'getCategories',
      'layerSelectionActive'

    ]),
    ...mapGetters([
      'isDataMartActive',
      'loadingFeature',
      'featureError',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'selectionBoundingBox',
      'singleSelectionFeatures',
      'loadingMultipleFeatures',
      'featureSelectionExists'
    ]),
    panelName () {
      if (this.displayLayerSelection) {
        return 'Layers'
      } else if (this.isSingleSelectedFeature) {
        return 'Feature Info'
      } else if (this.isMultipleSelectedFeatures) {
        return 'Features'
      }
      return 'Expand'
    },
    panelWidth () {
      if (this.displayLayerSelection) {
        return 500
      }
      return 800
    },
    infoSheetComponent () {
      return this.$store.state.feature.adjustableSidePanel ? InfoSheetAdjustable : InfoSheet
    },
    isFlexBoxComponent () {
      return !this.$store.state.feature.adjustableSidePanel
    },
    displayLayerSelection () {
      // determines whether or not layer selection should be displayed.
      // this function allows a mix of both user action (clicking on Layers button)
      // and automatic (there's nothing else to display after clearing selections etc.
      // so default to layer select)

      // return true if either layer selection has been manually activated, or if there are no
      // features selected
      return this.layerSelectionActive || !this.featureSelectionExists
    },
    isSingleSelectedFeature () {
      return this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name
    },
    isMultipleSelectedFeatures () {
      return this.dataMartFeatures && this.dataMartFeatures.length
    },
    currentComponent () {
      if (this.displayLayerSelection) {
        // this.panelWidth = 500
        return MapLayers
      } else if (this.isSingleSelectedFeature) {
        // this.panelWidth = 800
        return SingleSelectedFeature
      } else if (this.isMultipleSelectedFeatures) {
        // this.panelWidth = 800
        return MultipleSelectedFeatures
      }
      return null
    }
  },
  mounted () {
  },
  methods: {
  }
}
</script>
