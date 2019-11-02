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
LAYER_NAME='WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW'
LAYER_DESC='Ground Water Aquifers'
LAYER_URL='https://catalogue.data.gov.bc.ca/dataset/ground-water-aquifers'
PAYLOAD_URL="https://apps.gov.bc.ca/pub/dwds-ofi/public/order/createOrderFiltered/"

PAYLOAD=$(<geojson_request.json)
PAYLOAD=${PAYLOAD/<email_address>/$EMAIL}
PAYLOAD=${PAYLOAD/<layer_name>/$LAYER_NAME}
PAYLOAD=${PAYLOAD/<layer_desc>/$LAYER_DESC}
PAYLOAD=${PAYLOAD/<layer_url>/$LAYER_URL}

curl -Ls -H 'Content-Type: application/json' --data "$PAYLOAD" $PAYLOAD_URL

# ORDER_ID=$(curl -Ls -H 'Content-Type: application/json' --data "$PAYLOAD" $PAYLOAD_URL)
# echo "$ORDER_ID"
# ORDER_ID=$(echo $ORDER_ID | jq -r ".Value")

# echo "Order $ORDER_ID placed. Waiting for download to become available"

# declare -a link

# while true; do
#   link=$(curl -s https://apps.gov.bc.ca/pub/dwds-ofi/order/2038490 | jq -r '.ORDER_DOWNLOAD_PATH')
#   [ -z "$link" ] && break
# done
