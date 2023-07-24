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

## How to populate fasstr_flows

```sql
  with flows as (
    select
      f.station_number,
      year,
      month,
      flow1,
      flow2,
      flow3,
      flow4,
      flow5,
      flow6,
      flow7,
      flow8,
      flow9,
      flow10,
      flow11,
      flow12,
      flow13,
      flow14,
      flow15,
      flow16,
      flow17,
      flow18,
      flow19,
      flow20,
      flow21,
      flow22,
      flow23,
      flow24,
      flow25,
      flow26,
      flow27,
      flow28,
      flow29,
      flow30,
      flow31
    from hydat.dly_flows f
    inner join hydat.stations s on s.station_number = f.station_number
    where s.prov_terr_state_loc = 'BC'
  ),
  kv as (
    select station_number, year, month, each(hstore(flows)) as kv from flows
  )
  insert into fasstr.fasstr_flows (station_number, date, value)
  select
    station_number,
    to_date(concat(year::text, lpad(month::text, 2, '0'), lpad(replace((kv).key, 'flow', '')::text, 2, '0')), 'YYYYMMDD') as date,
    (kv).value::numeric as value
  from kv where (kv).key like 'flow%' and (kv).value is not null;
  ```

## Files in this folder

### db.py: database access

Database models and data access functions are located in `db.py`.

### endpoints.py: API endpoints and endpoint handlers

Endpoint handlers are located in `endpoints.py`.
These endpoints are imported into the router at `/backend/app/router.py` and loaded by the main API application.

### models.py: API data models

The API data models and schemas are located in `models.py`. These models describe the data format returned by the API endpoints in `endpoints.py`.
When running the development stack with docker compose, see the Swagger documentation located at http://localhost:8000/docs.
