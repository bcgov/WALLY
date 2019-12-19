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
      <GeocoderSearch/>
    </v-toolbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import GeocoderSearch from './toolbar/GeocoderSearch'
export default {
  name: 'Toolbar',
  components: {
    GeocoderSearch
  },
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
</style>
