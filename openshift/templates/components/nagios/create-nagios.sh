#!/usr/bin/env bash
## create base image in (Wally) bfpeyx-tools project
oc process -f ./nagios-base-bc.json | oc create -f -

## create nagios image in three environment
oc process -f ./nagios-sa.json | oc create -f -
#oc process -f ./nagios-sa.json | oc create -f -
#oc process -f ./nagios-sa.json | oc create -f -

## grant build to pull image from tools project, as nagios uses nagios-base image which is in tools project
#oc policy add-role-to-user system:image-puller system:serviceaccount:bfpeyx-dev:builder --namespace=bfpeyx-tools
oc policy add-role-to-user system:image-puller system:serviceaccount:bfpeyx-test:builder --namespace=bfpeyx-tools
#oc policy add-role-to-user system:image-puller system:serviceaccount:bfpeyx-prod:builder --namespace=bfpeyx-tools

## create nagios image in three environment
#oc process -f ./nagios-bc.json ENV_NAME=dev | oc create -f -
oc process -f ./nagios-bc.json ENV_NAME=test | oc create -f -
#oc process -f ./nagios-bc.json ENV_NAME=prod | oc create -f -

## grant service account nagios edit role otherwise check replica will fail
#oc policy add-role-to-user edit system:serviceaccount:bfpeyx-dev:nagios -n bfpeyx-dev
oc policy add-role-to-user edit system:serviceaccount:bfpeyx-test:nagios -n bfpeyx-test
#oc policy add-role-to-user edit system:serviceaccount:bfpeyx-prod:nagios -n bfpeyx-prod

## tag image
#oc tag nagios:latest nagios:dev -n bfpeyx-dev
oc tag nagios:latest nagios:test -n bfpeyx-test
#oc tag nagios:latest nagios:prod -n bfpeyx-prod

## create nagios dc in three environment
#oc process -f ./nagios-dc.json ENV_NAME=dev KEYCLOAK_CLIENT_ID=gwells KEYCLOAK_SA_REALM=gwells
#-dev KEYCLOAK_SA_CLIENT_ID=wally-service-dev \
#KEYCLOAK_SA_BASEURL=https://sso-dev.pathfinder.gov.bc.ca KEYCLOAK_REALM=https://sso-dev.pathfinder.gov.bc.ca/auth/realms/gwells \
#SMTP_SERVER_HOST=apps.smtp.gov.bc.ca| oc create -f - -n bfpeyx-dev
oc process -f ./nagios-dc.json ENV_NAME=test KEYCLOAK_CLIENT_ID=gwells KEYCLOAK_SA_REALM=gwells KEYCLOAK_SA_CLIENT_ID=wally-service-test \
KEYCLOAK_SA_BASEURL=https://sso-test.pathfinder.gov.bc.ca KEYCLOAK_REALM=https://sso-test.pathfinder.gov.bc.ca/auth/realms/gwells \
SMTP_SERVER_HOST=apps.smtp.gov.bc.ca| oc create -f - -n bfpeyx-test
# oc process -f ./nagios-dc.json ENV_NAME=prod KEYCLOAK_CLIENT_ID=gwells KEYCLOAK_SA_REALM=gwells KEYCLOAK_SA_CLIENT_ID=wally-service \
# KEYCLOAK_SA_BASEURL=https://sso.pathfinder.gov.bc.ca KEYCLOAK_REALM=https://sso.pathfinder.gov.bc.ca/auth/realms/gwells \
# SMTP_SERVER_HOST=apps.smtp.gov.bc.ca| oc create -f - -n bfpeyx-prod



