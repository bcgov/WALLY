# Fixture extents
These small shapefiles contain boundaries in both EPSG:3005 and EPSG:4326 that represent an
approximate boundary for the local/dev fixture extents.  They don't necessarily represent
the actual extent of all fixture data.

Use them to create new fixtures, for example:

```
# create new `stream_networks_fixture.shp` using input file `fwa_stream_networks_sp.shp`
# and clipping to `fixture_extent_3005.shp`.
# Make sure you use the right extent for the input file's projection.
ogr2ogr -f "ESRI Shapefile" -clipsrc fixture_extent_3005.shp stream_networks_fixture.shp fwa_stream_networks_sp.shp
```
