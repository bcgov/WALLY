<template>
  <div>
    <Plotly v-show="!dataLoading" id="2dPlot" :data="chartData" :layout="chartLayout"  :modeBarButtonsToRemove="ignoreButtons" :displayModeBar="true" ref="crossPlot"></Plotly>
  </div>
</template>
<script src="./CrossSectionChart.js"></script>
