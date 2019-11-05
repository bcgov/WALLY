import { mapGetters } from 'vuex'
import EventBus from '../../services/EventBus'
import Chart from '../charts/Chart'

const randomValues = (count, min, max) => {
  const delta = max - min
  return Array.from({ length: count }).map(() => Math.random() * delta + min)
}

let y0 = []
let y1 = []
for (let i = 0; i < 50; i++) {
  y0[i] = Math.random()
  y1[i] = Math.random() + 1
}
let trace1 = {
  y: y0,
  type: 'box'
}

let trace2 = {
  y: y1,
  type: 'box'
}

export default {
  name: 'LayerSelection',
  components: {
    Chart
  },
  data: () => ({
    selectedLayers: [],
    chartData: {
      labels: [],
      datasets: [{
        label: 'boxplot chart',
        data: [],
        // backgroundColor: blueChartColors.background,
        // borderColor: blueChartColors.border,
        borderWidth: 1
      }],
      visible: true
    },
    boxplotData: {
      data: [trace1, trace2],
      layout: {
        title: 'My boxplot graph'
      }
    }
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
      'featureSelectionExists',
      'activeMapLayers'
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
