# July 2026 - Openshift Deprecation Notice Refactor

The purpose of these release notes are to serve as a source of truth and discussion for updates made to the deployment patterns of this application in response to the BCGov Platforms Team notice of DeploymentConfig Objects becoming deprecated in Openshift 4.14.

To summarize, the goal of this refactor is to instead build standard Deployment Objects, move away from Openshift Templates and Jenkins Pipelines in favour of Helm Charts and Github Actions as per [BCGov Quickstart Openshift V2.0.0](https://github.com/bcgov/quickstart-openshift/tree/v2.0.0).

## Initial Issues - Build

### Whitebox Tools

WhiteboxTools becoming a tool that is no longer available for the public to use has prevented my ability to build and test this application locally out of the box.

To get around this, I authenticated to the openshift cluster' container registry, pulled the latest whitebox tools image from a previous build, and retagged to a local image.

```bash
# Get Token via Copy Login Command from console
oc login --token=************** --server=https://api.silver.devops.gov.bc.ca:6443
ocn d1b5d2-tools
oc whoami -t | docker login -u unused --password-stdin image-registry.apps.silver.devops.gov.bc.ca
docker pull image-registry.apps.silver.devops.gov.bc.ca/d1b5d2-tools/whiteboxtools:latest
docker tag image-registry.apps.silver.devops.gov.bc.ca/d1b5d2-tools/whiteboxtools:latest whitebox-builder:legacy-2023
```

After tagging and building a whitebox-tools image on your local machine, all development Dockerfiles can be updated to reference the `whitebox-builder:legacy-2023` image, and replace the previous `builder` step.

```bash
ARG DOCKER_TAG=latest

FROM whitebox-builder:legacy-2023 AS builder

FROM python:3.7

COPY --from=builder /wbt/target/x86_64-unknown-linux-musl/release/whitebox_tools /usr/local/bin/

...

```

Replacing:

```bash
ARG DOCKER_TAG=latest

FROM rust:latest AS builder

RUN apt-get update && apt-get install -y musl-tools git && \
  rustup target add x86_64-unknown-linux-musl && \
  git clone https://github.com/jblindsay/whitebox-tools.git /wbt
  # NOTE: this branch no longer exists
  # && cd /wbt && git checkout d8_flow_accum-fix

WORKDIR /wbt

RUN cargo build --release --target x86_64-unknown-linux-musl

FROM python:3.7

COPY --from=builder /wbt/target/x86_64-unknown-linux-musl/release/whitebox_tools /usr/local/bin/

...

```

Please see Dockerfile.dev.2026 for reference.

## Docker Compose

The only issues I encountered with the current Docker Compose file are that the database will not mount if a developer has postgres running locally.

As this is common for developers, I recommend port-fortwarding the DB service to `6432`. This does not impact the application running locally in any way.

I was able to get the application running pretty seamlessly via:

```bash
export MAPBOX_ACCESS_TOKEN=pk.eyxxxxxxxxxxxxx
export MAPBOX_STYLE=mapbox://styles/yourorg/xxxxx
docker compose -f docker-compose.2026.yml build
docker compose -f docker-compose.2026.yml up
```

*NOTE* - I am on a Linux machine. I imagine the same `{PLATFORM}` block would need to be added, and updates to the initial Dockerfile for the various Mac builds would need to be replicated.

## Github Actions - Deploy

### Whitebox Tools

Similiarily to what has been found locally, an action needs to be made to copy the `whitebox-tools` image from the openshift container registry to GHCR.

I am making a github action
