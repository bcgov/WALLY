<template>
  <div>
    <LayerSelection></LayerSelection>
    <MapFeatureSelectionSingle v-if="dataMartFeatureInfo && dataMartFeatureInfo.display_data_name"></MapFeatureSelectionSingle>
  </div>
</template>
<script>
import LayerSelection from '../layer_selection/LayerSelection.vue'
import MapFeatureSelectionSingle from './MapFeatureSelectionSingle'
export default {
  name: 'Panels',
  components: {
    MapFeatureSelectionSingle,
    LayerSelection
  }
}
</script>
