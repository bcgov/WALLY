# Migrating from OCP3 to OCP4

Note: These are the steps required to stand up WALLY from scratch on OCP4, but many of these steps are not OCP4 specific (e.g. they should have been documented for OCP3 too...).

# Prerequisites for TOOLS/DEV/TEST/PROD namespaces

Most resources that need to be created in the environments but are not stored in templates in the repo (such as secrets) can be retrieved from OCP3 using `oc get secret wally-at-github -o yaml`.

## Create or import secrets/configmaps

### Tools namespace
#### Secrets
* wally-at-github (GitHub SSH key)
* wally-github-token (GitHub token)
* apitest-test-creds (test account for CI/CD API tests)

### Dev namespace
#### Secrets
* common-docgen
* wally-psql
* minio
* keycloak-config
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config


### Test

#### Secrets
* common-docgen
* wally-psql
* minio
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config
* wally-staging-grafana
* wally-staging-grafana-cfg
* wally-staging-grafana-dashboards
* wally-staging-grafana-datasources
* wally-grafana-notifiers
* wally-staging-prometheus
* apitest-monitors

### Prod

#### Secrets
* common-docgen
* wally-psql
* minio
* gatekeeper-credentials
* wally-debug
* mapbox-access-token

#### ConfigMaps
* gatekeeper-config
* promtail-config
* loki-config
* wally-config
* wally-grafana
* wally-grafana-cfg
* wally-grafana-dashboards
* wally-grafana-datasources
* wally-grafana-notifiers
* wally-prometheus
* apitest-monitors

## Import images

The following external/community images don't have BuildConfigs and need to be imported:
Example import command: `oc4 -n d1b5d2-tools import-image --from=python:3.7 python:3.7 --reference-policy=local --confirm`

* `python:3.7`
* `crunchy-postgres-gis:centos7-12.5-3.0-4.4.2` - note: this image was not used for Wally on OpenShift 3. It's new for OCP4.  Database templates for this new image are in openshift/ocp4/crunchy-postgres .
* `promtail:v1.3.0` - Log exporter for Loki
* `apitest` - Warning: technical debt: this image needs a BuildConfig to be built using source code from github.com/stephenhillier/apitest onto a Red Hat Jenkins agent image.  The current image was transferred from OCP3.

Refer to https://github.com/BCDevOps/OpenShift4-Migration/issues/51 for instructions on how to enable pull secrets for builds using Docker Hub images.

## Set up NetworkPolicy

* there is a quickstart set of NetworkPolicies, see `quickstart-network-policy.yaml`. Must be applied to each namespace.
* TODO: set finer grained rules.
