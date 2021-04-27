#!/bin/bash
# Usage: ./deploy_redirect.sh <namespace> <environment>
# Sample usage: 
#    ./deploy_redirect.sh bfpeyx-dev dev
#    ./deploy_redirect.sh bfpeyx-test staging
#    ./deploy_redirect.sh bfpeyx-prod prod

PROJECT=${1:-}
ENV=${2:-}

# Destination will be the URL in the silver cluster
DEST_URL=wally.nrs.gov.bc.ca
NAME_SUFFIX=''

if [ "$ENV" != 'prod' ]; then
  NAME_SUFFIX="-$2"
  DEST_URL=wally${NAME_SUFFIX}.apps.silver.devops.gov.bc.ca
fi
DC_TMPL=redirect.dc.yaml


# Source is the URL from pathfinder
SOURCE_URL=wally-redirect${NAME_SUFFIX}.pathfinder.gov.bc.ca

# Process deployment config
oc -n $PROJECT process -f $DC_TMPL -p NAME_SUFFIX=$NAME_SUFFIX DESTINATION_HOST_NAME=$DEST_URL SOURCE_HOST_NAME=$SOURCE_URL | oc -n $PROJECT apply -f - 
