# Water Allocation Data Library

1. [Working on WALLY (Getting started)](#working-on-wally-getting-started)
2. [Application architecture](#application-architecture)
3. [Building & Deploying](#building--deploying)
4. [Feature-specific documentation](#feature-specific-documentation)
5. [Contributing / Code of Conduct](#contributing)

## Working on WALLY (Getting started)

WALLY runs locally using docker-compose (for the backend stack) and node (for the frontend web app development server).  The local environment
includes fixtures that cover the Whistler, BC area.

### Prerequisites

* Docker
* Node v22

#### Environment variables

Running WALLY locally requires the following env vars:

`MAPBOX_ACCESS_TOKEN` (required): a token from mapbox.com for making Mapbox API requests (e.g. requesting tiles and map images).

#### Feature flags

The backend uses [Pydantic's settings management](https://github.com/bcgov-c/wally/blob/0dc732c241bff5e8d8ce72d40ab88b9286e4566c/backend/api/config.py#L61-L82)
Create a file called `dev.env` under `backend/.config/` to test your feature flags and other settings.

### Running the backend services

> **This is currently broken.**  The stack comes up, but the backend exits during startup when it tries to upload raster fixtures to Minio.
> See [Local development and Minio](#local-development-and-minio) below for what's wrong and where to start looking.

Start the backend API and database stack with Docker Compose:

```bash
docker-compose up -d
```

This will start up Wally's Python backend, PostGIS, and Minio services.

Database fixtures will be loaded automatically using the `backend/api/initial_data.py` script. Raster fixtures are also
automatically copied to the Minio container. This script is only run on local and PR dev environments.

When building locally use the following command for logging into Artifactory private registry:

```bash
docker login -u <svc-usn> -p <svc-pwd> artifacts.developer.gov.bc.ca/wd1b-wbt-docker-local
```

Replace svc-usn and svc-pwd with Artifactory service account credentials obtained from Openshift (under ally-tools secrets)

To build and run the backend on computers with Apple M1 chip use the following command:

```bash
PLATFORM=.m1 docker-compose build --pull --no-cache --progress=plain backend && docker compose up -d
PLATFORM=.m1v2 docker-compose build --pull --no-cache --progress=plain backend && docker compose up -d
```

For an Apple computer with an M3 chip, use the .m1v2 version.

### Local development and Minio

**docker-compose is currently broken**, and the cause is Minio.

The `minio/minio` image was removed from Docker Hub on September 16th, and pulling it now fails with
`pull access denied for minio/minio, repository does not exist or may require 'docker login'`.  The compose file previously pinned
`minio/minio:RELEASE.2021-04-22T15-44-28Z`, which is no longer obtainable.

As a stopgap, a copy of WALLY's own Minio image has been preserved at `ghcr.io/bcgov/wally/minio` and the compose file now points at that.  This image is
the one built for OpenShift (with `minio-entrypoint.sh` and `MINIO_DATA_DIR=/opt/minio/s3/data`) rather than the stock upstream image local dev used to run,
so the two are not drop-in equivalents:

* The data directory is `/opt/minio/s3/data`, not `/data`.
* Minio refuses to start if anything is mounted *inside* its export path, so the raster fixtures can no longer be bind-mounted straight into
  `.../data/raster` the way they used to be.
* The backend currently fails on startup with `minio.error.AccessDenied` when `initial_data.py` tries to upload the raster fixtures.  The root credentials
  are accepted for listing buckets but denied for writes and all admin operations, which is not yet explained.

The same image and the same Minio release (`RELEASE.2025-09-07T16-13-09Z`) work correctly on staging and production, so this appears to be specific to the
local compose configuration rather than the image itself.  **If you are picking this up, start by diffing the compose Minio service against the deployed
Minio Deployment in the Helm chart** — env var names, command/args, and volume layout — rather than assuming credentials are wrong.

Everything else in the local stack (Postgres, Alembic migrations, fixture loading, pg_tileserv) comes up correctly.

#### Access the database directly

The database is exposed at `localhost:5432`.  For a shortcut to launch the psql client, use:

```sh
make psql
```

#### Browse the backend API documentation

The backend's Swagger API documentation is available at <http://localhost:8000/docs>.

### Running the frontend web app

Start the frontend development server:

```bash
cd frontend
npm install
npm run serve
```

The frontend will be deployed at <http://localhost:8080/>.  It requires the backend docker-compose stack to also be running.

## Application architecture

Wally is deployed as a group of services:

* `frontend/` (Vue app served by nginx) - The frontend folder contains Wally's web app and a Dockerfile for an nginx service that serves the built assets in the `dist` folder.
nginx also proxies requests to other services based on the `nginx.conf` ConfigMap defined in the Helm chart.  Requests are authenticated against BC Gov's
Keycloak SSO (`loginproxy.gov.bc.ca`); the Luketo Proxy (Gatekeeper) service that used to front the app is no longer deployed.

* `backend/` (FastAPI Python backend) - the backend folder contains the REST API backend that serves data at the `/api/v1/` path.

* PostGIS - Data used by Wally is stored in a PostGIS-enabled PostgreSQL database, now managed by the
[Crunchy Postgres Operator (PGO)](https://access.crunchydata.com/documentation/postgres-operator/latest/) rather than the hand-rolled Patroni setup that used
to live in `openshift/patroni-postgis`.  PGO handles replication, connection pooling (PgBouncer), users, and generated credentials.
PostGIS is used for querying the Freshwater Atlas and HYDAT data as well as storing user project data.

* Minio - WALLY uses Minio to host spatial data raster files, store Freshwater Atlas data, and store uploaded user files.  Configuration is in the Helm chart
under `charts/app`.

* Matomo + MariaDB - WALLY's analytics stack.  Matomo runs as a two-container Deployment (the Matomo PHP-FPM app plus an nginx proxy sidecar built from
`matomoproxy`), backed by a MariaDB Deployment with its own PVC.  Matomo's first-time setup (database connection, super user) is completed through Matomo's
own web installer; the credentials it needs are generated into Kubernetes Secrets by the chart.

### WALLY and OpenShift

WALLY runs on BCGov's OpenShift 4 platform.  All resources are now plain Kubernetes/OpenShift objects (`Deployment`, `Service`, `Route`, `NetworkPolicy`)
managed by Helm charts under `charts/`.  The OpenShift `Template`, `DeploymentConfig`, `BuildConfig` and `ImageStream` objects that used to live in
`openshift/ocp4` have been retired — images are built by GitHub Actions and published to `ghcr.io` instead of being built in-cluster.

## Building & Deploying

CI/CD runs entirely in GitHub Actions.  The Jenkins pipeline (`Jenkinsfile.ocp4`) and its GitHub webhook are no longer in use.

### Pull requests (dev)

Opening or updating a pull request against `master` builds every image and deploys a full PR environment to the `dev` namespace.

Because BC Gov's Keycloak SSO requires every redirect URI to be registered ahead of time, PR environments use a **fixed pool of deployment slots**
(`wally-slot-1` … `wally-slot-N`) rather than a unique hostname per PR.  The deploy workflow claims the first free slot (or re-uses the one the PR already
holds) and comments the resulting URL on the PR.  If every slot is taken by another open PR, the workflow says so in the comment instead of deploying.
Closing the PR uninstalls the release and frees the slot.

### Staging

Merging a PR into `master` builds the `staging` tagged images and deploys them to the `test` namespace automatically.

### Production

Production is deployed by **manually dispatching** the production deploy workflow — it does not deploy on merge.  Staging and production use fixed route
hostnames rather than slots.

### Database migrations

There are two separate migration mechanisms:

* **Flyway** (init container on the backend Deployment, SQL baked into the `migrations` image) — owns everything below the application schema: extensions
(`postgis`, `postgis_topology`, `postgis_raster`, `fuzzystrmatch`, `postgis_tiger_geocoder`, `pg_stat_statements`, `pgaudit`, `plr`, `ltree`, `pg_trgm`, `hstore`),
the `postgis_ftw`, `whse_basemapping` and `fasstr` schemas, the PL/R `fasstr` functions, and the grants the application user needs to read them.
This replaces the `pgconf/setup.sql` and `/scripts/*.sql` bootstrap that used to run inside the Patroni container on first start.

* **Alembic** (`backend/alembic`) — unchanged; still owns the application's own tables, run by the backend's `prestart.sh` init container.

Flyway connects as the Crunchy-generated superuser but targets the *application* database, not the `postgres` maintenance database — an easy thing to get
wrong, since the superuser secret's `dbname` points at the latter.

### Images

Images are built by the GitHub Actions build matrix and published under `ghcr.io/bcgov/wally/`: `backend`, `frontend`, `migrations`, `minio`, `matomoproxy`,
`crunchy` (a custom Crunchy Postgres image with PL/R, R, and the `fasstr`/`Rcpp` versions pinned to match production), and the backup/restore tooling image.

Some images pull their base from BC Gov's Artifactory mirror.  Note the registry path has changed: the old
`docker-remote.artifacts.developer.gov.bc.ca/<image>` subdomain form no longer resolves (it fails TLS verification against an unrelated certificate) —
use `artifacts.developer.gov.bc.ca/docker-remote/<image>` instead, and authenticate with `docker/login-action` in the workflow.

The `whiteboxtools` builder image can no longer be rebuilt from source — the upstream workspace no longer builds cleanly and prebuilt binaries moved behind a
paywall.  The last good in-cluster build was mirrored out of the tools namespace to `ghcr.io/bcgov/wally/whiteboxtools-builder`.  Treat it as a frozen legacy
artifact rather than a reproducible build; the backend Dockerfile copies the compiled binary out of it with a multi-stage `COPY --from`.

### Data imports

> **Much of this is broken or outdated.**  The import scripts predate the current infrastructure by several years and carry a lot of drift:
> hardcoded secret names (`wally-psql`) and service hostnames (`wally-psql-${ENV_NAME}`, `http://minio:9000`) that no longer exist, deprecated
> `mc config host add` syntax (now `mc alias set`), and deprecated Artifactory registry paths.  Several layers listed in the old
> `openshift/import-jobs/README.md` were already marked as manual-only or "unknown if supported", and at least one (`ground_water_wells`)
> was already noted as not working in DataBC.  The Jobs have been converted to Helm templates, but they have not all been run end to end
> against the current infrastructure — expect to fix things as you go.
>
> **For seeding a new environment, restore from production instead.**  It is faster, more reliable, and gives you real data.  See
> [Backup and restore](#backup-and-restore) below.

The import jobs in `charts/imports` are Helm-templated Kubernetes `Job`s (converted from the old `openshift/import-jobs` Templates) and are triggered by a
`workflow_dispatch` GitHub Action.  Download and import are **separate, ordered steps** — `wfs_direct_download.sh` writes a layer's `.zip` to Minio and
`load_layer_data.sh` reads it back out later.  Running them concurrently fails with "Object does not exist".

The tile generation (`tippecanoe`) and Mapbox upload jobs have been converted as well, but are further down the dependency chain (data must be imported
before tiles can be generated, and tiles must exist before they can be uploaded) and have had the least testing of anything here.

### Backup and restore

`charts/backup-restore` contains four Jobs (backup/restore × Postgres/Minio) that move data between environments using an S3 bucket as an intermediary, so no
direct connection between namespaces is needed (PVCs cannot be mounted or cloned across namespaces).  Backups are written under a timestamped prefix so they
double as restorable point-in-time artifacts.

Two things worth knowing before running a restore:

* Bulk `pg_restore` generates a lot of WAL.  The Crunchy `walVolumeClaimSpec` needs enough headroom for the whole restore, or Postgres will PANIC and
  crash-restart partway through, leaving the target database partially restored.
* A partial restore leaves `alembic_version` present but empty, which makes Alembic think no migrations have ever run and try to recreate tables that already
  exist.  If this happens, drop and recreate the target database and restore again rather than patching around it.

## Feature-specific documentation

### Spatial data

WALLY relies on spatial raster files, in Cloud Optimized GeoTIFF format, hosted on Minio.  The files will be accessed at runtime during certain requests (to query precipitation, for example).
Querying cloud optimized geotiff files using GDAL has generally been faster (in our environment) than PostGIS and is easier to set up.

The files are in the `raster` Minio bucket on all environments.

If you need to edit or update spatial raster files, you'll need to create two files: the BC-wide file that staging and production will use,
and a Whistler area cropped version for local dev fixtures.

See [the Watersheds README](backend/api/v1/watersheds/README.md) for instructions on how to create Cloud Optimized GeoTIFF rasters for use with WALLY,
and the [fixture extents README](backend/fixtures/extents/README.md) for instructions on how to create a corresponding fixture file in the `raster` dir.

All raster fixtures in the `/backend/fixtures/raster` dir will automatically be copied to the local Minio instance when using `docker-compose`. However, for staging and production,
you must manually upload any new raster files to the staging and prod minio servers, or copy them across using the backup/restore jobs.

### Spatial layers

To add or update spatial layers in WALLY (the items in the `Layers` menu), see [the Layers API README](backend/api/layers/README.md).

### Surface Water Analysis - Watershed delineation

The Surface Water Analysis feature delineates watersheds from a point that the user drops.  This requires
Freshwater Atlas fundamental watersheds and Freshwater Atlas stream networks layers to be loaded into
the database, as well as a stream-burned DEM. See the [the Watersheds README](backend/api/v1/watersheds/README.md)
for instructions on creating the DEMs.  If you only need to demo the feature, the local environment comes with data for the Whistler area.

The stream-burned DEM needs to be loaded in Minio, and the extents of the DEM need to be loaded in
the `dem.stream_burned_cdem_tile` database table. The Surface Water Analysis feature will automatically
select the best DEM in the area based on the extents in the table.

See [the Caribou DEM extent migration](backend/alembic/versions/20210625150931_add_caribou_dem_extent.py) for an example
of loading an extent.  The shapefile that represents the DEM extent needs to be created separately.

### Province wide data

WALLY local dev environments comes with enough data to demo all features in Whistler.
To get province wide data in a local environment (or a new server environment), the following steps need to be taken:

**Load all HYDAT stations**

Use the script in `imports/hydat`.  You may need to inspect the script for required env variables (e.g. `POSTGRES_SERVER=localhost`, and
the rest of the `POSTGRES_` variables as shown in the `backend.env` file in the top level directory).

**Load raster data**

Any province wide raster data can be copied over the fixture raster data in `backend/fixtures/raster`.  The next time you use `docker-compose up`,
these files will be copied to the Minio docker instance automatically.  Try not to accidently commit large files.

Get the existing province wide raster data from WALLY's Staging Minio instances (if you have access),
or regenerate them using the instructions in [the Watersheds README](backend/api/v1/watersheds/README.md).  If you regenerate stream-burned DEMs, make sure you
update the DEM tile extents in the `dem.stream_burned_cdem_tile` database table.

**Load FWA data**

To load FWA data province-wide, follow the instructions in [the Layers API README](backend/api/layers/README.md).  Only the streams and fundamental watersheds
layers need to be loaded into the database.  Other data is pulled from DataBC.

**Load Hydrosheds data**

Inspect the script in `imports/hydrosheds` and copy the commands for your environment.  This is only used for cross border watersheds, in which case you will also
need SRTM data along the 49th parallel (check the load raster data instructions above).

**Streamflow modeling data**

Ask the team for assistance with streamflow model data.

## Contributing

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).
