# Wally OpenShift templates
This folder contains templates for building and deploying Wally to OpenShift.

## Folders

`apitest` - contains a Dockerfile for an image that can be used to run API tests in the Jenkins pipeline.

`cleanup` - contains cleanup scripts used by Jenkins to tear down PR environments when PRs are merged/closed.
This script should be run by a Jenkins github webhook trigger.

`patroni-postgis` - contains a Dockerfile and pre-req resources (one time deployment to OpenShift) for using Patroni
in OpenShift. This folder contains the image's files; the actual deployment of a Postgres cluster (with Patroni)
is through the `database.deploy.yaml` template.

## Files

`backend.build.yaml` - BuildConfig and ImageStream for Wally's Python backend.

`backend.deploy.yaml` - DeploymentConfig for Wally's Python backend.  It requires the image produced by 
the `backend.build.yaml` template.

`database.deploy.yaml` - StatefulSet deployment for Wally's Postgres database.  It uses an image that includes PostGIS
for spatial data handling and Patroni for helping to manage the Postgres cluster's failover replicas. The resources in the
`patroni-postgis/` folder are pre-requisite for deployment.

`frontend.build.yaml` - BuildConfig and ImageStream for Wally's Vue web app and the nginx server that serves it.

`frontend.deploy.yaml` - DeploymentConfig that deploys the nginx server and static files produced by the web app build.
