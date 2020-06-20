<template>
  <div id="app-overlay" v-if="this.showOverlay">
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

export default {
  name: 'InfoPanel',
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
  watch: {
    $route (to, from) {
      this.$store.dispatch('map/resizeMap')
    }
  },
  computed: {
    ...mapGetters('map', [
      'isMapLayerActive',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'getCategories',
      'layerSelectionActive',
      'isMapReady'

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
    console.log(this.$route)
  },
  methods: {
  }
}
</script>
