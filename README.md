# Water Allocation Data Library



## Local development

### Prerequisites

Environment variables. Create a .env for docker to read your environment variables from
`MAPBOX_ACCESS_TOKEN` (required): a token from mapbox.com for making Mapbox API requests (e.g. requesting tiles and map images).
`MINIO_HOST_URL`: Set the default to minio:9000


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

Wally is deployed to OpenShift as a group of services. Except for the PostgreSQL database, each service is represented by a folder in this repo:

* `gatekeeper/` (Keycloak Gatekeeper) - gatekeeper is the OIDC proxy that directs users to the SSO service to login, and verifies that users have
the right permission to view resources. Gatekeeper is the only Wally service exposed to the internet, and proxies requests to the `frontend` service if authorized.

* `frontend/` (Vue app served by nginx) - The frontend folder contains Wally's web app and a Dockerfile for an nginx service that serves the built assets in the `dist` folder.
nginx also proxies requests to other services based on the `nginx.conf.templ` file in this folder.

* `backend/` (FastAPI Python backend) - the backend folder contains the REST API backend that serves data at the `/api/v1/` path.

* PostGIS - Data used by Wally is stored in a PostGIS-enabled PostgreSQL database, which uses Patroni for managing multiple replicas.  The Dockerfile and other build resources are in `openshift/patroni-postgis`.

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
