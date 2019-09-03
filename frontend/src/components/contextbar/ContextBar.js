import { mapGetters } from 'vuex'
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
    processTemplates (templates) {
      // console.log(templates)
      this.contextComponents = []
      templates.length > 0 && templates.forEach(template => {
        this.contextComponents.push({
          component: ContextTitle,
          data: { title: template.title },
          key: this.chartKey++
        })
        this.buildComponents(template.display_components)
      })
      this.openContextBar()
    },
    buildComponents (components) {
      components.forEach(component => {
        switch (component.type) {
          case 'chart':
            // build chart
            console.log('building chart', component)
            this.contextComponents.push({
              component: ChartWMS,
              data: component,
              key: this.chartKey
            })
            break
          case 'link':
            this.contextComponents.push({
              component: ContextLink,
              data: component,
              key: this.chartKey
            })
            break
          case 'title':
            this.contextComponents.push({
              component: ContextTitle,
              data: component,
              key: this.chartKey
            })
            break
          case 'image':
            this.contextComponents.push({
              component: ContextImage,
              data: component,
              key: this.chartKey
            })
            break
          case 'card':
            this.contextComponents.push({
              component: ContextCard,
              data: component,
              key: this.chartKey
            })
            break
        }
      })
    }
  },
  watch: {
    displayTemplates (value) {
      this.processTemplates(value.displayTemplates)
      this.chartKey++ // hack to refresh vue component; doesn't work
      // }
    }
  }
}
