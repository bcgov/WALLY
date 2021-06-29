#!/bin/bash
set -euxo pipefail

LATEST_HYDAT="${LATEST_HYDAT:-Hydat_sqlite3_20210510}"
PGLOADER_LOG_DIR="${PGLOADER_LOG_DIR:-'/tmp/pgloader'}"
cd /tmp

if [ ! -f "/tmp/$LATEST_HYDAT.zip" ]; then
    curl "https://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/$LATEST_HYDAT.zip" -O
fi

unzip /tmp/$LATEST_HYDAT.zip -d /tmp && \
mkdir -p "${PGLOADER_LOG_DIR}" && \
pgloader \
    -L "${PGLOADER_LOG_DIR}/pgloader.log" -D "${PGLOADER_LOG_DIR}" \
    --type sqlite \
    --with "create no tables" \
    --with "truncate" \
    --set "search_path='hydat'" \
    /tmp/Hydat.sqlite3 \
    postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB && \
psql "postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB" -w -c "update hydat.stations set geom=ST_SetSrid(ST_MakePoint(longitude, latitude), 4326);" && \

# transform HYDAT data into something resembling time series (station : date : value)
# and load into the `fasstr.fasstr_flows`
psql "postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB" << EOF
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
EOF

rm "/tmp/$LATEST_HYDAT.zip" && \
rm /tmp/Hydat.sqlite3
