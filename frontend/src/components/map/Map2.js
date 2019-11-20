import MapLegend from './MapLegend.vue'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Map',
  components: { MapLegend },
  data () {
    return {
      map: null,
      // legendControlContent: null,
      // activeLayerGroup: L.layerGroup(),
      // markerLayerGroup: L.layerGroup(),
      activeLayers: {},
      draw: null, // mapbox draw object (controls drawn polygons e.g. for area select)
      isDrawingToolActive: false
    }
  },
  computed: {
    ...mapGetters([
      'allMapLayers',
      'activeMapLayers',
      'allDataMarts',
      'activeDataMarts',
      'highlightFeatureData',
      'dataMartFeatureInfo',
      'infoPanelVisible'
    ])
  },
  methods: {
    ...mapActions(['initMap'])
  },
  mounted () {
    this.initMap()
  }
}
