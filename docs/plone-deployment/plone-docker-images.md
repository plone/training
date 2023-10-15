---
myst:
  html_meta:
    "description": "Plone Docker images for deployment"
    "property=og:description": "Plone Docker images for deployment"
    "property=og:title": "Plone Docker images for deployment"
    "keywords": "Plone, deployment, Docker, images"
---

# Plone Docker Images

Since the release of Plone 6, the community has a new set of Docker images -- and offering more base options.

## plone/plone-frontend

Repository available at [https://github.com/plone/plone-frontend/](https://github.com/plone/plone-frontend/)

Installs the Plone 6 default user-experience (Using the React-powered frontend: Volto).

Should be used to showcase the default Plone 6 experience, as new projects will probably implement their own Docker images (with a similar Dockerfile),
like the one below:

```Dockerfile
# syntax=docker/dockerfile:1
FROM node:18-slim as base
FROM base as builder

RUN <<EOT
    set -e
    apt update
    apt install -y --no-install-recommends python3 build-essential
    mkdir /app
    chown -R node:node /app
    rm -rf /var/lib/apt/lists/*
EOT

COPY --chown=node . /build/
RUN corepack enable

USER node
WORKDIR /build
RUN <<EOT
    set -e
    make install
    yarn build
EOT

FROM base

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="ploneconf2023-training-frontend" \
      org.label-schema.description="Plone Conference Training Frontend." \
      org.label-schema.vendor="Plone Community"

# Install busybox and wget
RUN <<EOT
    set -e
    apt update
    apt install -y --no-install-recommends busybox wget
    busybox --install -s
    rm -rf /var/lib/apt/lists/*
    mkdir /app
    chown -R node:node /app
EOT

# Run the image with user node
USER node

# Copy -
COPY --from=builder /build/ /app/

# Set working directory to /app
WORKDIR /app

# Expose default Express port
EXPOSE 3000

# Set healthcheck to port 3000
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s CMD [ -n "$LISTEN_PORT" ] || LISTEN_PORT=3000 ; wget -q http://127.0.0.1:"$LISTEN_PORT" -O - || exit 1

# Entrypoint would be yarn
ENTRYPOINT [ "yarn" ]

# And the image will run in production mode
CMD ["start:prod"]

```

## plone/plone-backend

Repository available at [https://github.com/plone/plone-backend/](https://github.com/plone/plone-backend/)

Installs the Plone 6 backend using a pip-based installation.
This approach makes it easier and faster to extend this image in your own project.

One example of such extension would be:

```Dockerfile
# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6.0.7
FROM plone/server-builder:${PLONE_VERSION} as builder

WORKDIR /app

# Add local code
COPY . .

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    bin/pip install mxdev
    mv requirements-docker.txt requirements.txt
    sed -i 's/-e src\/ploneconf2023_training\[test\]/src\/ploneconf2023_training/g' mx.ini
    bin/mxdev -c mx.ini
    bin/pip install -r requirements-mxdev.txt
    bin/python /compile_mo.py
    rm -Rf src/
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="ploneconf2023-training-backend" \
      org.label-schema.description="Plone Conference Training Backend." \
      org.label-schema.vendor="Plone Community"

# Copy /app from builder -
COPY --from=builder /app /app

RUN <<EOT
    set -e
    ln -s /data /app/var
EOT
```

## plone/plone-zeo

Repository available at [https://github.com/plone/plone-zeo/](https://github.com/plone/plone-zeo/)

Installs a ZEO database server.
