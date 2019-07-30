import { mapGetters } from 'vuex'
import RandomChart from '../charts/RandomChart'
import CircleChart from '../charts/CircleChart'
import BarChart from '../charts/BarChart.js'
import chartColors from '../../constants/colors'

export default {
  name: 'ContextBar',
  components: { CircleChart, RandomChart, BarChart },
  data () {
    return {
      drawer: {
        open: true,
        mini: true
      },
      bar_key: 0,
      bar_data: {
        labels: [],
        datasets: [{
          label: 'Bar chart',
          data: [],
          backgroundColor: [],
          borderColor: [],
          borderWidth: 1
        }],
        visible: true
      }
    }
  },
  computed: {
    ...mapGetters([
      'featureLayers'
    ])
  },
  mounted () {
    this.bar_data = {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'Water Quantity',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: chartColors.backgroundColor,
        borderColor: chartColors.border,
        borderWidth: 1
      }]
    }
  },
  methods: {
    toggleContextBar () {
      this.drawer.mini = !this.drawer.mini
    },
    populateChartData (items) {
      // console.log('populating data.....')
      if (items.length > 0) {
        this.bar_data.labels = []
        this.bar_data.datasets[0].data = []
        this.bar_data.visible = true

        items.forEach((layerGroup, groupIndex) => {
          Object.keys(layerGroup).map(key => {
            layerGroup[key].forEach(item => {
              // Depends on the type of data
              console.log(item.properties.LICENCE_NUMBER, item.properties.QUANTITY, item.properties)
              this.bar_data.labels.push(item.properties.LICENCE_NUMBER)
              this.bar_data.datasets[0].data.push(item.properties.QUANTITY)
              console.log(this.bar_data)
            })
          })
        })
      }
    }
  },
  watch: {
    featureLayers (value) {
      // console.log('selected some features')
      if (value.length > 0) {
        this.populateChartData(value)
        this.bar_key++
      }
    }
  }
}
