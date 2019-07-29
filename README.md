# Water Allocation Data Library



## Local development

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
