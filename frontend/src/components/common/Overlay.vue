<template>
  <div id="app-overlay" v-if="this.showOverlay">
    <InfoSheetAdjustable :panelName=this.panelName>
      <router-view></router-view>
    </InfoSheetAdjustable>
    <div class="draggableBorder" v-show="true"></div>
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
      if (this.isSingleSelectedFeature) {
        return 'Feature Info'
      } else if (this.isMultipleSelectedFeatures) {
        return 'Features'
      }
      return 'Expand'
    },
    showOverlay () {
      // Hide overlay side panel on initial load
      return this.$route.path !== '/'
    },
    panelWidth () {
      return 800
    },
    infoSheetComponent () {
      return this.$store.state.feature.adjustableSidePanel ? InfoSheetAdjustable : InfoSheet
    },
    isFlexBoxComponent () {
      return !this.$store.state.feature.adjustableSidePanel
    },
    isSingleSelectedFeature () {
      return this.dataMartFeatureInfo && this.dataMartFeatureInfo.display_data_name
    },
    isMultipleSelectedFeatures () {
      return this.dataMartFeatures && this.dataMartFeatures.length
    }
  },
  mounted () {
    global.config.debug && console.log('[wally]', this.$route)
  },
  methods: {
  }
}
</script>
