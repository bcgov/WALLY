# Migrating from OCP3 to OCP4

Note: These are the steps required to stand up WALLY from scratch on OCP4, but many of these steps are not OCP4 specific (e.g. they should have been documented for OCP3 too...).

# Prerequisites for TOOLS/DEV/TEST/PROD namespaces

Most resources that need to be created in the environments but are not stored in templates in the repo (such as secrets) can be retrieved from OCP3 using `oc get secret wally-at-github -o yaml`.

## Create or import secrets

### tools namespace
* wally-at-github (GitHub SSH key)
* wally-github-token (GitHub token)
* apitest-test-creds (test account for CI/CD API tests)

## Import images

The following external/community images don't have BuildConfigs and need to be imported:
Example import command: `oc4 -n d1b5d2-tools import-image --from=python:3.7 python:3.7 --reference-policy=local --confirm`

* `python:3.7`
* `crunchy-postgres-gis:centos8-13.2-3.0-4.6.2` - note: this image was not used for Wally on OpenShift 3. It's new for OCP4.  Database templates in openshift/ocp4/ will be updated to reflect this new image.
* `promtail:v1.3.0` - Log exporter for Loki

## Set up NetworkPolicy

* there is a quickstart set of NetworkPolicies, see `quickstart-network-policy.yaml`. Must be applied to each namespace.
* TODO: set finer grained rules.
