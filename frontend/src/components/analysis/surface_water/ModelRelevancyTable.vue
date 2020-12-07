<template>
  <div>
    <v-data-table
      :headers="tableHeaders"
      :items="modelInfo"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      item-key="name"
    >
      <template v-slot:top>
        <v-toolbar flat>
        <div class="title">Model Relevancy Statistics</div>
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
    <v-container>
      <v-row>
        <v-col class="title black--text pl-3 mb-5">Model Relevancy Box Plots</v-col>
      </v-row>
      <v-row no-gutters >
        <v-col cols="12" md="3" v-for="(item) in modelInfo" :key="`modelinput-${item.name}`">
          <ModelRelevancyBoxPlot :statInfo="item"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import ModelRelevancyBoxPlot from './ModelRelevancyBoxPlot'
import { humanReadable } from '../../../common/helpers/index'

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
      { text: 'Units', value: 'units', align: 'end' },
      { text: 'Min', value: 'minimum', sortable: true, align: 'end' },
      { text: 'Quartile1', value: 'quartile_1', align: 'end' },
      { text: 'Median', value: 'median', align: 'end' },
      { text: 'Mean', value: 'average', align: 'end' },
      { text: 'Standard Deviation', value: 'standard_deviation', align: 'end' },
      { text: 'Quartile3', value: 'quartile_3', align: 'end' },
      { text: 'Max', value: 'maximum', align: 'center' },
      { text: 'Watershed Value', value: 'inputValue' },
      { text: '', value: 'data-table-expand' }
    ]
  }),
  methods: {
    parseStat (stat) {
      const input = this.inputs[stat.name]
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
    },
    humanReadable: (val) => humanReadable(val)
  }
}
</script>
