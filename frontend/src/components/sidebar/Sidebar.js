import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'
import * as dataUtils from '../../utils/dataUtils'

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
      items: [
        {
          title: 'Layers',
          icon: 'layers',
          action: 'layers',
          choices: utils.MAP_LAYERS
        },
        {
          title: 'Data Sources',
          icon: 'library_books',
          action: 'library_books',
          choices: dataUtils.DATA_LAYERS
        }
      ],
      mini: true,
      subHeading: ''
    }
  },
  computed: {
    ...mapGetters([
      'isMapLayerActive',
      'isDataSourceActive',
      'featureInfo',
      'featureLayers'
    ])
  },
  methods: {
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (id, type, resource) {
      if (type === dataUtils.API_DATASOURCE) {
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
      if (this.isDataSourceActive(id)) {
        this.$store.commit('removeDataSource', id)
      } else {
        this.$store.dispatch('getDataSource', { id: id, url: url })
      }
    },
    handleSelectListItem (item) {
      // this.$store.dispatch(FETCH_MAP_OBJECT, item.id)
      if ('LATITUDE' in item.properties && 'LONGITUDE' in item.properties) {
        item.coordinates = [item.properties['LATITUDE'], item.properties['LONGITUDE']]
      } else {
        item.coordinates = null
      }
      this.$store.commit('setFeatureInfo', item)
    },
    createReportFromSelection () {
      if (this.active_tab === 1) {
        this.$store.dispatch('downloadLayersReport', this.featureLayers)
      } else if (this.active_tab === 2) {
        this.$store.dispatch('downloadFeatureReport',
          { featureName: this.mapSubheading(this.featureInfo.id), ...this.featureInfo })
      }
    },
    humanReadable: val => humanReadable(val),
    mapLayerItemTitle: val => utils.mapLayerItemTitle(val),
    mapLayerItemValue: val => utils.mapLayerItemValue(val),
    mapLayerName: val => utils.mapLayerName(val),
    mapSubheading: val => utils.mapSubheading(val)
  },
  watch: {
    featureInfo (value) {
      if (value && value.properties) {
        this.setTabById(2)
      }
    },
    featureLayers (value) {
      if (value.length > 0) {
        this.setTabById(1)
      }
    }
  }
}
