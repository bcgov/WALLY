import { mapGetters } from 'vuex'
import RandomChart from '../charts/RandomChart'
import CircleChart from '../charts/CircleChart'
import BarChart from '../charts/BarChart.js'
import { chartColors } from '../../constants/colors'
import { dataMarts } from '../../utils/dataMartMetadata'

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
      'dataMartFeatures'
    ])
  },
  mounted () {
    this.bar_data = {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: 'Water Quantity',
        data: [],
        backgroundColor: chartColors.background,
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
      // Clear data
      this.bar_data.labels = []
      this.bar_data.datasets = []
      this.bar_data.visible = true

      items.length > 0 && items.forEach(layers => {
        // Go through each layer
        Object.keys(layers).map(layer => {
          const tempDataset = {
            label: '',
            data: [],
            backgroundColor: chartColors.background,
            borderColor: chartColors.border,
            borderWidth: 1
          }
          tempDataset.label = dataMarts[layer].highlight_fields.label
          layers[layer].forEach(item => {
            // Depends on the type of data
            dataMarts[layer].highlight_fields.data_labels.forEach(label => {
              this.bar_data.labels.push(item.properties[label])
            })
            dataMarts[layer].highlight_fields.datasets.forEach((dataset, i) => {
              tempDataset.data.push(item.properties[dataset])
            })
          })
          this.bar_data.datasets.push(tempDataset)
        })
      })
    }
  },
  watch: {
    // TODO: Rename this to something like features/pointsSelected
    dataMartFeatures (value) {
      // console.log('selected some features')
      if (value.length > 0) {
        this.populateChartData(value)
        this.bar_key++
      }
    }
  }
}
