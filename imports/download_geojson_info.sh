#!/bin/bash

# Send a request for geoJSON layers from NRS Apps
# Emails get sent to the email address on geojson_request.json
# USE THIS WISELY


# Order 2031571
# https://apps.gov.bc.ca/pub/dwds-rasp/pickup/2031571
# https://distribution.data.gov.bc.ca/BCGW_7113060B_156885004189_7212.zip

EMAIL=$1

[ -z "$EMAIL" ] && echo "You need to provide an email address" && exit 1

PAYLOAD_URL="https://apps.gov.bc.ca/pub/dwds-ofi/public/order/createOrderFiltered/"

PAYLOAD=$(<geojson_request.json)
PAYLOAD=${PAYLOAD/<email_address>/$EMAIL}
COMMAND="curl -L -i -X POST -H 'Content-Type: application/json' -d '$PAYLOAD' $PAYLOAD_URL"

echo "-------------------------------"
echo $COMMAND
echo "-------------------------------"

while true; do
    read -p "Run the command? " yn
    case $yn in
        [Yy]* ) eval $command; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

