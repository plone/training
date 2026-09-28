---
myst:
  html_meta:
    "description": "How the deploy job reaches the swarm, and how repository.toml settings become running services."
    "property=og:title": "5. The deploy"
    "keywords": "docker stack deploy, Docker Swarm, Traefik labels, placement constraints"
---

(deploy-ref-deploy)=

# 5. The deploy

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

## The job

```yaml
"deploy:production":
  image:
    name: ghcr.io/kitconcept/docker-stack-deploy:1.4.0
    entrypoint: [""]
  tags: [${RUNNER_TAG_DEPLOY}]
  resource_group: production
  environment:
    name: production
    url: ${DEPLOY_URL}
  script:
    - set -a && . ./deploy.env && set +a
    - export STACK_PARAM="${IMAGE_TAG}"
    - /docker-entrypoint.sh
```

`docker-stack-deploy` is a small image built on `docker:cli`. Its entrypoint
configures SSH from the variables it is given, sets
`DOCKER_HOST=ssh://user@host`, and runs `docker stack deploy` against the remote
daemon.

```{note}
Because it works over SSH, this job needs **neither Docker-in-Docker nor a
mounted Docker socket**. GitLab overrides a job image's entrypoint with its own
shell, so `entrypoint: [""]` clears it and the script calls the entrypoint
itself.
```

`resource_group: production` serialises deploys — two pipelines can never touch
the stack at once.

The log is a line per phase, so the last successful line tells you where it
stopped:

```
Container Registry: Logged in registry.playcluster.plone.org as deploy
SSH client: Configured
SSH remote: Keys added to /root/.ssh/known_hosts
SSH connect: Success
Deploy: Updated services
Deploy: Checking status
Deploy: Completed
```

No `SSH_KNOWN_HOSTS` variable is needed — the entrypoint runs `ssh-keyscan`
itself.

## From repository.toml to running services

This is the chain worth understanding, because everything else follows from it.

```
repository.toml [deployment]
        |  read by the config job with tomllib
        v
   deploy.env  (ordinary artifact)
        |  sourced by deploy:production
        v
  environment variables
        |  interpolated by docker stack deploy
        v
 devops/stacks/stack.yml
        |
        v
   running services
```

Four hops, one source. Change the hostname in `repository.toml` and it reaches
the router rule, the Volto API path and the VHM rewrites without touching the
stack file.

## The stack file

Three services. No Traefik, no published ports.

### frontend

```yaml
frontend:
  image: ${REGISTRY_IMAGE_PREFIX}/frontend:${STACK_PARAM:-latest}
  environment:
    RAZZLE_INTERNAL_API_PATH: http://backend:8080/Plone
    RAZZLE_API_PATH: https://${PUBLIC_HOSTNAME}
  networks: [nw-public, nw-internal]
  deploy:
    replicas: 2
    placement:
      constraints:
        - ${APP_PLACEMENT:-node.platform.os == linux}
```

Two API paths, and the difference matters. `RAZZLE_INTERNAL_API_PATH` is used by
Volto's server-side rendering and points at the backend service directly over
the internal network. `RAZZLE_API_PATH` is what the browser uses, so it must be
the public URL.

### backend

Same shape, plus the VirtualHostMonster rewrites. Plone needs to know the public
URL to generate correct links, and Traefik tells it by rewriting the path:

```yaml
- "traefik.http.middlewares.${STACK_PREFIX}-vhm.replacepathregex.replacement=/VirtualHostBase/https/${PUBLIC_HOSTNAME}/Plone/++api++/VirtualHostRoot$$1"
```

The `$$` is an escaped `$` — docker compose would otherwise try to interpolate
it.

### db

```yaml
db:
  image: postgres:18
  deploy:
    replicas: 1
    placement:
      constraints:
        - ${DB_PLACEMENT:?set DB_PLACEMENT to deployment.db_placement from repository.toml}
  volumes:
    - vol-site-data:/var/lib/postgresql
```

```yaml
volumes:
  vol-site-data:
    driver_opts:
      type: none
      device: "${DATA_PATH:?...}"
      o: bind
```

```{warning}
This is the most dangerous part of the file. The volume is a **bind mount to a
path on one specific node**. Without a placement constraint, Swarm may
reschedule the task elsewhere, where that path is a different — empty —
directory, and Plone comes up against a blank database. Nothing errors.
```

Hence `db_placement` uses `:?` — the deploy refuses to run without it — while
`app_placement` uses `:-` with an always-true default, because an unconstrained
frontend is merely suboptimal. The severity of the failure decides which form to
use.

`db_placement` resolves to `node.labels.storage == persistent`, which is
`play3`.

## Traefik labels

The stack ships no Traefik, so routing is a set of labels the cluster's
instance reads. Four things have to line up, all from `[deployment.traefik]`:

```yaml
- traefik.enable=true
- traefik.constraint-label=${TRAEFIK_CONSTRAINT_LABEL:-public}
- traefik.swarm.network=${TRAEFIK_NETWORK:-nw-public}
- traefik.http.routers.${STACK_PREFIX}-frontend.rule=Host(`${PUBLIC_HOSTNAME}`)
- traefik.http.routers.${STACK_PREFIX}-frontend.entrypoints=${TRAEFIK_ENTRYPOINT:-https}
- traefik.http.routers.${STACK_PREFIX}-frontend.tls.certresolver=${TRAEFIK_CERTRESOLVER:-le}
```

Each has to match the cluster's Traefik, set up in the `training-deployment-playcluster`
repository (its chapter 3): the constraint label it
filters on, the network it reaches services over, and the names of its
entrypoint and certificate resolver. Get one wrong and the service is simply not
routed — usually with no error anywhere.

```{warning}
Set `traefik.swarm.network`, never `traefik.docker.network` as well. Defining
both makes Traefik **skip the service entirely**:

    ERR Skip container error="both Docker and Swarm labels are defined"

No router appears at all, which looks like a discovery problem rather than a
label problem. This cost an evening.
```

Two more things learned by getting them wrong:

**Namespace what you define.** Router, service and middleware names are global
to the Traefik instance. `${STACK_PREFIX}` prefixes everything this stack owns.

**Do not redeclare what the cluster owns.** The routers reference `gzip`, which
the cluster's Traefik defines. Declaring a second `gzip` in the same provider
can conflict and affect other applications.

**There is no HTTP router.** The cluster Traefik redirects at the entrypoint:

```
--entrypoints.http.http.redirections.entrypoint.to=https
```

so no stack needs its own redirect.

## The tag being deployed

```sh
export STACK_PARAM="${IMAGE_TAG}"
```

`STACK_PARAM` is what the image lines interpolate:

```yaml
image: ${REGISTRY_IMAGE_PREFIX}/backend:${STACK_PARAM:-latest}
```

So a push to `main` deploys `sha-<short-sha>` — the immutable tag, not `latest`.
Which is what makes the rollback in chapter 6 work.

On a release tag, `IMAGE_TAG` is the tag itself, so the images are named after
the release rather than after a sha. Only version-shaped tags do that:

```yaml
.rules-release:
  rules:
    - if: $CI_COMMIT_TAG =~ /^v?\d+\.\d+/
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

Without that pattern, *any* tag deploys — and a tag put on an older commit for
some unrelated reason would quietly build that commit and ship it over what is
running. A training that tags every step of an exercise, or a `git bisect`
marker, is exactly such a case.
