import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'
import * as metadataUtils from '../../utils/metadataUtils'
import StreamStation from '../features/StreamStation'

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
      reportLoading: false
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
      'selectionBoundingBox'
    ]),
    layers () {
      return [
        {
          title: 'Layers',
          active: 'true',
          icon: 'layers',
          action: 'layers',
          choices: this.allMapLayers
        }
      ]
    }
  },
  methods: {
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (id) {
      this.updateMapLayer(id)
    },
    updateMapLayer (id) {
      if (this.isMapLayerActive(id)) {
        this.$store.commit('removeMapLayer', id)
      } else {
        this.$store.commit('addMapLayer', id)
      }
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
      this.$store.dispatch('downloadFeatureReport',
        {
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
    handleFeatureItemClick (item, displayName) {
      // this.$store.dispatch(FETCH_MAP_OBJECT, item.id)
      if ('LATITUDE' in item.properties && 'LONGITUDE' in item.properties) {
        item.coordinates = [item.properties['LATITUDE'], item.properties['LONGITUDE']]
      } else {
        item.coordinates = null
      }
      this.$store.commit('setDataMartFeatureInfo',
        {
          display_data_name: displayName,
          coordinates: item.coordinates,
          properties: item.properties
        })
    },
    humanReadable: val => humanReadable(val),
    getMapLayerItemTitle: val => {
      console.log(val)
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
