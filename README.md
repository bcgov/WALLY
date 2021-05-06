# Water Allocation Data Library


## Local development

### Prerequisites

Environment variables. Create a `.env` for docker to read your environment variables from
`MAPBOX_ACCESS_TOKEN` (required): a token from mapbox.com for making Mapbox API requests (e.g. requesting tiles and map images).
`MINIO_HOST_URL`: Set the default to minio:9000

The backend also uses [Pydantic's settings management](https://github.com/bcgov-c/wally/blob/0dc732c241bff5e8d8ce72d40ab88b9286e4566c/backend/api/config.py#L61-L82)
Create a file called `dev.env` under `backend/.config/` to test your feature flags and other settings.

Start the backend API and database stack with Docker Compose:

```bash
docker-compose up -d
```

Start the frontend development server:
```bash
cd frontend
npm install
npm run serve
```

Migrate database:
```bash
make migrate
```

Load fixture data:
```bash
make loaddata
```

## Application

Wally is deployed as a group of services:

* `frontend/` (Vue app served by nginx) - The frontend folder contains Wally's web app and a Dockerfile for an nginx service that serves the built assets in the `dist` folder.
nginx also proxies requests to other services based on the `nginx.conf.templ` file in this folder.

* `backend/` (FastAPI Python backend) - the backend folder contains the REST API backend that serves data at the `/api/v1/` path.

* PostGIS - Data used by Wally is stored in a PostGIS-enabled PostgreSQL database, which uses Patroni for managing multiple replicas.  The Dockerfile and other build resources are in `openshift/patroni-postgis`.

* Minio - WALLY uses Minio to host spatial data raster files, store Freshwater Atlas data, and store uploaded user files. See the configuration in `openshift/ocp4/minio`.


### WALLY and OpenShift

WALLY runs on BCGov's OpenShift 4 platform.

For day to day feature work, WALLY's CI/CD will take care of deploying PR environments and automatically deploying merged PR's to staging.  See `Jenkinsfile.ocp4` and
the templates in the `openshift` folder.

For configuration and data that WALLY needs to get up and running the first time, see [Migrating to OpenShift 4](openshift/ocp4/README.md).

## Working on spatial raster files

If you need to edit or update spatial raster files, you'll need to create two files: the BC-wide file that staging and production will use,
and a Whistler area cropped version for local dev fixtures.

See [the Watersheds README](backend/api/v1/watersheds/README.md) for instructions on how to create Cloud Optimized GeoTIFF rasters for use with WALLY,
and the [fixture extents README](backend/fixtures/extents/README.md) for instructions on how to create a corresponding fixture file in the `raster` dir.


### Use a terminal inside a container

To get inside the container with a `bash` session you can start the stack with:

```bash
docker-compose up -d
```

and then `exec` inside the running container:

```bash
docker-compose exec backend bash
```

## Contributing

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).
