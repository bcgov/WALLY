import { mapGetters } from 'vuex'

import SingleSelectedFeature from './SingleSelectedFeature'
import MultipleSelectedFeatures from './MultipleSelectedFeatures'
import LayerSelection from './LayerSelection'

export default {
  name: 'Sidebar',
  components: {
    SingleSelectedFeature,
    MultipleSelectedFeatures,
    LayerSelection
  },
  data () {
    return {
    }
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
