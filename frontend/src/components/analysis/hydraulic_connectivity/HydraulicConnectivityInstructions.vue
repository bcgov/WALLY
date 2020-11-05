<template>
  <div id="hydraulic_connectivity">
    <div>
    <h3>Instructions</h3>
    <p>Zoom into an area of interest on the map.</p>

    <p>
      Click the "Select a Point" button and drop a point of interest to represent a groundwater point of diversion.
      The weighting factor is automatically set to 2 and can be updated after your analysis is produced.
      The weighting factor must be either 1 (linear) or 2 (squared).
    </p>
    <p>
      After your analysis is produced, there are buttons available to remove multiple streams, remove overlaps,
      and remove streams where apportionment is less than 10%.
    </p>
    <p>
      Each row in the table has an eye icon to highlight stream segments and a trash can icon to delete that specific
      stream segment.
    </p>
    <p>
      The button called "New Stream Point" allows you to add new stream points. Each new point you add on the map will
      also appear in the table.
    </p>
    <p>
      If you made modifications to your analysis, such as removing stream segments or adding custom stream points, a
      counterclockwise arrow icon will appear, which allows you to reset the analysis. Warning: This button reloads t
      he analysis to its initial results and will remove any custom-added stream points.
      You can export results to Excel by selecting the "Excel" button.
    </p>
    <p>
      If no analysis is produced, then press "Select a New Point" and try again. It also helps to have the map zoomed
      to a smaller area with a sufficiently large amount of detail.
    </p>
    <p>
      After your analysis is produced, there are buttons available to: remove multiple streams, remove overlaps,
      and remove streams where apportionment is less than 10%. Each row in the table has an eye icon to highlight
      stream segments and a trash can icon to delete that specific stream segment. If you have made modifications
      to your analysis, a counterclockwise arrow icon will appear beside the weighting factor - click on this
      button to reset the analysis to the initial results.
    </p>
    <p>
      You can export results to Excel by selecting the "Excel" button.
    </p>
    <p>
      If no analysis is produced, then go to the drop down Selection menu in the top navigation bar and
      "Reset Selections" and try again. It also helps to have the map zoomed to a smaller area with a
      sufficiently large amount of detail.
    </p>
    </div>
    <div>
      <h3>Methodology</h3>
      <p>
        The Hydraulic Connectivity analysis is produced by obtaining the ten nearest stream segments from the dropped
        point. The tool identifies the closest point on the stream from those stream segments and uses the distance
        from these points to compute what the apportionment value is, based on an inverse distance method as documented
        in the
        <a href="http://a100.gov.bc.ca/appsdata/acat/documents/r50832/HydraulicConnectMW3_1474311684426_4310694949.pdf" target="_blank">
          Determining the Likelihood of Hydraulic Connection
        </a> report from the
        <a href="https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-science-series" target="_blank">
          Water Science Series.
        </a>
      </p>
      <p>The following terms used in this analysis are defined here:</p>
      <dl>
        <dt>Distance</dt>
        <dd>Computed distance of the closest point of the stream to the selected point of interest.</dd>
        <dt>Demand</dt>
        <dd>
          Assign demand from a well to hydraulically connected streams;
          also known as stream apportionment.
        </dd>
        <dt>Weighting Factor</dt>
        <dd>
          A weighting factor of 1 (linear) or 2 (squared) is usually set when assigning demand from a well.
          A larger weighting factor results in a greater contribution from the nearest stream.
          A weighting factor of 2 is recommended for general applications as per
          the guidance document for
          <a href="http://a100.gov.bc.ca/appsdata/acat/documents/r50832/HydraulicConnectMW3_1474311684426_4310694949.pdf" target="_blank">
          Determining the Likelihood of Hydraulic Connection
          </a>.
        </dd>
      </dl>
    </div>
    <div class="mt-3">
      <h3>Data Sources</h3>
      <p class="mb-0">
        The Hydraulic Connectivity analysis feature uses the following datasets:
      </p>
      <ul class="mb-3">
        <li>
          <a href="https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-stream-network" target="_blank">
            Freshwater Atlas Stream Network
          </a>
        </li>
      </ul>
      <p>
        If you notice an issue with data or layers, please notify the contact email listed in the URLs above.
      </p>
    </div>
  </div>
</template>
<style lang="scss">
#hydraulic_connectivity{
  h3 {
    border-bottom: 1px groove;
    margin-bottom: 5px;
  }
}
</style>
<script>
export default {
  name: 'HydraulicConnectivityInstructions'
}
</script>
