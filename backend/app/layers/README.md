# layers

The layers module contains database models for simple layers (e.g. one table) that we store
in the Wally database. These layers generally come from the DataBC Geographic Warehouse.

## Cadastral/Parcels

https://catalogue.data.gov.bc.ca/dataset/parcelmap-bc-parcel-fabric

To load parcels, use `ogr2ogr`.

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/full/path/to/parcels.geojson" \
--config PG_USE_COPY YES \
-nlt PROMOTE_TO_MULTI -nln cadastral -append
```

## Aquifers

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/path/to/aquifers.geojson" \
--config PG_USE_COPY YES \
-nlt PROMOTE_TO_MULTI -nln ground_water_aquifers
```

## Water Rights Licences

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/path/to/water_rights.geojson" \
--config PG_USE_COPY YES \
-nln water_rights_licenses
```
