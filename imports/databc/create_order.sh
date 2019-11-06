#!/bin/bash

# Send a request for geoJSON layers from NRS Apps
# Emails get sent to the email address on geojson_request.json
# USE THIS WISELY


# Order 2031571
# https://apps.gov.bc.ca/pub/dwds-rasp/pickup/2031571
# https://distribution.data.gov.bc.ca/BCGW_7113060B_156885004189_7212.zip

set -e

# temporary, just for testing
EMAIL="gwells@gov.bc.ca"
LAYER_NAME='WHSE_BASEMAPPING.FWA_STREAM_NETWORKS_SP'
LAYER_DESC=''
LAYER_URL=''
PAYLOAD_URL="https://apps.gov.bc.ca/pub/dwds-ofi/public/order/createOrderFiltered/"

PAYLOAD=$(<geojson_request.json)
PAYLOAD=${PAYLOAD/<email_address>/$EMAIL}
PAYLOAD=${PAYLOAD/<layer_name>/$LAYER_NAME}
PAYLOAD=${PAYLOAD/<layer_desc>/$LAYER_DESC}
PAYLOAD=${PAYLOAD/<layer_url>/$LAYER_URL}

# curl -Ls -H 'Content-Type: application/json' --data "$PAYLOAD" $PAYLOAD_URL

ORDER=$(curl -Ls -H 'Content-Type: application/json' --data "$PAYLOAD" $PAYLOAD_URL)
echo "$ORDER"
STATUS=$(echo "$ORDER" | jq .Status)
echo $STATUS
[[ $STATUS = '"FAILURE"' ]] && echo "Failed: $(echo $ORDER | jq .Description)" && exit 1

ORDER_ID=$(echo "$ORDER" | jq .Value)
echo "Order placed: $ORDER_ID"
