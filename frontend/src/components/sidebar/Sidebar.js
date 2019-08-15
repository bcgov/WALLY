import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'
import * as metadataUtils from '../../utils/metadataUtils'

export default {
  name: 'Sidebar',
  data () {
    return {
      active_tab: 0,
      tabs: [
        { id: 1, name: 'Layers' },
        { id: 2, name: 'Features' },
        { id: 3, name: 'Info' }
      ],
      drawer: true,
      // items: [
      //   {
      //     title: 'Layers',
      //     icon: 'layers',
      //     action: 'layers',
      //     // TODO: Replace with api call
      //     choices: this.allMapLayers ? this.allMapLayers.filter(ml => ml.map_layer_type_id === metadataUtils.WMS_DATAMART) : []
      //   },
      //   {
      //     title: 'Data Sources',
      //     icon: 'library_books',
      //     action: 'library_books',
      //     // TODO: Replace with api call
      //     choices: metadataUtils.DATA_MARTS.filter(dm => dm.type === metadataUtils.API_DATAMART)
      //   }
      // ],
      mini: true,
      subHeading: ''
    }
  },
  computed: {
    ...mapGetters([
      'isMapLayerActive',
      'isDataMartActive',
      'dataMartFeatures',
      'dataMartFeatureInfo',
      'allMapLayers'
    ]),
    items() {
      return [
        {
          title: 'Layers',
          icon: 'layers',
          action: 'layers',
          choices: this.allMapLayers ? this.allMapLayers.filter(ml => ml.map_layer_type_id === metadataUtils.WMS_DATAMART) : []
        },
        {
          title: 'Data Sources',
          icon: 'library_books',
          action: 'library_books',
          // TODO: Replace with api call
          choices: metadataUtils.DATA_MARTS.filter(dm => dm.type === metadataUtils.API_DATAMART)
        }
      ]
    }
  },
  methods: {
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (id, type, resource) {
      if (type === metadataUtils.API_DATAMART) {
        this.updateDataLayer(id, resource)
      } else {
        this.updateMapLayer(id)
      }
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
      if (this.active_tab === 1) {
        this.$store.dispatch('downloadLayersReport', this.dataMartFeatures)
      } else if (this.active_tab === 2) {
        this.$store.dispatch('downloadFeatureReport',
          { featureName: this.getMapSubheading(this.dataMartFeatureInfo.id), ...this.dataMartFeatureInfo })
      }
    },
    handleFeatureItemClick (item) {
      // this.$store.dispatch(FETCH_MAP_OBJECT, item.id)
      if ('LATITUDE' in item.properties && 'LONGITUDE' in item.properties) {
        item.coordinates = [item.properties['LATITUDE'], item.properties['LONGITUDE']]
      } else {
        item.coordinates = null
      }
      this.$store.commit('setDataMartFeatureInfo', item)
    },
    humanReadable: val => humanReadable(val),
    getMapLayerItemTitle: val => utils.getMapLayerItemTitle(val),
    getMapLayerItemValue: val => utils.getMapLayerItemValue(val),
    getMapLayerName: val => utils.getMapLayerName(val),
    getMapSubheading: val => utils.getMapSubheading(val)
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
