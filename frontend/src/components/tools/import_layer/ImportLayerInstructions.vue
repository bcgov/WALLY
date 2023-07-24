<template>
  <div id="import_layer_instructions" class="instructions">
    <h3>Instructions</h3>
    <p>Choose files, data or layers to import from your computer, which will become temporarily available on the map.</p>
    <p>Supported file types include: geojson, csv, xlsx, kml, shapefiles (shp, dbf, prj)</p>
    <p>
      Imported files require a location in order to be displayed. The supported coordinated system is decimal
      degrees longitude/latitude (WGS84). For example, -127.10205, 51.81051
    </p>
    <p>Large or complex files may impact performance. A message will indicate if the file has been successfully imported.</p>
    <h3>CSV and Excel</h3>
    <p>
      For CSV and Excel, the files should have two columns with the headings (not case sensitive):
      "Latitude" and "Longitude" or "lat" and "long". It works best to import an Excel workbook that has a table on
      the first sheet (and no other cells filled in outside the table).
    </p>
    <h3>Shapefile</h3>
    <p>
      Shapefiles must include both the .shp and .prj. Importing the .dbf is also recommended if you want to view features and properties of the layer.
    </p>
  </div>
</template>
<script>
export default {
  name: 'ImportLayerInstructions'
}
</script>
<style lang="scss">
</style>
