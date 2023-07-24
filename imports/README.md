# Import Scripts

## Downloading geojson files

Shell script to download geojson files from the Data Catalogue

```bash
$ bash download_geojson_info.sh <email_address_to_send_to>
``` 

Update the `geojson_request.json` for less, or more layers. With the current settings it takes around 4 hours to receive an email that your order is ready for download. It comes as a .zip file that's around 4GB



----
## Use tippecanoe to generate the tiles for a specific layer 

`$  brew install tippecanoe`

```bash
tippecanoe -o stream_restrictions.mbtiles -zg --drop-densest-as-needed  WLS_STREAM_RESTRICTIONS_SP.geojson
```

Then upload the .mbtiles file onto mapbox studio

---
## Load geojson into the database
To load data into the database, use `ogr2ogr` which is part of the GDAL (Geospatial Data Abstraction Library)

`$ brew install gdal`

```bash
$ ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/full/path/to/parcels.geojson" \
--config PG_USE_COPY YES \
-nlt PROMOTE_TO_MULTI -nln parcel -append
```
