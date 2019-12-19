<template>
  <div>
    <v-toolbar fixed class="wally-toolbar" short>
      <v-toolbar-items class="py-2">
        <v-btn
          color="primary"
          @click.prevent="handleLayerSelectionState"
          :outlined="$route.name !== 'layer-selection'"
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
      // if (!this.featureSelectionExists) {
      //   return this.$store.commit('setLayerSelectionActiveState', true)
      // }
      this.$store.commit('setLayerSelectionActiveState', !this.layerSelectionActive)

      if (this.$route.name === 'layer-selection') {
        // use history if the layer select button was triggered in the application,
        // otherwise go to the home route. This allows us to use the browser history
        // to go back to the previous screen (after selecting layers), without
        // leaving the application (if the layer select was not triggered in app, but
        // instead the user clicked a bookmark directly to /layers)
        if (this.layerSelectTriggered) {
          return this.$router.go(-1)
        } else {
          return this.$router.push('/')
        }
      }
      this.layerSelectTriggered = true
      return this.$router.push('/layers')
    }
  }
}
</script>

<style>
</style>
