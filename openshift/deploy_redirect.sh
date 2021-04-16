#!/bin/bash
# Usage: ./deploy_redirect.sh <namespace> <environment>
# Sample usage: 
#    ./deploy_redirect.sh bfpeyx-dev dev
#    ./deploy_redirect.sh bfpeyx-staging staging
#    ./deploy_redirect.sh bfpeyx-prod

PROJECT=${1:-}
ENV=${2:-}
NAME_SUFFIX="-$2"
DC_TMPL=redirect.dc.yaml

# Destination will be the URL in the silver cluster
# Will change this to wally${NAME_SUFFIX}.apps.silver.devops.gov.bc.ca
DEST_URL=apps.nrs.gov.bc.ca

# Source is the URL from pathfinder
SOURCE_URL=wally-redirect${NAME_SUFFIX}.pathfinder.gov.bc.ca

# Process deployment config
oc -n $PROJECT process -f $DC_TMPL -p NAME_SUFFIX=$NAME_SUFFIX DESTINATION_HOST_NAME=$DEST_URL SOURCE_HOST_NAME=$SOURCE_URL | oc apply -f - 
