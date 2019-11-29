import { mapGetters } from 'vuex'

import SingleSelectedFeature from './SingleSelectedFeature'
import MultipleSelectedFeatures from './MultipleSelectedFeatures'
import LayerSelection from './LayerSelection'
import InfoSheetAdjustable from '../common/InfoSheetAdjustable'
import InfoSheet from '../common/InfoSheet'

export default {
  name: 'Sidebar',
  components: {
    SingleSelectedFeature,
    MultipleSelectedFeatures,
    LayerSelection,
    InfoSheet,
    InfoSheetAdjustable
  },
  data () {
    return {
    }
  },
  computed: {
    infoSheetComponent () {
      return this.$store.state.feature.adjustableSidePanel ? InfoSheetAdjustable : InfoSheet
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
    panelWidth () {
      if (!this.displayLayerSelection &&
           (this.isSingleSelectedFeature || this.isMultipleSelectedFeatures)) {
        return 850
      }
      return 500
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
