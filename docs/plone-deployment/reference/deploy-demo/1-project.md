---
myst:
  html_meta:
    "description": "The backend and frontend of a cookieplone project, and the two Dockerfiles that turn them into images."
    "property=og:title": "1. The project and its images"
    "keywords": "cookieplone, Plone, Volto, Dockerfile, uv, pnpm"
---

(deploy-ref-project)=

# 1. The project and its images

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

A cookieplone project is a monorepo: one repository holding a Plone backend, a
Volto frontend, and the deployment description for both. They are versioned and
released together, which is what makes a single pipeline sensible.

```
backend/     Plone, installed with uv. Python package: playclusterdemo
frontend/    Volto, installed with pnpm. Add-on: volto-playclusterdemo
devops/      The Docker Swarm stack file
.gitlab/     The pipeline
repository.toml   Project and deployment settings
```

## repoplone, the thing that knows the answers

Almost nothing in this repository hardcodes a version. `repository.toml`
declares them, and `repoplone` reads it:

```shell
uvx repoplone settings dump
```

```json
{
  "name": "playcluster-demo",
  "container_images_prefix": "registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy",
  "backend":  { "python_version": "3.13", "base_package_version": "6.2.1" },
  "frontend": { "volto_version": "19.3.0" }
}
```

Both Makefiles call this while *parsing*, not while running:

```makefile
REPOSITORY_SETTINGS := $(shell uvx repoplone settings dump)
PLONE_VERSION := $(shell echo '$(REPOSITORY_SETTINGS)' | jq -r '.backend.base_package_version')
```

```{important}
That has a consequence for CI: **every job that runs `make` needs `uv` and
`jq`**, even frontend jobs that never touch Python. Miss it and the Makefile
fails before the first target runs.
```

## The backend

Plone installed with `uv`, not buildout, and not pip. `backend/Makefile`'s
`install` target does three things:

```makefile
update-constraints:  uvx repoplone deps constraints
sync:                uv sync
config:              uvx cookiecutter ... gh:plone/cookiecutter-zope-instance
```

`uv.lock` pins the entire dependency tree, and `uv sync --locked` in the image
build refuses to proceed if the lockfile and `pyproject.toml` disagree. That is
the property we want in CI: builds fail loudly rather than resolving something
new.

The `[tool.uv] constraint-dependencies` block in `backend/pyproject.toml` holds
the Plone version pins that `repoplone deps constraints` generates. It is
several hundred lines and it is generated — do not hand-edit it.

## The backend image

`backend/Dockerfile`, two stages:

```dockerfile
ARG PYTHON_VERSION=3.13
FROM plone/server-builder:uv-${PYTHON_VERSION} AS builder

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-group test --group container --no-install-project

COPY . /src
RUN uv sync --locked --no-dev --no-group test --group container --no-editable

FROM plone/server-prod-config:uv-${PYTHON_VERSION}
COPY --from=builder --chown=500:500 /app /app
```

Two details worth pausing on.

**Dependencies are installed before the source is copied.** Only `uv.lock` and
`pyproject.toml` are bind-mounted for that first `uv sync`. So editing Python
code does not invalidate the dependency layer, and rebuilds after a code change
are fast.

**The runtime stage carries no build tooling.** It starts from
`plone/server-prod-config` and copies the finished `/app` across.

## The frontend image

`frontend/Dockerfile` has a wrinkle that surprises people:

```dockerfile
FROM plone/frontend-builder:${VOLTO_VERSION} AS builder

COPY --chown=node packages/volto-playclusterdemo /app/packages/volto-playclusterdemo
COPY --chown=node package.json /app/package.json.temp
COPY --chown=node mrs.developer.json /app/
COPY --chown=node pnpm-lock.yaml /app/pnpm-lock.yaml

RUN <<EOT
    python3 -c "...merge package.json.temp dependencies into package.json..."
    pnpm dlx mrs-developer missdev --no-config --fetch-https
    pnpm install && pnpm build:deps
    pnpm build
EOT
```

Volto core is **not** in this repository. `mrs.developer.json` pins a version:

```json
{ "core": { "package": "@plone/volto", "tag": "19.3.0", "filterBlobs": true } }
```

and `mrs-developer` clones it into `frontend/core` during the build. So the
image build needs network access to GitHub, and `frontend/core` is deliberately
gitignored.

The base image already carries a `package.json`; the project's own dependencies
are merged into it rather than replacing it. That is what the `package.json.temp`
dance is doing.

## Both Dockerfiles take a MAINTAINER build argument

```dockerfile
ARG MAINTAINER="Fred van Dijk <fred@plone.org>"
LABEL maintainer="${MAINTAINER}" \
      org.label-schema.name="playcluster-demo-backend"
```

The default keeps a bare `docker build` sensible. CI passes the real value,
read from `backend/pyproject.toml`'s `[project].authors` — the single place it
is declared.

## Building them by hand

```shell
make build-images
```

which is just the two Makefile targets:

```makefile
build-image:
	docker build . -t $(IMAGE_NAME) --build-arg PYTHON_VERSION=$(PYTHON_VERSION) -f Dockerfile
```

`IMAGE_NAME` comes from `container_images_prefix` in `repository.toml`, so a
local build produces exactly the names CI produces. That is deliberate: the
pipeline is not doing anything you cannot reproduce on your laptop.

## Try it

Nothing to deploy, but worth running to see where the values come from:

```shell
make debug-settings
```

```
PROJECT_NAME: playcluster-demo
VOLTO_VERSION: 19.3.0
PLONE_VERSION: 6.2.1
PUBLIC_HOSTNAME: playcluster.plone.org
STACK_NAME: playcluster-plone-org
STACK_FILE: devops/stacks/stack.yml
```

Every one of those comes out of `repository.toml`. Chapter 5 shows where they
end up.
