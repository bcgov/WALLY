# National Water Data Archive - Hydrometric Data

Stream flow and water level data collected at monitoring stations.

## Source

https://www.canada.ca/en/environment-climate-change/services/water-overview/quantity/monitoring/survey/data-products-services/national-archive-hydat.html


## How to load data on local machine

Download `Hydat.sqlite3` from the above link.

Download `pgloader` (available on Homebrew).

Make sure that the Wally app is running with `docker-compose up`.

Edit the following command and use it to load the data:
```sh
pgloader \
    --type sqlite \
    --with "create no tables" \
    --with "truncate" \
    --set "search_path='hydat'" \
    /path/to/Hydat.sqlite3 \
    postgres://wally:test_pw@localhost:5433/wally
```

Note: `wally:test_pw` is the default postgres user/password for the postgres container (for local development only).

## Files in this folder

### db.py: database access

Database models and data access functions are located in `db.py`.

### endpoints.py: API endpoints and endpoint handlers

Endpoint handlers are located in `endpoints.py`.
These endpoints are imported into the router at `/backend/app/router.py` and loaded by the main API application.

### models.py: API data models

The API data models and schemas are located in `models.py`. These models describe the data format returned by the API endpoints in `endpoints.py`.
When running the development stack with docker compose, see the Swagger documentation located at http://localhost:8000/docs.
