import { mapGetters } from 'vuex'
import { dataMarts } from '../../utils/dataMartMetadata'
import ContextImage from './ContextImage'
import ChartWMS from './ChartWMS'
import ChartAPI from './ChartAPI'

export default {
  name: 'ContextBar',
  components: { ContextImage, ChartWMS, ChartAPI },
  data () {
    return {
      showContextBar: false,
      drawer: {
        open: true,
        mini: true
      },
      contextComponents: [],
      chartKey: 0
    }
  },
  computed: {
    ...mapGetters([
      'dataMartFeatures'
    ])
  },
  mounted () {
  },
  methods: {
    toggleContextBar () {
      this.showContextBar = !this.showContextBar
    },
    openContextBar () {
      this.showContextBar = true
    },
    build (items) {
      items.length > 0 && items.forEach(layers => {
        this.contextComponents = []
        // Go through each layer
        Object.keys(layers).map(layer => {
          dataMarts[layer].context.forEach(contextData => {
            switch (contextData.type) {
              case 'chart':
                console.log('building chart')
                if (dataMarts[layer].type === 'wms') {
                  contextData.features = layers[layer]
                  this.contextComponents.push({ component: ChartWMS, data: contextData, key: this.chartKey })
                } else if (dataMarts[layer].type === 'api') {
                  this.contextComponents.push({ component: ChartAPI, data: contextData, key: this.chartKey })
                }
                break
              case 'link':
                console.log('building link')
                break
              case 'title':
                console.log('building title')
                break
              case 'image':
                console.log('building image')
                this.contextComponents.push({ component: ContextImage, data: contextData })
                break
            }
          })
        })
      })
      console.log('context components', this.contextComponents)
      this.openContextBar()
    }
  },
  watch: {
    dataMartFeatures (value) {
      if (value.length > 0) {
        this.build(value)
        this.chartKey++ // hack to refresh vue component; doesn't work
      }
    }
  }
}
