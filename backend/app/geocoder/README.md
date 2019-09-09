# geocoder

The geocoder module provides API endpoints and database functions for searching for parcels.  This can be extended to wells, aquifers, and other features as needed.

# loading parcels

To load parcels, use `ogr2ogr`.

```bash
ogr2ogr -f "PostgreSQL" PG:"dbname=wally user=wally host=localhost port=5432 password=test_pw" \
"/full/path/to/parcels.geojson" \
--config PG_USE_COPY YES \
-nlt PROMOTE_TO_MULTI -nln parcel -append
```
