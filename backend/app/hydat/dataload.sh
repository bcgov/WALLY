curl http://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/Hydat_sqlite3_20190717.zip -o /tmp/hydat.zip && \
unzip /tmp/hydat.zip && \
pgloader \
    --type sqlite \
    --with "create no tables" \
    --with "truncate" \
    --set "search_path='hydat'" \
    /tmp/Hydat.sqlite3 \
    postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_SERVER:5432/$POSTGRES_DB
