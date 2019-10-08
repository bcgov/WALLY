import { mapGetters } from 'vuex'
import ContextImage from './ContextImage'
import Chart from './Chart'
import ContextLink from './ContextLink'
import ContextTitle from './ContextTitle'
import ContextCard from './ContextCard'

export default {
  name: 'ContextBar',
  components: { ContextImage, Chart, ContextTitle },
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
            this.contextComponents.push({
              component: Chart,
              data: component,
              key: this.chartKey
            })
            break
          case 'links':
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
      // if templates were cleared, close the context bar.
      if (!value.displayTemplates || !value.displayTemplates.length) {
        this.showContextBar = false
        return
      }

      // otherwise, when a new set of templates appears, process them
      // and display them in the context bar.
      this.processTemplates(value.displayTemplates)
      this.chartKey++ // hack to refresh vue component; doesn't work
      // }
    }
  }
}
