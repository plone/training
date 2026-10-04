---
myst:
  html_meta:
    "description": "Building images with buildx and publishing them to the zot registry on play4."
    "property=og:title": "4. Images and the registry"
    "keywords": "buildx, BuildKit, zot, container registry, deploy token"
---

(deploy-ref-registry)=

# 4. Images and the registry

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

## The registry

`play4` runs **zot**, an OCI-native registry, behind its own Traefik, at
`registry.playcluster.plone.org`. Images live under the GitLab project's own
path:

```
registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy/backend
registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy/frontend
```

zot was chosen over Harbor, which needs nine services and 8 GB of RAM, and over
the reference `registry:3`, which has no per-repository access control. zot is
one container and does have it — which matters for the next section.

## Two accounts, not one

zot has two robot accounts with different rights:

| Account | Rights | Used by |
| --- | --- | --- |
| push | read and write | the `build:*` jobs |
| pull | read only | the swarm |

That split exists for a specific reason. The deploy runs:

```
docker stack deploy --with-registry-auth
```

`--with-registry-auth` copies the credentials the deploying client used **onto
every swarm node**, where they persist so nodes can re-pull after a reboot or a
rescheduled task. So whatever the deploy authenticates with ends up sitting on
the cluster indefinitely.

```{important}
Two consequences. The credential handed to the deploy must be **read-only** —
otherwise every swarm node holds a push credential. And it must **not expire**,
or a node reboot months from now fails to pull and the service will not start.
```

This is also why the deploy never uses `$CI_JOB_TOKEN`: it dies with the
pipeline.

## Two registry modes

The pipeline supports GitLab's own registry as well, switched by a single
variable:

| `REGISTRY_IMAGE_PREFIX` | Result |
| --- | --- |
| unset | GitLab's registry via `$CI_REGISTRY_IMAGE`, built-in credentials |
| set | that prefix, with `REGISTRY_USER` / `REGISTRY_PASSWORD` |

The `config` job resolves it. It first expands any variable references in the
value itself — a group-level `registry.example.org/$CI_PROJECT_PATH` reaches
the job unexpanded — and stops if anything is left unresolved. It publishes the
result as `IMAGE_PREFIX`, not under the original name: a CI/CD variable outranks
a dotenv variable of the same name, so later jobs would get the raw value back.
It derives the host by taking everything before the first slash — which keeps
any `:port`:

```sh
echo "REGISTRY_HOST=${PREFIX%%/*}" >> build.env
```

Credentials are chosen by shell fallback at the point of use, never through the
dotenv report:

```yaml
- docker login
  -u "${REGISTRY_USER:-$CI_REGISTRY_USER}"
  -p "${REGISTRY_PASSWORD:-$CI_REGISTRY_PASSWORD}"
  "${REGISTRY_HOST}"
```

```{warning}
Dotenv artifacts are **not masked** in job logs. Secrets must never pass
through one. That is why credential selection happens in the shell.
```

Here, `REGISTRY_IMAGE_PREFIX` is set, to use the cluster's own registry. On
`gitlab.com` the built-in registry is always enabled, and that makes one mistake
quiet: if `REGISTRY_IMAGE_PREFIX` is missing from a pipeline — typically because
it was marked *Protected* and the pipeline runs on an unprotected branch — the
`config` job does not fail. It falls back to GitLab's registry, the build pushes
there, and the deploy looks for the images in zot. So `REGISTRY_IMAGE_PREFIX` is
the one variable that must **not** be protected.

## Building

`docker:29-cli` plus buildx, with the registry itself as the layer cache:

```yaml
docker buildx build ${TAGS} \
  --build-arg "${BUILD_ARG_NAME}=${BUILD_ARG_VALUE}" \
  --build-arg "MAINTAINER=${MAINTAINER}" \
  --cache-from "type=registry,ref=${IMAGE}/cache" \
  --cache-to   "type=registry,ref=${IMAGE}/cache,mode=max" \
  --push "${IMAGE_ROLE}"
```

`mode=max` exports every intermediate layer, not just the final ones, so a
later build can resume from any step. The cache lives in the registry alongside
the images, at `…/backend/cache`.

### One shared, persistent builder

```yaml
- export BUILDER="buildx-${CI_PROJECT_PATH_SLUG}"
- docker buildx create --use --driver docker-container --name "${BUILDER}"
  || docker buildx use "${BUILDER}"
```

Note what is missing: nothing ever removes it. That is deliberate, and it was
learned the hard way.

BuildKit handles concurrent builds perfectly well. What it does not survive is
being **torn down** while a build is running. With both build jobs sharing the
host's Docker daemon, an `after_script` doing `buildx rm` on a fixed name kills
whichever build is still going:

```
ERROR: failed to build: ... received prior goaway ... "graceful_stop"
```

A builder per job avoids that but throws away the content store every time,
which costs about 47 seconds re-pulling the 565 MB frontend base image on every
build. A shared, never-removed builder keeps the store warm. BuildKit's own
garbage collection bounds the disk use.

The effect is worth stating: a no-op backend build went from **2 m 40 s to
19 s**, and the cache export from 25.8 s to 3.2 s.

## Tagging, and why it matters

```sh
TAGS="--tag ${IMAGE}:${IMAGE_TAG}"
if [ "${CI_COMMIT_BRANCH}" = "${CI_DEFAULT_BRANCH}" ]; then
  TAGS="${TAGS} --tag ${IMAGE}:latest"
fi
```

| Pipeline | Tags |
| --- | --- |
| push to `main` | `sha-<short-sha>` **and** `latest` |
| git tag `1.0.0a1` | `1.0.0a1` |

Every build gets an **immutable** tag. `latest` moves; `sha-…` never does. That
is what makes rollback possible — chapter 6 uses it.

## Watching a build

The log tells you which parts of this worked:

```
#7 importing cache manifest from .../backend/cache
#7 inferred cache manifest type: application/vnd.oci.image.manifest.v1+json
```

The cache was found and reused. On a first build it reports `not found`
instead, which is expected and harmless.

```
#20 pushing manifest for .../backend:sha-52d3e62e
#21 exporting cache to registry
```

Image pushed, then the cache exported for the next run.
