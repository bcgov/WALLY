# Water Allocation Data Library

## Contributing

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

PGAdmin, PostgreSQL web administration: http://localhost:5050

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

## Backend local development, additional details

### General workflow

Open your editor at `./backend/app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc.

Modify or add SQLAlchemy models in `./backend/app/app/db_models/`, Pydantic models in `./backend/app/app/models/`, API endpoints in `./backend/app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./backend/app/app/crud/`. The easiest might be to copy the ones for Items (models, endpoints, and CRUD utils) and update them to your needs.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`. 

If you need to install any additional package to the worker, add it to the file `./backend/app/celeryworker.dockerfile`.

There is an `.env` file that has some Docker Compose default values that allow you to just run `docker-compose up -d` and start working, while still being able to use and share the same Docker Compose files for deployment, avoiding repetition of code and configuration as much as possible.

### Use a terminal inside a container

To get inside the container with a `bash` session you can start the stack with:

```bash
docker-compose up -d
```

and then `exec` inside the running container:

```bash
docker-compose exec backend bash
```

### Backend tests

To test the backend run:

```bash
DOMAIN=backend sh ./scripts/test.sh
```

The file `./scripts/test.sh` has the commands to generate a testing `docker-stack.yml` file from the needed Docker Compose files, start the stack and test it.

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

If you need to install any additional package for the tests, add it to the file `./backend/app/tests.dockerfile`.

#### Test running stack

If your stack is already up and you just want to run the tests, you can use:

```bash
docker-compose exec backend-tests /tests-start.sh
```

That `/tests-start.sh` script inside the `backend-tests` container calls `pytest`. If you need to pass extra arguments to `pytest`, you can pass them to that command and they will be forwarded.

For example, to stop on first error:

```bash
docker-compose exec backend-tests /tests-start.sh -x
```

### Migrations

As during local development your app directory is mounted as a volume inside the container (set in the file `docker-compose.dev.volumes.yml`), you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```bash
docker-compose exec backend bash
```

* If you created a new model in `./backend/app/app/db_models/`, make sure to import it in `./backend/app/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```bash
alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```bash
alembic upgrade head
```

## Frontend development

* Enter the `frontend` directory, install the NPM packages and start the live server using the `npm` scripts:

```bash
cd frontend
npm install
npm run serve
```

Then open your browser at http://localhost:8080

Notice that this live server is not running inside Docker, it is for local development, and that is the recommended workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a production-like environment. But compiling the image at every change will not be as productive as running the local development server.

Check the file `package.json` to see other available options.

If you have Vue CLI installed, you can also run `vue ui` to control, configure, serve and analyse your application using a nice local web user interface.


## Docker Compose files

There are several Docker Compose files, each with a specific purpose.

They are designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why several of the files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

Because of that, for each "stage" (development, building, testing, deployment) you would use a different set of Docker Compose files.

But you probably don't have to worry about the different files, for building, testing and deployment, you would probably use a CI system (like GitLab CI) and the different configured files would be already set there.

And for development, there's a `.env` file that will be automatically used by `docker-compose` locally, with the default configurations already set for local development. Including environment variables. So, for local development you can just run:

```bash
docker-compose up -d
```

and it will do the right thing.

They are also separated by the common tasks and functionalities they solve, and they are named accordinly. So, although there are many Docker Compose files, each one has a name that shows what should be in there, and the contents tend to be small and specific. That makes it easier to modify, or add configurations, as you can go directly to the relevant file.

The `docker-compose.deploy.*.yml` files are only used at deployment, being it to production or any other environment. They build the images in production mode (not installing debugging packages), set configurations for Docker Swarm mode, etc.

The `docker-compose.dev.*.yml` files are only used during development. They have overrides and tools for development, as mounting app volumes directly inside the container to iterate fast, map ports directly to your machine, install debugging packages, etc.

The `docker-compose.test.yml` file is used for testing, during development and in a CI environment running tests, but not used in deployment to production (or staging or any other deployment environment of the final code).

The `docker-compose.shared.*.yml` files are used at several stages and contain stuff shared by several stages: development, testing, deployment. They have things like the databases or the environment variables, that are used by all the main services / containers, during development, testing and deployment. The file for `admin`, that has utils needed for development and production, like the Swagger UI interactive API documentation system. But this file is not used during testing (in CI environments) as this is not needed or used in that stage.

The purpose of each Docker Compose file is:

* `docker-compose.deploy.build.yml`: build directories and `Dockerfile`s, for deployment (the building process for development has a little difference).
* `docker-compose.deploy.command.yml`: command overrides for images only during deployment. Initially only for the main Traefik proxy, making it run in a Docker Swarm mode cluster.
* `docker-compose.deploy.images.yml`: image names to be created, with environment variables for the specific tag.
* `docker-compose.deploy.labels.yml`: labels for deployment, the configurations to make the internal Traefik proxy serve some services on specific URLs, some with basic HTTP auth, etc. Also labels used in the internal Traefik proxy container to make it talk to the public Traefik proxy (outside of this stack) and make it send requests for this domain, generate HTTPS certificates, etc.
* `docker-compose.deploy.networks.yml`: networks that have to be used and shared by containers that need to be able to talk to the public Traefik proxy (when a service requires a domain for itself).
* `docker-compose.deploy.volumes-placement.yml`: volume declarations, volumes used by stateful services (as databases) and volume placement constraints, to make those services always run on the node that has their volumes, even after stack updates.
* `docker-compose.dev.build.yml`: build directories and `Dockerfile`s, for local development, sets a built-time argument that then is used in the `Dockerfile`s to install and configure helper tools exclusively for development.
* `docker-compose.dev.command.yml`: command overrides for local development. To tell the internal Traefik proxy to work with a local Docker in the host instead of a Docker Swarm mode cluster. And (commented out but ready to be used) overrides to make the containers run an infinite loop while keeping alive to be able to run the development server manually or do any other interactive work.
* `docker-compose.dev.env.yml`: development environment variable overrides.
* `docker-compose.dev.labels.yml`: local development labels, to be used by the local development Traefik proxy. They have to be declared in a different place than for deployment.
* `docker-compose.dev.networks.yml`: local development networks, to enable interactively talking to the backend.
* `docker-compose.dev.ports.yml`: local development port mappings.
* `docker-compose.dev.volumes.yml`: local development mounted volumes, mainly to map the development code directory inside the container, for fast development without needing to re-build the images.
* `docker-compose.shared.admin.yml`: additional services for administration or utilities with their configurations, like PGAdmin and Swagger, that are not needed during testing and use external images (don't need to be built or create images).
* `docker-compose.shared.base-images.yml`: base Docker images used without modification for shared services, as databases. Used in deployment, development, testing, etc.
* `docker-compose.shared.depends.yml`: dependencies between main services with `depends_on`, used in deployment, development, testing, etc.
* `docker-compose.shared.env.yml`: environment variables used by services, as database passwords, secret keys, etc.
* `docker-compose.test.yml`: specific additional container to be used only during testing, mainly the container that tests the backend and the APIs.

## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

You can check the variables used during generation in the file `cookiecutter-config-file.yml`.

You can generate the project again with the same configurations used the first time.

That would be useful if, for example, the project generator (`tiangolo/full-stack-fastapi-postgresql`) was updated and you want to integrate or review the changes.

You could generate a new project with the same configurations as this one in a parallel directory. And compare the differences between the two, without having to overwrite your current code but being able to use the same variables used for your current project.

To achieve that, the generated project includes the file `cookiecutter-config-file.yml` with the current variables used.

You can use that file while generating a new project to reuse all those variables.

For example, run:

```bash
cookiecutter --config-file ./cookiecutter-config-file.yml --output-dir ../project-copy https://github.com/tiangolo/full-stack-fastapi-postgresql
```

That will use the file `cookiecutter-config-file.yml` in the current directory (in this project) to generate a new project inside a sibling directory `project-copy`.
