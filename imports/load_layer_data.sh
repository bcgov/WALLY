#!/bin/bash
# first call port forward: 
# oc port-forward wally-psql-staging-0 5432:5432
# then call this script in the directory with the properly named geojson files that match the db tables
# call this script with one parameter which matches the db password
for filename in *.geojson; do
    echo "loading" $filename
    SECONDS=0
    [ -e "$filename" ] || continue
        name=${filename%%.*}
        ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 dbname=wally user=wally password=$1" $filename -nln $name -append -progress -skipfailures --config OGR_TRUNCATE YES --config PG_USE_COPY YES
    duration=$SECONDS
    echo "Import Time: $(($duration / 60)) minutes and $(($duration % 60)) seconds."
done