import { mapGetters } from 'vuex'
import {dataMarts} from '../../utils/dataMartMetadata'
import ContextImage from './ContextImage'

export default {
  name: 'ContextBarContainer',
  components: { ContextImage },
  data () {
    return {
      drawer: {
        open: true,
        mini: true
      },
      contextComponents: []
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
      this.drawer.mini = !this.drawer.mini
    },
    openContextBar () {
      this.drawer.mini = false
    },
    build (items) {
      items.length > 0 && items.forEach(layers => {
        // Go through each layer
        Object.keys(layers).map(layer => {
          dataMarts[layer].context.forEach(contextData => {
            switch (contextData.type) {
              case 'chart':
                console.log('building chart')
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
      }
    //   console.log('selected some features for container')
    //   if (value.length > 0) {
    //     this.build(value)
    //     this.populateChartData(value)
    //     this.bar_key++ // ugly hack to refresh vue component
    //   }
    }
  }
}
