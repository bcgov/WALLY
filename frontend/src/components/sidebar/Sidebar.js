import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'
import StreamStation from '../features/StreamStation'
import EventBus from '../../services/EventBus'

export default {
  name: 'Sidebar',
  components: {
    StreamStation
  },
  data () {
    return {
      active_tab: 0,
      tabs: [
        { id: 1, name: 'Layers' },
        { id: 2, name: 'Features' },
        { id: 3, name: 'Info' }
      ],
      drawer: true,
      mini: true,
      subHeading: '',
      reportLoading: false,
      selectedLayers: []
    }
  },
  computed: {
    ...mapGetters([
      'isMapLayerActive',
      'isDataMartActive',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'allMapLayers',
      'mapLayerName',
      'getMapLayer',
      'selectionBoundingBox',
      'getCategories'
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
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (selectedLayers) {
      this.$store.commit('setActiveMapLayers', selectedLayers)
    },
    updateDataLayer (id, url) {
      if (this.isDataMartActive(id)) {
        this.$store.commit('removeDataMart', id)
      } else {
        this.$store.dispatch('getDataMart', { id: id, url: url })
      }
    },
    createReportFromSelection () {
      this.reportLoading = true
      this.$store.dispatch('downloadExcelReport',
        {
          format: 'xlsx',
          bbox: this.selectionBoundingBox,
          layers: this.dataMartFeatures.map((feature) => {
            // return the layer names from the active data mart features as a list.
            // there is only expected to be one key, so we could use either
            // Object.keys(feature)[0] or call flat() on the resulting nested array.
            return Object.keys(feature)
          }).flat()
        }
      ).catch((e) => {
        console.error(e)
      }).finally(() => {
        this.reportLoading = false
      })
    },
    setSingleListFeature (item, displayName) {
      this.$store.commit('setDataMartFeatureInfo',
        {
          type: item.type,
          display_data_name: displayName,
          geometry: item.geometry,
          properties: item.properties
        })
    },
    onMouseEnterListItem (feature, layerName) {
      this.$store.commit('updateHighlightFeatureData', feature)
    },
    humanReadable: val => humanReadable(val),
    getMapLayerItemTitle: val => {
      return utils.getMapLayerItemTitle(val)
    },
    getMapLayerItemValue: val => utils.getMapLayerItemValue(val),
    getMapSubheading (val) {
      if (!val) { return '' }

      const valStr = val + ''
      if (!~valStr.indexOf('.')) { return valStr }

      let trim = val.substr(0, val.lastIndexOf('.'))
      let name = this.mapLayerName(trim || '')
      if (name) { return name.slice(0, -1) }
    },
    getHighlightProperties (info) {
      let layer = this.getMapLayer(info.display_data_name)
      if (layer != null) {
        let highlightFields = layer.highlight_columns
        let obj = {}
        highlightFields.forEach((field) => {
          obj[field] = info.properties[field]
        })
        return obj
      }
      return {}
    },
    handleResetLayers () {
      this.selectedLayers = []
      EventBus.$emit('draw:reset', null)
      this.$store.commit('setActiveMapLayers', [])
      this.$store.commit('clearDataMartFeatures')
      this.$store.commit('clearDisplayTemplates')
    }
  },
  watch: {
    dataMartFeatureInfo (value) {
      if (value && value.properties) {
        this.setTabById(2)
      }
    },
    dataMartFeatures (value) {
      if (value.length > 0) {
        this.setTabById(1)
      }
    }
  }
}
