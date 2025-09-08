---
myst:
  html_meta:
    "description": "Plone Docker images for deployment"
    "property=og:description": "Plone Docker images for deployment"
    "property=og:title": "Plone Docker images for deployment"
    "keywords": "Plone, deployment, Docker, images"
---

# Plone Docker Images

Since the release of Plone 6, the community has a new set of Docker images offering more base options.

## `plone/plone-frontend`

Repository available at https://github.com/plone/plone-frontend/.

Installs the Plone 6 user-experience using the React-powered frontend, Volto.

Should be used to showcase the Plone 6 experience, as new projects will probably implement their own Docker images (with a similar Dockerfile), like the one below:

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

Installs the Plone 6 backend using a pip-based installation.
This approach makes it easier and faster to extend this image in your own project.

One example of such extension would be:

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
      org.label-schema.name="ploneconf2024-training-backend" \
      org.label-schema.description="Plone Conference Training Backend." \
      org.label-schema.vendor="Plone Community"

# Copy /app from builder
COPY --from=builder /app /app

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT
```

## `plone/plone-zeo`

Repository available at https://github.com/plone/plone-zeo/.

Installs a ZEO database server.
