#!/bin/bash

# Send a request for geoJSON layers from NRS Apps
# Emails get sent to the email address on geojson_request.json

payload_url="https://apps.gov.bc.ca/pub/dwds-ofi/public/order/createOrderFiltered/"

test="hello"
PAYLOAD=$(<geojson_request.json)
command="curl -L -i -X POST -H 'Content-Type: application/json' -d '$PAYLOAD' $payload_url"
echo $command

eval $command

