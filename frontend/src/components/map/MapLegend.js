import { mapGetters } from 'vuex'

export default {
  name: 'MapLegend',
  data () {
    return {
      legend: [],
      show: true
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

          if (mapLayerType !== 'raster') {
            mapLayerPaint = this.getPaint(mapLayerType, layerID)
            legendItems = this.getLegendItems(mapLayerPaint, mapLayerType, layerID)
            const layerLegend = {
              name: layer.display_name,
              legendItems,
              'plenty': (legendItems.length > 1),
              'className': (legendItems.length > 1) && 'grouped'
            }
            this.legend.push(layerLegend)
          }

          if (mapLayerType === 'raster') {
            const legendItems = [{
              wmsIconUrl: `https://openmaps.gov.bc.ca/geo/pub/${layer.wms_name}/ows?service=WMS&request=GetLegendGraphic&format=image%2Fpng&width=20&height=20&layer=pub%3A${layer.wms_name}&style=${layer.wms_style}`
            }]
            const layerLegend = {
              name: layer.display_name,
              legendItems,
              'plenty': false,
              'className': ''
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
    getLegendItems (paint, lType, layerID) {
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

      if (!paint.color) {
        return legendItems
      }

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
          'color': layerID === 'water_rights_licences' ? paint.color[4] : paint.color[6],
          'outlineColor': layerID === 'water_rights_licences' ? paint.outlineColor[3] : paint.outlineColor,
          'lineWidth': paint.width,
          'strokeWidth': '1px',
          icon,
          iconSize
        })
        return legendItems
      }

      // Multiple legend items in this layer, but there are a few different
      // ways mapbox sends the details (see Mapbox Style Specs)

      // Water Rights Licences
      if (paint.color[0] === 'match') {
        // color[1] will be the condition
        for (let i = 2; i < paint.color.length - 1; i += 2) {
          global.config.debug && console.log('[wally]', paint.color[i].constructor)
          if (paint.color[i].constructor === Array) {
            text = this.replaceLabelCode(paint.color[i].join(', '))
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

      // Streams with allocation restrictions

      for (let i = 1; i < paint.color.length; i += 2) {
        if (paint.color[i].constructor === Array) {
          text = this.replaceLabelCode(paint.color[i][2].join(', '))
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
    },
    replaceLabelCode (code) {
      switch (code) {
        // Stream restrictions
        case 'OR':
          return 'Office Reserve'
        case 'FR':
          return 'Fully Recorded'
        case 'FR_EXC':
          return 'Fully Recorded Except'
        case 'PWS':
          return 'Possible Water Shortage'
        case 'PWS, RNW':
          return 'Possible Water Shortage, Refused No Water'
        // Water Rights Licences
        case 'POD':
          return 'Surface Water'
        case 'PG, PWD':
          return 'Groundwater'
        // Water Approval Points
        case 'Current':
          return 'Active Approvals'
        case 'Refuse/Abandoned, Cancelled':
          return 'Non-Active Approvals'
        default:
          return code
      }
    },
    toggle () {
      this.show = !this.show
    }
  },
  computed: {
    ...mapGetters('map', [
      'activeMapLayers'
    ])
  },
  watch: {
    activeMapLayers (value) {
      this.processLayers(value)
    }
  }
}
