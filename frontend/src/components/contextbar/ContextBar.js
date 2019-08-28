import { mapGetters } from 'vuex'
import { dataMarts } from '../../utils/dataMartMetadata'
import ContextImage from './ContextImage'
import ChartWMS from './ChartWMS'
import ChartAPI from './ChartAPI'
import ContextTitle from './ContextTitle'

export default {
  name: 'ContextBar',
  components: { ContextImage, ChartWMS, ChartAPI, ContextTitle },
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
      'displayTemplates'
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
    build (displayTemplates) {
      // contexts.length > 0 && items.forEach(layers => {
        this.contextComponents = []
        // Go through each layer
        displayTemplates.forEach(displayTemplate => {
          this.contextComponents.push({ component: ContextTitle, data: {data: {title: displayTemplate.title}}, key: this.chartKey + 1000 })
          displayTemplate.display_components.forEach(component => {
            switch (component.type) {
              case 'chart':
                console.log('building chart')
                this.contextComponents.push({ component: ChartWMS, data: component.chart, key: this.chartKey })
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
    displayTemplates (value) {
      // if (value.length > 0) {
        this.build(value.displayTemplates)
        this.chartKey++ // hack to refresh vue component; doesn't work
      // }
    }
  }
}
