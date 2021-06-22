<template>
  <div>
    <Plotly v-if="!dataLoading" id="3dPlot" :data="surfaceData" :layout="surfaceLayout" :displayModeBar="true" ref="surfacePlot"></Plotly>
  </div>
</template>
<script src="./CrossSectionChart3d.js"></script>
