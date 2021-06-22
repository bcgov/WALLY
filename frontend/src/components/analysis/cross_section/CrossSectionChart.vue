<template>
  <div>
    <v-btn small v-on:click="resetMarkerLabels" color="blue-grey lighten-4" class="mb-1 mt-0 mr-5 ml-2">
      <span class="hidden-sm-and-down"><v-icon color="secondary" class="mr-1" size="18">format_clear</v-icon>Reset Labels</span>
    </v-btn>
    <Plotly v-show="!dataLoading" :id="plotId" :data="chartData" :layout="chartLayout" :modeBarButtonsToRemove="ignoreButtons" :displayModeBar="true" ref="crossPlot"></Plotly>
  </div>
</template>
<script src="./CrossSectionChart.js"></script>
