<template>
<div id="layerSelectionCard">
    <v-card class="pa-5" >
      <v-row>
        <v-col class="title" cols=4>
          Categories
        </v-col>
        <v-col cols=8 class="text-right">
          <v-btn
            small
            color="grey darken-2"
            text
            :to="{ name: 'import-layer' }"
            v-if="this.app.config && this.app.config.external_import">
            <v-icon small>mdi-cloud-upload</v-icon> Upload file or data
          </v-btn>
          <v-btn @click.prevent="handleResetLayers" small color="grey darken-2" text>
            <v-icon>refresh</v-icon> Reset all
          </v-btn>
        </v-col>
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
            <Dialog
            v-if="item.description"
            :name="item.name" :description="item.description" :url="item.source_url" />
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
            <Dialog
              v-if="item.description"
              :name="item.name"
              :description="item.description"
              :url="item.source_url" />
          </div>
        </template>
      </v-treeview>
      <v-treeview
        selectable
        selected-color="grey darken-2"
        v-if="layers && categories"
        hoverable
        open-on-click
        @input="handleSelectCustomLayer"
        :items="[customLayers]"
        :value="selectedCustomLayers"
      >
        <template v-slot:label="{ item }">
          <div>
            <span>{{item.name}}</span>
            <v-btn
              class="float-right"
              v-if="item.type !=='category'"
              text
              small
              @click="removeCustomLayer(item.id)">
              <v-icon small>mdi-trash-can-outline</v-icon>
            </v-btn>
          </div>
        </template>
      </v-treeview>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
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
      'baseMapLayers',
      'map'
    ]),
    ...mapGetters('customLayers',
      ['customLayers', 'selectedCustomLayers']
    ),
    ...mapGetters([
      'isDataMartActive',
      'loadingFeature',
      'featureError',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'app'
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
    removeCustomLayer (id) {
      this.$store.dispatch('customLayers/unloadCustomLayer', { map: this.map, id })
    },
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
      this.$store.dispatch('map/clearSelections')
      this.$store.dispatch('map/clearHighlightLayer')
      this.$store.dispatch('map/updateActiveMapLayers', [])
      this.$store.commit('resetDataMartFeatureInfo')
      this.$store.commit('clearDataMartFeatures')
    },
    handleSelectLayer (selectedLayers) {
      this.$store.dispatch('map/updateActiveMapLayers', selectedLayers)
      this.$store.dispatch('user/updateDefaultMapLayers', selectedLayers)
    },
    handleSelectBaseLayer (selectedBaseLayers) {
      this.$store.dispatch('map/setActiveBaseMapLayers', selectedBaseLayers)
    },
    handleSelectCustomLayer (selectedCustomLayers) {
      this.$store.dispatch('customLayers/setActiveCustomLayers', selectedCustomLayers)
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
    max-height: calc(100vh - 150px);
  }
</style>
