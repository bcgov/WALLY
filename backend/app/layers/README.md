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
-nlt PROMOTE_TO_MULTI -nln parcel -append
```

Since the parcels dataset is 2 GB, there is also a FactoryBoy class (ParcelFactory) in parcel_factory.py for generating dev fixtures.
