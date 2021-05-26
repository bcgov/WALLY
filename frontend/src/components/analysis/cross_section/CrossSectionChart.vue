<template>
  <div>
    This is a chart again
    <Plotly v-show="!dataLoading" id="2dPlot" :data="chartData" :layout="chartLayout"  :modeBarButtonsToRemove="ignoreButtons" ref="crossPlot"></Plotly>
  </div>
</template>
<script src="./CrossSectionChart.js"></script>
