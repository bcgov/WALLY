<template>
  <div>
    <v-row>
      <v-col cols=2>
        <v-btn
          fab
          v-if="allowDisableLayerSelection"
          class="elevation-1"
          small
          @click.prevent="$store.commit('setLayerSelectionActiveState', false)"
        ><v-icon>arrow_back</v-icon></v-btn>
      </v-col>
      <v-col class="title" cols=6>
        Categories
      </v-col>
      <v-col cols=4 class="text-right"><v-btn @click.prevent="handleResetLayers" small color="grey lighten-2"><v-icon>refresh</v-icon>Reset all</v-btn></v-col>
    </v-row>
    <v-treeview
      selectable
      selected-color="grey darken-2"
      v-model="selectedLayers"
      @input="handleSelectLayer"
      v-if="layers && categories"
      :items="categories"
    ></v-treeview>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import EventBus from '../../services/EventBus'

export default {
  name: 'LayerSelection',
  data: () => ({
    selectedLayers: []
  }),
  computed: {
    ...mapGetters([
      'isMapLayerActive',
      'isDataMartActive',
      'loadingFeature',
      'featureError',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'getCategories',
      'layerSelectionActive',
      'featureSelectionExists'
    ]),
    allowDisableLayerSelection () {
      return this.featureSelectionExists
    },
    layers () {
      return this.filterLayersByCategory(this.allMapLayers)
    },
    categories () {
      // Returns categories with child nodes from this.layers.
      // The v-treeview component expects nodes to have keys id, name, and children.
      // Finally, filter out empty categories, since this can cause a problem if they get selected
      // and there is no need to allow selecting empty categories.
      return this.getCategories.map((c) => ({
        id: c.layer_category_code,
        name: c.description,
        children: this.layers[c.layer_category_code]
      })).filter((c) => !!c.children)
    }
  },
  methods: {
    filterLayersByCategory (layers) {
      let catMap = {}

      layers.forEach((layer) => {
        const layerNode = {
          id: layer.display_data_name,
          name: layer.display_name
        }
        if (!catMap[layer.layer_category_code]) {
          // this category hasn't been seen yet, start it with this layer in it
          catMap[layer.layer_category_code] = [layerNode]
        } else {
          // category exists: add this layer to it
          catMap[layer.layer_category_code].push(layerNode)
        }
      })
      return catMap
    },
    handleResetLayers () {
      this.selectedLayers = []
      EventBus.$emit('draw:reset', null)
      EventBus.$emit('highlight:clear')
      this.$store.commit('setActiveMapLayers', [])
      this.$store.commit('resetDataMartFeatureInfo')
      this.$store.commit('clearDataMartFeatures')
      this.$store.commit('clearDisplayTemplates')
    },
    handleSelectLayer (selectedLayers) {
      this.$store.commit('setActiveMapLayers', selectedLayers)
    }
  }
}
</script>

<style>

</style>
