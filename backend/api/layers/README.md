# layers

The layers module contains database models for simple layers (e.g. one table) that we store
in the Wally database. These layers generally come from the DataBC Geographic Warehouse.

Many of the individual layer models in this folder are deprecated as WALLY uses the DataBC WFS
service whenever possible.  The exceptions are Freshwater Atlas streams and watersheds layers.

# Adding a new layer to WALLY

[Here is an example of the SQL used to create a new layer](../../alembic/versions/20200810025228_add_licensed_works_layer.py).
It is recommended to create a new migration and have the migration load the layer on staging and prod.
As soon as the layer is loaded, it should show up as a toggle-able layer in WALLY.

# Loading FWA layers

WALLY uses FWA layers to do queries for streams and watersheds.  If you want the upstream/downstream
and surface water features to work locally across the Province, load the FWA layers below.

## FWA Stream Networks

Use the GeoBC FTP site at ftp://ftp.geobc.gov.bc.ca/sections/outgoing/bmgs/FWA_Public to get the FWA
Stream Networks and FWA Watersheds layers.

You may need to update the commands below depending on what
version you download.  The destination table names e.g. `-nln freshwater_atlas_watersheds` won't change, just
the source filenames.

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"./FWSTRMNTWR_line.shp" \
--config PG_USE_COPY YES \
-nln freshwater_atlas_stream_networks -progress
```

## FWA Watersheds

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"./FWA_WATERSHEDS_POLY.geojson" \
--config PG_USE_COPY YES \
-nln freshwater_atlas _watersheds -progress
```
