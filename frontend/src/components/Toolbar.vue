<template>
  <div>
    <v-toolbar fixed id="wally-toolbar" short>
      <v-toolbar-items class="py-2">

        <v-menu
              v-model="layerSelection"
              :close-on-content-click="false"
              :nudge-width="200"
              offset-y
              allow-overflow
              class="layer-selection-menu"
            >
              <template v-slot:activator="{ on }">
                <v-btn
                  color="grey darken-3"
                  text
                  tile
                  v-on="on"
                >
                  <v-icon>layers</v-icon> Layers
                </v-btn>
              </template>
              <LayerSelection @closeDialog="layerSelection = false"/>
        </v-menu>

        <!-- <v-btn
          color="primary"
          @click.prevent="handleLayerSelectionState"
          :outlined="$route.name !== 'layer-selection'"
          width=128
        ><v-icon>layers</v-icon> Layers</v-btn> -->
        <SelectionMenu/>
      </v-toolbar-items>

      <div class="flex-grow-1"></div>
      <GeocoderSearch/>
      <Screenshot/>
    </v-toolbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import GeocoderSearch from './toolbar/GeocoderSearch'
import SelectionMenu from './toolbar/SelectionMenu'
import LayerSelection from './toolbar/LayerSelection'
import Screenshot from './toolbar/Screenshot'

export default {
  name: 'Toolbar',
  components: {
    GeocoderSearch,
    SelectionMenu,
    LayerSelection,
    Screenshot
  },
  data: () => ({
    layerSelection: false
  }),
  computed: {
    ...mapGetters('map', [
      'layerSelectionActive',
      'singleSelectionFeatures',
      'featureSelectionExists',
      'layerSelectTriggered'
    ])
  },
  methods: {
    handleLayerSelectionState () {
      // if (!this.featureSelectionExists) {
      //   return this.$store.commit('setLayerSelectionActiveState', true)
      // }
      this.$store.commit('setLayerSelectionActiveState', !this.layerSelectionActive)

      this.$store.commit('setLayerSelectTriggered', true)
      return this.$router.push('/layers')
    }
  }
}
</script>

<style lang="scss">
.layer-selection-menu {
  max-height: 60vh;
}
#wally-toolbar {
  box-shadow: inset 0 -1px 0 grey;
  z-index: 3;
  position: relative;
}
</style>
