#!/bin/bash
curl https://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/Hydat_sqlite3_20210116.zip -o /tmp/hydat.zip && \
unzip /tmp/hydat.zip -d /tmp && \
mkdir -p /dataload/pgloader && \
pgloader \
    -L /dataload/pgloader/pgloader.log -D /dataload/pgloader \
    --type sqlite \
    --with "create no tables" \
    --with "truncate" \
    --set "search_path='hydat'" \
    /tmp/Hydat.sqlite3 \
    postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB

psql "postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB" -w -c "update hydat.stations set geom=ST_SetSrid(ST_MakePoint(longitude, latitude), 4326);"
