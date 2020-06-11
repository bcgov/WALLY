<template>
  <div>
    <p>Zoom into an area of interest on the map.</p>

    <p>
      Click the “Draw Point” button and drop a point of interest to represent a groundwater point of diversion.
      The weighting factor is automatically set to 2 and can be updated after your analysis is produced.
      The weighting factor must be either 1 (linear) or 2 (squared).
    </p>
    <p>
      After your analysis is produced, there are buttons available to: remove multiple streams, remove overlaps,
      and remove streams where apportionment is less than 10%. Each row in the table has an eye icon to highlight
      stream segments and a trash can icon to delete that specific stream segment. If you have made modifications
      to your analysis, a counterclockwise arrow icon will appear beside the weighting factor - click on this
      button to reset the analysis to the initial results.
    </p>
    <p>
      You can export results to Excel by selecting the “Excel” button.
    </p>
    <p>
      If no analysis is produced, then go to the drop down Selection menu in the top navigation bar and
      "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a
      sufficiently large amount of detail.
    </p>
    <p>
      For more information on what data is used and caveats to the analysis, please review the
      "Where does this information come from?" box at the bottom of the page.
    </p>
  </div>
</template>
<script>
export default {
  name: 'StreamApportionmentInstructions'
}
</script>
