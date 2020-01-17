<template>
<div id="layerSelectionCard">
    <v-card class="pa-5" >
      <v-row>
        <v-col cols=2>
          <v-btn
            fab
            v-if="allowDisableLayerSelection"
            class="elevation-1"
            small
            @click.prevent="$emit('closeDialog')"
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
        :value="activeMapLayers.map(layer => layer.display_data_name)"
        @input="handleSelectLayer"
        v-if="layers && categories"
        hoverable
        open-on-click
        :items="categories"
      >
        <template v-slot:label="{ item }">
          <div>
            <span>{{item.name}}</span>
            <Dialog :name="item.name" :description="item.description" :url="item.source_url" />
          </div>
        </template>
      </v-treeview>
      <v-treeview
        selectable
        selected-color="grey darken-2"
        v-if="layers && categories"
        hoverable
        open-on-click
        @input="handleSelectBaseLayer"
        :items="baseMapLayers"
        :value="selectedBaseLayers"
      >
        <template v-slot:label="{ item }">
          <div>
            <span>{{item.name}}</span>
            <Dialog :name="item.name" :description="item.description" :url="item.source_url" />
          </div>
        </template>
      </v-treeview>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import EventBus from '../../services/EventBus'
import Dialog from '../common/Dialog'

export default {
  name: 'MapLayerSelection',
  components: {
    Dialog
  },
  computed: {
    ...mapGetters('map', [
      'isMapLayerActive',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'getCategories',
      'layerSelectionActive',
      'featureSelectionExists',
      'activeMapLayers',
      'selectedBaseLayers',
      'baseMapLayers'
    ]),
    ...mapGetters([
      'isDataMartActive',
      'loadingFeature',
      'featureError',
      'dataMartFeatures',
      'dataMartFeatureInfo'
    ]),
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
          name: layer.name,
          description: layer.description,
          source_url: layer.source_url
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
      EventBus.$emit('draw:reset', null)
      EventBus.$emit('highlight:clear')
      this.$store.commit('map/setActiveMapLayers', [])
      this.$store.commit('resetDataMartFeatureInfo')
      this.$store.commit('clearDataMartFeatures')
      this.$store.commit('clearDisplayTemplates')
    },
    handleSelectLayer (selectedLayers) {
      this.$store.commit('map/setActiveMapLayers', selectedLayers)
    },
    handleSelectBaseLayer (selectedBaseLayers) {
      this.$store.commit('map/setActiveBaseMapLayers', selectedBaseLayers)
    },
    allowDisableLayerSelection () {
      return this.featureSelectionExists
    }
  }
}
</script>

<style>
  .appendRight{
    float:right;
  }
  #layerSelectionCard {
    z-index: 999!important;
    max-height: 60vh;
  }
</style>
