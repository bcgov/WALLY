import { mapGetters } from 'vuex'
import { dataMarts } from '../../utils/dataMartMetadata'
import ContextImage from './ContextImage'
import ChartWMS from './ChartWMS'
import ChartAPI from './ChartAPI'
import ContextLink from './ContextLink'
import ContextTitle from './ContextTitle'
import ContextCard from './ContextCard'

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
    processLayers (items) {
      let contextList, dataType, features
      items.length > 0 && items.forEach(layers => {
        this.contextComponents = []
        // Go through each layer
        Object.keys(layers).map(layer => {
          contextList = dataMarts[layer].context
          dataType = dataMarts[layer].type
          features = layers[layer]
          this.buildComponents(contextList, dataType, features)
        })
      })
      this.openContextBar()
    },
    buildComponents (contextList, dataType, features) {
      contextList.forEach(contextData => {
        switch (contextData.type) {
          case 'chart':
            // api call to aggregator for chart features
            if (dataType === 'wms') {
              contextData.features = features
              this.contextComponents.push({
                component: ChartWMS,
                data: contextData,
                key: this.chartKey
              })
            } else if (dataType === 'api') {
              this.contextComponents.push({
                component: ChartAPI,
                data: contextData,
                key: this.chartKey
              })
            }
            break
          case 'link':
            this.contextComponents.push({
              component: ContextLink,
              data: contextData
            })
            break
          case 'title':
            this.contextComponents.push({
              component: ContextTitle,
              data: contextData
            })
            break
          case 'image':
            this.contextComponents.push({
              component: ContextImage,
              data: contextData
            })
            break
          case 'card':
            this.contextComponents.push({
              component: ContextCard,
              data: contextData
            })
            break
        }
      })
    }
  },
  watch: {
    dataMartFeatures (value) {
      if (value.length > 0) {
        this.processLayers(value)
        this.chartKey++ // hack to refresh vue component; doesn't work
      }
    }
  }
}
