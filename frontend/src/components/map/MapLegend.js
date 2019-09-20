import { mapGetters } from 'vuex'

export default {
  name: 'MapLegend',
  data () {
    return {
      legend: {}
    }
  },
  props: ['map'],
  methods: {
    processLayers (layers) {
      this.legend = {}
      layers.forEach(layer => {
        const layerID = layer.display_data_name
        let mapLayerType, mapLayerPaint, legendItems
        try {
          mapLayerType = this.map.getLayer(layerID).type
          mapLayerPaint = this.getPaint(mapLayerType, layerID)
          if (mapLayerType === 'raster') {
            console.log('Using a graphic')
          } else {
            legendItems = this.getLegendItems(mapLayerPaint, mapLayerType)
            this.$set(this.legend, layer.display_name, legendItems)
          }
        } catch (err) {
        }
      })
    },
    getPaint (lType, id) {
      let color = this.map.getPaintProperty(id, lType + '-color')
      let strokeWidth = lType === 'circle' && this.map.getPaintProperty(id, lType + '-stroke-width')
      let radius = lType === 'circle' && this.map.getPaintProperty(id, lType + '-radius')
      let opacity = lType === 'fill' && this.map.getPaintProperty(id, lType + '-opacity')
      let outlineColor = lType === 'fill' && this.map.getPaintProperty(id, lType + '-outline-color')
      let width = lType === 'line' && this.map.getPaintProperty(id, lType + '-width')

      return {
        color,
        strokeWidth,
        radius,
        opacity,
        outlineColor,
        width
      }
    },
    getLegendItems (paint, lType) {
      let color, text
      // Skip first element
      let icon = (lType === 'line') ? 'remove' : 'lens'
      let legendItems = []
      for (let i = 1; i < paint.color.length; i += 2) {
        if (paint.color[i].constructor === Array) {
          text = paint.color[i][2].join(', ')
          color = paint.color[i + 1]
          legendItems.push({
            'text': text,
            'color': color,
            'icon': icon
          })
        }
      }
      return legendItems
    }
  },
  computed: {
    ...mapGetters([
      'activeMapLayers'
    ])
  },
  watch: {
    activeMapLayers (value) {
      this.processLayers(value)
    }
  }
}
