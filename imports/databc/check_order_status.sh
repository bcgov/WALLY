#!/bin/bash

# Check for an order to become available
# USAGE: ./check_order_status.sh <order_id>

set -e
ORDER_ID="$1"

[ -z $ORDER_ID ] && echo "Order ID is required. Usage: check_order_status.sh <order_id>" && exit 1

echo "Waiting for order $ORDER_ID to become available"

while true; do
  ((i++)) && ((i==300)) && echo "Exceeded loop limit ($i) without download link becoming available." && exit 1
  echo "Checking status of order $ORDER_ID..."
  link=$(curl -s https://apps.gov.bc.ca/pub/dwds-ofi/order/$ORDER_ID | jq -r '.ORDER_DOWNLOAD_PATH')
  [[ ! -z "$link" ]] && echo "Download link: $link" && break
  echo "Order not ready yet. Checking again in 15 seconds..."
  sleep 15
done
