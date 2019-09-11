import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'
import * as metadataUtils from '../../utils/metadataUtils'
import StreamStation from '../features/StreamStation'
import Well from '../features/Well'
import Aquifer from '../features/Aquifer'

export default {
  name: 'Sidebar',
  components: {
    StreamStation,
    Well,
    Aquifer
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
      subHeading: ''
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
      'getMapLayer'
    ]),
    items () {
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
          { featureName: this.getMapSubheading(this.dataMartFeatureInfo.display_data_name), ...this.dataMartFeatureInfo })
      }
    },
    handleFeatureItemClick (item) {
      // this.$store.dispatch(FETCH_MAP_OBJECT, item.id)
      if ('LATITUDE' in item.properties && 'LONGITUDE' in item.properties) {
        item.coordinates = [item.properties['LATITUDE'], item.properties['LONGITUDE']]
      } else {
        item.coordinates = null
      }
      this.$store.commit('setDataMartFeatureInfo',
        {
          display_data_name: item.id,
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
