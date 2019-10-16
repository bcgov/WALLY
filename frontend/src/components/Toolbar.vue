<template>
  <v-toolbar fixed class="wally-toolbar" short>
    <v-toolbar-items class="py-2">
      <v-btn
        color="primary"
        @click.prevent="handleLayerSelectionState"
        :outlined="!layerSelectionActive"
        width=128
      ><v-icon>layers</v-icon> Layers</v-btn>
    </v-toolbar-items>

    <div class="flex-grow-1"></div>
    <v-toolbar-items class="py-2">
      <div id="geocoder" class="mr-5"></div>
    </v-toolbar-items>
  </v-toolbar>
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
      'singleSelectionFeatures'
    ])
  },
  methods: {
    handleLayerSelectionState () {
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
  /* #geocoder {
    width: 64rem!important;
  } */
</style>
