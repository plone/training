---
myst:
  html_meta:
    "description": "Plone Docker images for deployment"
    "property=og:description": "Plone Docker images for deployment"
    "property=og:title": "Plone Docker images for deployment"
    "keywords": "Plone, deployment, Docker, images"
---

# Plone Docker images

Since the release of Plone 6, the community has a new set of public Docker images offering most base options, and documenting the configuration. They are meant as a way to quickly start a project, and provide inspiration for your own projects advanced requirements.

## `plone/plone-frontend`

Repository is available at https://github.com/plone/plone-frontend/.

Installs the Plone 6 user experience using the React-powered frontend, Volto.

Should be used to showcase the Plone 6 experience, and how to build images in multiple stages to reduce image size. New projects will probably implement their own Docker images with a similar Dockerfile, like the one below:

```Dockerfile
# syntax=docker/dockerfile:1
ARG VOLTO_VERSION
FROM plone/frontend-builder:${VOLTO_VERSION} AS builder

COPY --chown=node packages/volto-project-title /app/packages/volto-project-title
COPY --chown=node volto.config.js /app/
COPY --chown=node package.json /app/package.json.temp

RUN --mount=type=cache,id=pnpm,target=/app/.pnpm-store,uid=1000 <<EOT
    set -e
    python3 -c "import json; orig_data = json.load(open('package.json.temp')); orig_deps = orig_data['dependencies']; data = json.load(open('package.json')); data['dependencies'].update(orig_deps); json.dump(data, open('package.json', 'w'), indent=2)"
    rm package.json.temp
    pnpm install && pnpm build:deps
    pnpm build
    pnpm install --prod
EOT

FROM plone/frontend-prod-config:${VOLTO_VERSION}

LABEL maintainer="Plone Community <dev@plone.org>" \
      org.label-schema.name="project-title-frontend" \
      org.label-schema.description="Project Title frontend image." \
      org.label-schema.vendor="Plone Community"

COPY --from=builder /app/ /app/

RUN <<EOT
    set -e
    corepack enable pnpm
    corepack use pnpm@9.1.1
    corepack prepare pnpm@9.1.1 --activate
EOT
```

## `plone/plone-backend`

Repository available at https://github.com/plone/plone-backend/.

Installs the Plone 6 backend using a package-based installation.

There are currently two distinct approaches to use the backend base images in your project, as described in the following sections.

### Usage with pip and mxdev

```Dockerfile
# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.13
FROM plone/server-builder:${PLONE_VERSION} AS builder

WORKDIR /app


# Add local code
COPY scripts/ scripts/
COPY . src

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    bin/pip install mxdev uv
    sed -i 's/-e .\[test\]/./g' src/mx.ini
    cd /app/src
    # remove potentially existing virtualenv from local build
    rm -rf .venv
    ../bin/mxdev -c mx.ini
    ../bin/uv pip install -r requirements-mxdev.txt
    ../bin/python /compile_mo.py
    cd /app
    rm -Rf src/
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="ploneconf2025-training-backend" \
      org.label-schema.description="Plone Conference Training Backend." \
      org.label-schema.vendor="Plone Community"

# Copy /app from builder
COPY --from=builder /app /app

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT
```

### Usage with uv (experimental)

To use these images, your project should already use uv and have a {file}`pyproject.toml` section with additional dependencies to be installed inside a container:

```toml
[dependency-groups]
...
container = [
    "plone.app.upgrade",
    "psycopg2==2.9.10",
    "relstorage==4.1.1",
    "zeo==6.0.0",
]
```

The `Dockerfile` will look like:

```Dockerfile
# syntax=docker/dockerfile:1.9
ARG PYTHON_VERSION=3.12
FROM plone/server-builder:uv-${PYTHON_VERSION} AS builder

# Install dependencies
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
        --locked \
        --no-dev \
        --no-group test \
        --group container \
        --no-install-project

COPY . /src
WORKDIR /src

# Install package
RUN --mount=type=cache,target=/root/.cache \
    uv sync \
        --locked \
        --no-dev \
        --no-group test \
        --group container \
        --no-editable

# Move skeleton files to /app
RUN <<EOT
    mv /app_skeleton/* /app
    rm -Rf /app_skeleton
    mv container/docker-entrypoint.sh /app/docker-entrypoint.sh
    chmod +x /app/docker-entrypoint.sh
    mv scripts/create_site.py /app/scripts/create_site.py
EOT

# Compile translation files
RUN <<EOT
    /app/bin/python /compile_mo.py
EOT

FROM plone/server-prod-config:uv-${PYTHON_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="ploneconf2025-training-backend" \
      org.label-schema.description="Plone Conference Training Backend." \
      org.label-schema.vendor="Plone Community"

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=builder --chown=500:500 /app /app

RUN <<EOT
    ln -s /data /app/var
    chown -R 500:500 /data
EOT
```


## `plone/plone-zeo`

Repository available at https://github.com/plone/plone-zeo/.

Provides a ZEO database server for your container based Plone CMS stack. This allows you to scale to multiple backends without a relational database, such as PostgreSQL or MySQL, to store the content data.
