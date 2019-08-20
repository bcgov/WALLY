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
      'contexts'
    ])
  },
  mounted () {
  },
  methods: {
    toggleContextBar () {
      this.drawer.mini = !this.drawer.mini
    },
    openContextBar () {
      this.drawer.mini = false
    },
    build (contexts) {
      // contexts.length > 0 && items.forEach(layers => {
        this.contextComponents = []
        // Go through each layer
        Object.values(contexts.contexts).forEach( (layer) => {
          layer.context.forEach(contextData => {
            switch (contextData.type) {
              case 'chart':
                console.log('building chart')
                this.contextComponents.push({ component: ChartWMS, data: contextData.chart, key: this.chartKey })

                // if (dataMarts[layer].type === 'wms') {
                //   contextData.features = layers[layer]
                //   this.contextComponents.push({ component: ChartWMS, data: contextData, key: this.chartKey })
                // } else if (dataMarts[layer].type === 'api') {
                //   this.contextComponents.push({ component: ChartAPI, data: contextData, key: this.chartKey })
                // }
                break
              case 'links':
                console.log('building links')
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
      // })
      console.log('context components', this.contextComponents)
      this.openContextBar()
    }
  },
  watch: {
    contexts (value) {
      // if (value.length > 0) {
        this.build(value)
        this.chartKey++ // hack to refresh vue component; doesn't work
      // }
    }
  }
}
