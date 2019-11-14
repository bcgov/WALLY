# layers

The layers module contains database models for simple layers (e.g. one table) that we store
in the Wally database. These layers generally come from the DataBC Geographic Warehouse.

# Adding a new layer to WALLY

The following list shows all the steps required to integrate a fully functional new data 
layer into the Wally application.

1. Download raw data in geojson from DataBC
2. Create the Database Model in /app/layers/ (file named with the table name)
3. Create the Alembic migration to create the table in the database along with any metadata
    - metadata tables: vector_catalogue, data_source, display_catalogue
    (example in this migrations /alembic/versions/a2b8d50d796d_add_water_applications.py)
4. Create Production Mapbox layer - In the iit-water mapbox account, add the new layer and 
    design it in the Wally Production style
8. Create Testing Mapbox layer (Whistler Subset) - take a subset of the data around 
    Whistler BC, and upload it to mapbox and create the layer in the
    Wally Testing - Whistler style

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

## Wells

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/path/to/ground_water_wells.geojson" \
--config PG_USE_COPY YES \
-nln ground_water_wells -progress
```
