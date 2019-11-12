import { mapGetters } from 'vuex'

export default {
  name: 'MapLegend',
  data () {
    return {
      legend: []
    }
  },
  props: ['map'],
  methods: {
    processLayers (layers) {
      this.legend = []
      layers.forEach(layer => {
        const layerID = layer.display_data_name
        let mapLayerType, mapLayerPaint, legendItems
        try {
          mapLayerType = this.map.getLayer(layerID).type

          if (mapLayerType === 'raster') {
          } else {
            mapLayerPaint = this.getPaint(mapLayerType, layerID)
            legendItems = this.getLegendItems(mapLayerPaint, mapLayerType)
            const layerLegend = {
              name: layer.display_name,
              legendItems,
              'plenty': (legendItems.length > 1),
              'className': (legendItems.length > 1) && 'grouped'
            }
            this.legend.push(layerLegend)
          }
        } catch (err) {
          console.error(err)
        }
      })
    },
    getPaint (lType, id) {
      let color = lType !== 'symbol' && this.map.getPaintProperty(id, lType + '-color')
      let strokeWidth = lType === 'circle' && this.map.getPaintProperty(id, lType + '-stroke-width')
      // let strokeColor = lType === 'circle' && this.map.getPaintProperty(id, lType + '-stroke-color')
      let radius = lType === 'circle' && this.map.getPaintProperty(id, lType + '-radius')
      let opacity = lType === 'fill' && this.map.getPaintProperty(id, lType + '-opacity')
      let outlineColor = lType === 'fill' ? this.map.getPaintProperty(id, lType + '-outline-color')
        : lType === 'circle' && this.map.getPaintProperty(id, lType + '-stroke-color')
      let width = lType === 'line' && this.map.getPaintProperty(id, lType + '-width')
      let iconImage = lType === 'symbol' && this.map.getLayoutProperty(id, 'icon-image')
      let iconRotate = lType === 'symbol' && this.map.getLayoutProperty(id, 'icon-rotate')
      let iconSize = lType === 'symbol' && this.map.getLayoutProperty(id, 'icon-size')

      return {
        color,
        strokeWidth,
        radius,
        opacity,
        outlineColor,
        width,
        iconImage,
        iconRotate,
        iconSize
      }
    },
    getLegendItems (paint, lType) {
      let color, text
      // Skip first element
      let icon
      if (lType === 'line') {
        icon = 'remove'
      } else if (lType === 'fill') {
        icon = 'signal_cellular_4_bar'
      } else if (lType === 'symbol') {
        // icon = require('../../assets/mapbox-maki-icons/' + paint.iconImage + '.svg')
        // TODO: Change this to grab SVG & color from mapbox
        // Right now it's hard to do, so this is a quicker way to implement
        paint.color = 'green'
        icon = 'change_history'
      } else {
        icon = 'lens'
      }
      let iconSize = icon === 'lens' ? 12 : 20
      let legendItems = []

      // There's only one type in this layer
      if (typeof paint.color === 'string') {
        legendItems.push({
          'text': '',
          'color': paint.color,
          'outlineColor': paint.outlineColor,
          'lineWidth': paint.width,
          'strokeWidth': paint.strokeWidth ? paint.strokeWidth + 'px' : '1px',
          icon,
          iconSize
        })
        return legendItems
      }

      // Gradient color items that interpolate between 2+ values
      if (paint.color[0] === 'interpolate') {
        legendItems.push({
          'text': '',
          'color': paint.color[6],
          'outlineColor': paint.outlineColor,
          'lineWidth': paint.width,
          'strokeWidth': '1px',
          icon,
          iconSize
        })
        return legendItems
      }

      // Multiple legend items in this layer
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
