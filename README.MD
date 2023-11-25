# jetfork hack-ai

## Features

- FastAPI
- ElasticSearch
- Pre-commit hooks (black, autoflake, isort, flake8, prettier)
- Github Action
- Dependabot config
- Docker images


## Step 1: Getting started

Start a local development instance with docker-compose

```bash

# for medium files
git lfs insatll
git lfs pull

# for large files. Download Resource folder!
# scp -r -C -B ./resources/* hackai:/root/hack/resources/
chmod u+x ./resources.sh && . ./resources.sh

docker-compose up -d
```

Now you can navigate to the following URLs:

- Backend OpenAPI docs: http://localhost:8000/docs/
- Frontend: http://localhost:3000

### Step 2: Setup pre-commit hooks and database

Keep your code clean by using the configured pre-commit hooks. Follow the [instructions here to install pre-commit](https://pre-commit.com/). Once pre-commit is installed, run this command to install the hooks into your git repository:

```bash
pre-commit install
```

### Local development

The backend setup of docker-compose is set to automatically reload the app whenever code is updated. However, for frontend it's easier to develop locally.

```bash
docker-compose stop frontend
cd frontend
yarn
yarn start
```

If you want to develop against something other than the default host, localhost:8000, you can set the `REACT_APP_API_BASE` environment variable:

```bash
export REACT_APP_API_BASE=http://mydomain.name:8000
yarn start
```

Don't forget to edit the `.env` file and update the `BACKEND_CORS_ORIGINS` value (add `http://mydomain:3000` to the allowed origins).

### Rebuilding containers

If you add a dependency, you'll need to rebuild your containers like this:

```bash
docker-compose up -d --build
```

### Regenerate front-end API package

Instead of writing frontend API client manually, OpenAPI Generator is used. Typescript bindings for the backend API can be recreated with this command:

```bash
yarn genapi
```
