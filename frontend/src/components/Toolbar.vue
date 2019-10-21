<template>
  <div>
    <v-toolbar fixed class="wally-toolbar" short>
      <v-toolbar-items class="py-2">
        <v-btn
          color="primary"
          @click.prevent="handleLayerSelectionState"
          :outlined="!layerSelectionActive && this.featureSelectionExists"
          width=128
        ><v-icon>layers</v-icon> Layers</v-btn>
      </v-toolbar-items>

      <div class="flex-grow-1"></div>
      <v-toolbar-items class="py-2">
      </v-toolbar-items>
    </v-toolbar>
    <div id="geocoder" class="mr-5 geocoder"></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Toolbar',
  data: () => ({
  }),
  computed: {
    ...mapGetters([
      'layerSelectionActive',
      'singleSelectionFeatures',
      'featureSelectionExists'
    ])
  },
  methods: {
    handleLayerSelectionState () {
      if (!this.featureSelectionExists) {
        return this.$store.commit('setLayerSelectionActiveState', true)
      }
      this.$store.commit('setLayerSelectionActiveState', !this.layerSelectionActive)
    }
  }
}
</script>

<style>
  .wally-toolbar {
    box-shadow: inset 0 -1px 0 grey;
    z-index: 3;
  }
  .mapboxgl-ctrl-geocoder {
    width: 164rem!important;
    border: 1px solid #3B99FC;
  }
  #geocoder {
    position: absolute;
    z-index: 4;
    right:15px;
    top: 8px;
  }
</style>
