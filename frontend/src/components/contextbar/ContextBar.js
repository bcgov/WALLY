import RandomChart from '../charts/RandomChart'
import CircleChart from '../charts/CircleChart'

export default {
  name: 'ContextBar',
  components: { CircleChart, RandomChart },
  data () {
    return {
      drawer: {
        open: true,
        mini: true
      }
    }
  },
  methods: {
    toggleContextBar () {
      this.drawer.mini = !this.drawer.mini
    }
  }
}