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
  components: { ContextImage, ChartWMS, ChartAPI, ContextTitle },
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
      'displayTemplates'
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
    processLayers (templates) {
      // TODO: Merge the two codebase
      console.log(templates)
    }
    /*
<<<<<<< HEAD
    processLayers (templates) {
      let contextList, dataType, features
      templates.length > 0 && templates.forEach(template => {
        this.contextComponents = []
        // Go through each layer
        Object.keys(template).map(layer => {
          contextList = dataMarts[layer].context
          dataType = dataMarts[layer].type
          features = template[layer]
          this.buildComponents(contextList, dataType, features)
        })
      })
=======
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
>>>>>>> alex/dbrefactor2
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
    } */
  },
  watch: {
    displayTemplates (value) {
      this.processLayers(value.displayTemplates)
      this.chartKey++ // hack to refresh vue component; doesn't work
      // }
    }
  }
}
