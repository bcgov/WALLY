import { mapGetters } from 'vuex'
import { humanReadable } from '../../helpers'
import * as utils from '../../utils/mapUtils'

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
          choices: [{ // TODO update to use DATA_SOURCE from dataUtils
            id: 'Climate Normals 1980-2010',
            name: 'Canadian Climate Normals 1980-2010',
            uri: '',
            geojson: ''
          }]
        }
      ],
      mini: true,
      subHeading: ''
    }
  },
  computed: {
    ...mapGetters([
      'isMapLayerActive',
      'featureInfo',
      'featureLayers'
    ])
  },
  methods: {
    setTabById (id) {
      this.active_tab = id
    },
    handleSelectLayer (id) {
      if (this.isMapLayerActive(id)) {
        this.$store.commit('removeMapLayer', id)
      } else {
        this.$store.commit('addMapLayer', id)
      }
    },
    createReportFromSelection () {
      if (this.active_tab === 1) {
        this.$store.dispatch('downloadLayersReport', this.featureLayers)
      } else if (this.active_tab === 2) {
        this.$store.dispatch('downloadFeatureReport',
          { featureName: this.mapSubheading(this.featureInfo.id), ...this.featureInfo })
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
