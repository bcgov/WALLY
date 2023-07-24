<template>
  <div>
    <p>
      Zoom into an area of interest on the map.
    </p>
    <p>
      Click on the "Select Point" button and select a point on a stream. The buffer radius is
      automatically set to 50 metres and can be updated from 0 to 500 metres after your analysis is produced.
    </p>
    <p>
      You can search the entire upstream catchment or within the distance of the stream. The entire
      upstream catchment is the full area that drains to the point you selected (entire drainage basin
      upstream from your point). The stream buffer shows the area within the buffer radius from the stream.
    </p>
    <p>
      A drop down menu gives you options of layers to analyze: Groundwater Wells, Water Rights Licences,
      Water Rights Applications, EcoCat Reports, Aquifers or Critical Habitats. After you make a selection,
      there is the option to enable the layer to see all the features of that layer.
    </p>
    <p>
      If no analysis is produced, then go to the drop down Selection menu in the top navigation bar and
      "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a
      sufficiently large amount of detail.
    </p>
    <p>
      For more information on what data is used and caveats to the analysis, please review the "Where does
      this information come from?" box at the bottom of the page.
    </p>
  </div>
</template>
<script>
export default {
  name: 'UpstreamDownstreamInstructions'
}
</script>
