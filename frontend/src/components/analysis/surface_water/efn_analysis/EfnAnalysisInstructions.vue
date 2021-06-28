
<template>
  <div id="hydraulic_connectivity" class="instructions">
    <div>
    <h3>Instructions</h3>
    <p>There are two options currently available to further refine the EFN results for your selected watershed.
      These toggles are available under the Species Sensitivity header below.</p>
    <p>1. "Highly sensitive species in the area" will disable the risk calculations and display because special consideration should be taken in this scenario.</p>
    <p>2. "Fish bearing watershed" will update the risk calculations to use the more sensitive risk thresholds when calculating the monthly risk levels.</p>
    <p></p>
    </div>
    <div class="mt-12">
      <h3>Methodology</h3>
      <p>
        The EFN risk values presented here by WALLY are based upon the 2016 Evironmental Risk Management Framework.
        The following graphic shows a chart that outlines the flow sensitivity logic used to determine monthly risk levels.
      </p>
      <img
        :src="require('../../../../assets/images/efn_chart.png')"
        width="625"
        alt="EFN Risk Management Framework" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'EfnAnalysisInstructions'
}
</script>

<style>
.efn-img{
  width: 250px;
}
</style>
