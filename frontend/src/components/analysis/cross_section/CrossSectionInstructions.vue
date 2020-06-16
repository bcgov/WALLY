<template>
  <div>
    <p>Zoom into a place of interest on the map.</p>
    <p>Click on the "Draw a Line" button and draw a line on the map, which must be a straight line through an
      area of wells since the calculation uses the distance of each well from the origin of the line as the hypotenuse.
      Double click to complete the line. The buffer radius is automatically set to 200 metres and can be updated
      to 0 to 1000 metres after your analysis is produced.</p>
    <p>When you hover over the resulting 2D and 3D graphs, a toolbar of icons will appear. To view lithology,
      select the box or lasso icon and then create a box or lasso over the wells in the graph that you want
      to see the lithology for.</p>
    <p>The table below the graph displays the wells in your buffer radius. If you do not want a well included
      in your analysis, then click on the trash icon in the corresponding row and it will be removed from the graph
      and analysis.</p>
    <p>Select the Excel button to download the data and information related to the wells within your cross section.</p>
    <p>If no analysis is produced, then go to the drop down Selection menu and "Reset Selections" and try again.
      It also helps to have the map zoomed to a smaller area with a sufficiently large amount of detail.</p>
    <p>
      For more information on what data is used and caveats to the analysis, please review the "Where does this information come from?" box at the bottom of the page.
    </p>
  </div>
</template>
<script>
export default {
  name: 'CrossSectionInstructions'
}
</script>
