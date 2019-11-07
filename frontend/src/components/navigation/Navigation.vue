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
        @click.prevent="toggleLayerSelection">
        <!--        <v-list-item-action>-->
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on">layers</v-icon>
          </template>
          <span>Layer Selection</span>
        </v-tooltip>
        <!--        </v-list-item-action>-->
      </v-list-item>
      <v-list-item @click="toggleInfoSelection">
        <v-tooltip right>
          <template v-slot:activator="{ on }">
            <v-icon v-on="on">info</v-icon>
          </template>
          <span>Info</span>
        </v-tooltip>
      </v-list-item>
    </v-row>

    <!--    <LayerSelection />-->
  </v-navigation-drawer>
</template>
<script>
import { mapGetters } from 'vuex'
import LayerSelection from '../layer_selection/LayerSelection'
import router from '../../router.js'

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
  methods: {
    toggleLayerSelection () {
      // router.push('/map-layers')
      if (this.$route.path === '/map-layers') {
        router.push('/')
      } else {
        router.push('/map-layers')
      }
      console.log('this route', this.$route)

      // TODO: get rid of setLayerSelectionActive
      // console.log(this.layerSelectionActive)
      // if (!this.featureSelectionExists) {
      //   return this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
      // }
      // this.$store.commit('setLayerSelectionActive', !this.layerSelectionActive)
    },
    toggleInfoSelection () {
      if (this.$route.path === '/map-info') {
        router.push('/')
      } else {
        router.push('/map-info')
      }
    }
  }
}
</script>
