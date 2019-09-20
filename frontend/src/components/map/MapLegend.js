import { mapGetters } from 'vuex'

export default {
  name: 'MapLegend',
  data () {
    return {
      legend: {},
      map: this.map
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
          console.log('type and paint', mapLayerType, mapLayerPaint)
          legendItems = this.getLegendItems(mapLayerPaint)
          this.$set(this.legend, layerID, legendItems)
          // this.legend[layerID] = legendItems
        } catch (err) {
          console.log('Layer type doesn\'t exist', err)
        }
      })

      console.log('LEGENDARY', this.legend)
    },
    getPaint (layerType, layerID) {
      let paint = {}
      switch (layerType) {
        case 'circle':
          paint = {
            'circle-color': this.map.getPaintProperty(layerID, 'circle-color'),
            'circle-stroke-width': this.map.getPaintProperty(layerID, 'circle-stroke-width'),
            'circle-radius': this.map.getPaintProperty(layerID, 'circle-radius')
          }
          break
        case 'fill':
          paint = {
            'fill-color': this.map.getPaintProperty(layerID, 'fill-color'),
            'fill-opacity': this.map.getPaintProperty(layerID, 'fill-opacity'),
            'fill-outline-color': this.map.getPaintProperty(layerID, 'fill-outline-color')
          }
          break
        case 'line':
          paint = {
            'line-color': this.map.getPaintProperty(layerID, 'line-color'),
            'line-width': this.map.getPaintProperty(layerID, 'line-width')
          }
          break
      }
      return paint
    },
    getLegendItems (paint) {
      let color = 'color'
      let text = 'text'
      let paintThing = paint['line-color']
      // paint['line-color']
      // Skip first element
      let legendItems = []
      for (let i = 1; i < paintThing.length; i += 2) {
        if (paintThing[i].constructor === Array) {
          text = paintThing[i][2].join(', ')
          color = paintThing[i + 1]
          legendItems.push({
            'text': text,
            'color': color,
            'icon': 'remove' // v-icon
          })
        }
      }

      console.log(legendItems)
      return legendItems
    },
    buildLegend (layers) {
      layers.map(layer => {
        // get legend items
        console.log(layer)
      })
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
