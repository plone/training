---
myst:
  html_meta:
    "description": "Following a GitLab pipeline from git push through lint, test, image build and registry to a running Plone site on Docker Swarm."
    "property=og:description": "Following a GitLab pipeline from git push through lint, test, image build and registry to a running Plone site on Docker Swarm."
    "property=og:title": "Building and deploying with GitLab CI"
    "keywords": "Plone, GitLab CI, BuildKit, container registry, Docker Swarm, deploy, create-site"
---

(build-deploy-gitlab-label)=

# Building and deploying with GitLab CI

In {ref}`playcluster-label` we looked at what the project contains.
This chapter follows what happens when you push it.

## The pipeline at a glance

Five stages.
`.pre` is built into GitLab and always runs first.

```
.pre      config
check     backend:lint  frontend:lint  frontend:i18n  changelog (merge requests)
test      backend:test  frontend:test
build     build:backend  build:frontend
deploy    deploy:production
```

Every branch and merge request gets `config`, `check` and `test`.
Only the default branch and version-shaped tags such as `1.0.0` go on to `build` and `deploy`: nothing publishes an image or touches the cluster from a feature branch.

All jobs run on the GitLab Runner on `play4`, through its tags: `docker` for everything that builds, `deploy` for the deploy.
The runner takes four jobs at a time, one per CPU of `play4`, and the check and test jobs start as soon as `config` is done rather than waiting for their whole stage.

In the reference: {ref}`deploy-ref-pipeline`.

## config: one job that knows everything

The first job reads the project's settings once and hands them to every later job: the Python, Plone and Volto versions from `repoplone`, the `[deployment]` section of `repository.toml`, the image tag, and which registry to use.
Its log ends by printing everything it resolved, which makes it the first place to look when a deploy goes somewhere unexpected:

```console
IMAGE_PREFIX=registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy
REGISTRY_HOST=registry.playcluster.plone.org
IMAGE_TAG=sha-080716f7
DEPLOY_URL=https://playcluster.plone.org
PUBLIC_HOSTNAME=playcluster.plone.org
STACK_NAME=playcluster-plone-org
STACK_PREFIX=reference
DATA_PATH=/srv/playcluster-demo/data
DB_PLACEMENT='node.labels.storage == persistent'
```

That log earned its keep on the very first pipeline for this project.
It showed `registry.playcluster.plone.org/$CI_PROJECT_PATH`, with the variable name still in it: GitLab had passed the group variable's reference through unexpanded.
The build job then failed trying to tag an image with a `$` in its name.
The fix was to let `config` expand the reference itself, and to stop with a clear message if anything is ever left unresolved.

```{note}
GitLab rejects a dotenv report with more than 20 variables, with an unhelpful `400 Bad Request`.
So `config` writes the few values that must be real CI/CD variables to `build.env`, and everything the stack file needs to `deploy.env`, an ordinary file the deploy job reads.
```

## check and test

Lint and tests for backend and frontend, in parallel.
Two things are worth knowing:

- The backend lint job does **not** run `make lint`.
  That target fixes the code it lints and always exits 0, so in CI it would pass forever.
  The pipeline calls the same tools in read-only mode instead.
- Every job that runs `make` needs `uv` and `jq`, even the frontend ones, because the Makefiles ask `repoplone` for the versions while they are parsed.

## build: images and the registry

The build jobs log in to the registry with the `ci` account, build with BuildKit, and push.
Each image gets two tags on the default branch:

`sha-<short commit>`
: Immutable. This is the one the deploy uses, and what makes a rollback possible.

`latest`
: Moves with every build.

A release tag, such as `1.0.0` made with `make release-tag`, names the images after the release instead.

The registry doubles as the build cache.
The very first build of an image finds nothing:

```console
#11 importing cache manifest from …/backend/cache
#11 ERROR: failed to configure registry cache importer: …/backend/cache:latest: not found
```

That is expected, not a failure.
The job exports its cache at the end, and the next pipeline finds it: on the second run of the backend build today, nine steps came back `CACHED`.
The first backend build, with no cache at all, took under two minutes.

In the reference: {ref}`deploy-ref-registry`.

## deploy: over SSH to the swarm

The deploy job runs a small image, `docker-stack-deploy`, that logs in to the registry with the read-only `deploy` account, connects to the swarm manager over SSH as `plone`, and runs `docker stack deploy`.
It needs no Docker of its own.

Its log is one line per phase, so the last line tells you how far it got.
This is the first deploy of the reference site, which took just over a minute:

```console
Container Registry: Logged in registry.playcluster.plone.org as deploy
SSH connect: Success
Deploy: Updated services
Deploy: Checking status
Service playcluster-plone-org_backend state: replicating 0/2
Service playcluster-plone-org_db state: replicating 0/1
Service playcluster-plone-org_frontend state: replicating 0/2
Service playcluster-plone-org_db state: deployed
Service playcluster-plone-org_backend state: deployed
Service playcluster-plone-org_frontend state: deployed
Deploy: Completed
```

The database is up in seconds, the backends shortly after; Volto takes longest to start.

In the reference: {ref}`deploy-ref-deploy`.

## The first deploy: two steps by hand

A deploy brings up the services.
Two things it cannot do by itself, and both are needed exactly once per project.

### Before: the data directory

The database keeps its files in a directory on the node that holds persistent data.
Docker does not create it, so it has to exist before the first deploy.
Which node?

```shell
ssh root@play3.playcluster.plone.org mkdir -p /srv/playcluster-demo/data
```

`play3`, because `db_placement` pins the database to the node labelled `storage=persistent`.
Create it on `play2` instead, and nothing complains — until the deploy, when Swarm schedules the database on `play3`, finds no directory there, and the task fails with `failed to populate volume`.

### After: creating the Plone site

Once the deploy is green, the site is running but empty.
Traefik routes the request, Volto answers, and the backend has no Plone site to show:

- `/` returns an error, then Volto's own *"This page does not seem to exist…"*,
- `/++api++` returns 404.

The site is created once, inside one of the backend containers.
First find where the backends run:

```shell
ssh root@play1.playcluster.plone.org docker service ps playcluster-plone-org_backend --filter desired-state=running
```

Then, on one of the nodes in the `NODE` column:

```shell
ssh root@play2.playcluster.plone.org 'docker exec $(docker ps -qf name=playcluster-plone-org_backend | head -1) ./docker-entrypoint.sh create-site'
```

Its output looks worse than it is: a page of `WARNING` lines and two `ERROR:plone.dexterity.schema` lines about the `plone.allowdiscussion` and `plone.translatable` behaviors, which belong to add-ons this project does not install.
Reload the page, and the Volto welcome page appears.

Filter on the full `<stack>_backend` name.
With several projects on the cluster, one node can run backends of different stacks, and a filter on just `_backend` can pick the wrong one.

## Every deploy after that

From now on, a push to `main` is a release.
The pipeline builds new images, tagged with the new commit, and the deploy updates the running services one by one, while the database stays where it is.
The second deploy of the reference site today went from `sha-080716f7` to `sha-2d11b5e2` without anyone touching the cluster.

## Rolling back

Every build left an immutable `sha-…` image behind, so going back means deploying an older one.
The simplest way: {menuselection}`Deploy --> Environments --> production`, and **Re-deploy** an earlier deployment.

You can also run a pipeline on `main` with the variable `IMAGE_TAG` set to the tag you want.
The build jobs are skipped in such a pipeline, on purpose: building would push today's code under the old tag.
On `gitlab.com`, running a pipeline with variables has to be allowed first, under {menuselection}`Settings --> CI/CD --> Variables`.

## When it breaks

The stage that fails tells you where to look: `config` for settings, `check` and `test` for the code, `build` for the registry, `deploy` for the cluster.
The reference has the full table of symptoms and causes: {ref}`deploy-ref-operating`.
