<template>
  <div>
    <v-toolbar fixed class="wally-toolbar" short>
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
                  color="indigo"
                  dark
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
        <SelectionMenu></SelectionMenu>
      </v-toolbar-items>

      <div class="flex-grow-1"></div>
      <GeocoderSearch/>
    </v-toolbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import GeocoderSearch from './toolbar/GeocoderSearch'
import SelectionMenu from './toolbar/SelectionMenu'
import LayerSelection from './sidebar/LayerSelection'
export default {
  name: 'Toolbar',
  components: {
    GeocoderSearch,
    SelectionMenu,
    LayerSelection
  },
  data: () => ({
    layerSelection: false
  }),
  computed: {
    ...mapGetters([
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
</style>
