<template>
  <v-navigation-drawer
    clipped
    mini-variant
    mini-variant-width="56"
    app
    permanent
    collapse
    color="#036"
    dark
  >

    <v-row>
      <v-list-item
        @click.prevent="handleLayerSelection">
        <!--        <v-list-item-action>-->
        <v-icon>layers</v-icon>
        <!--        </v-list-item-action>-->
      </v-list-item>
      <v-list-item @click="">
        <v-list-item-action>
          <v-icon>info</v-icon>
        </v-list-item-action>
      </v-list-item>
    </v-row>

    <!--    <LayerSelection />-->
  </v-navigation-drawer>
</template>
<script>
import { mapGetters } from 'vuex'
import LayerSelection from '../layer_selection/LayerSelection'

export default {
  name: 'Navigation',
  data: () => ({
    drawer: true,
    mini: true
  }),
  computed: {
    ...mapGetters([
      'layerSelectionActive',
      'singleSelectionFeatures',
      'featureSelectionExists'
    ])
  },
  components: {
    LayerSelection
  },
  methods: {
    handleLayerSelection () {
      console.log(this.layerSelectionActive)
      if (!this.featureSelectionExists) {
        return this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
      }
      this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
    }
  }
}
</script>
