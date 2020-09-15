<template>
  <v-data-table
    :headers="tableHeaders"
    :items="modelInfo"
    :single-expand="singleExpand"
    :expanded.sync="expanded"
    item-key="name"
    show-expand
  >
    <template v-slot:top>
      <v-toolbar flat>
      <h4>Watershed Relevancy</h4>
      </v-toolbar>
    </template>
    <template v-slot:[`item.name`]="{ item }">
      {{ humanReadable(item.name) }}
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <ModelRelevancyBoxPlot :statInfo="item"/>
      </td>
    </template>
  </v-data-table>
</template>

<script>
import ModelRelevancyBoxPlot from './ModelRelevancyBoxPlot'
import { humanReadable } from './../../../helpers/index'

export default {
  name: 'ModelRelevancyTable',
  components: {
    ModelRelevancyBoxPlot
  },
  props: ['modelInfo'],
  data: () => ({
    singleExpand: false,
    expanded: [],
    tableHeaders: [
      { text: 'Name', value: 'name', sortable: true },
      { text: 'Units', value: 'units' },
      { text: 'Min', value: 'minimum', sortable: true },
      { text: 'Quartile 1', value: 'quartile_1', align: 'end' },
      { text: 'Median', value: 'median', align: 'end' },
      { text: 'Mean', value: 'average', align: 'end' },
      { text: 'Standard Deviation', value: 'standard_deviation', align: 'end' },
      { text: 'Quartile 3', value: 'quartile_3', align: 'end' },
      { text: 'Max', value: 'maximum', align: 'center' },
      { text: 'Watershed Value', value: 'inputValue' },
      { text: '', value: 'data-table-expand' }
    ]
  }),
  methods: {
    parseStat (stat) {
      var input = this.inputs[stat.name]
      return [{
        type: 'box',
        name: stat.name,
        y: [stat.minimum, stat.quartile_1, stat.median, stat.median, stat.quartile_3, stat.maximum]
      },
      {
        type: 'line',
        name: 'Watershed Input',
        y: [input, input],
        x: [0, 1],
        line: { color: '#17BECF' }
      }]
    }
  }
}
</script>
