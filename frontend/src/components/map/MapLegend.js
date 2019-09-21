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

          if (mapLayerType === 'raster') {
            console.log('Using a graphic')
          } else {
            mapLayerPaint = this.getPaint(mapLayerType, layerID)
            legendItems = this.getLegendItems(mapLayerPaint, mapLayerType)
            this.$set(this.legend, layer.display_name, legendItems)
          }
        } catch (err) {
          console.log('Something happened', err)
        }
      })
    },
    getPaint (lType, id) {
      console.log(lType)
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
      console.log(paint)
      let icon
      if (lType === 'line') {
        icon = 'remove'
      } else if (lType === 'fill') {
        icon = 'signal_cellular_4_bar'
      } else {
        icon = 'lens'
      }
      let iconSize = icon === 'lens' ? 12 : 20
      let legendItems = []

      console.log(paint.color)
      // There's only one type in this layer
      if (typeof paint.color === 'string') {
        console.log('blha')
        legendItems.push({
          'text': '',
          'color': paint.color,
          'outlineColor': paint.outlineColor,
          icon,
          iconSize
        })
      }

      for (let i = 1; i < paint.color.length; i += 2) {
        if (paint.color[i].constructor === Array) {
          text = paint.color[i][2].join(', ')
          color = paint.color[i + 1]
          legendItems.push({
            text,
            color,
            outlineColor: paint.outlineColor,
            icon,
            iconSize
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
