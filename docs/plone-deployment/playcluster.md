---
myst:
  html_meta:
    "description": "The deploy demo: a cookieplone Plone 6 project extended to build and deploy itself onto the playcluster."
    "property=og:description": "The deploy demo: a cookieplone Plone 6 project extended to build and deploy itself onto the playcluster."
    "property=og:title": "The deploy demo"
    "keywords": "Plone, cookieplone, Volto, repository.toml, Docker Swarm, GitLab CI"
---

(playcluster-label)=

# The deploy demo

This morning we built the cluster.
This afternoon we follow a Plone project from a `git push` to a running site on it.

The project is [training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy), and it is already running: <https://playcluster.plone.org>.
Everything shown this afternoon is in that repository, and every path mentioned is real.
The reference documentation for it is included in this training, starting at {ref}`deploy-ref-overview`.

## A cookieplone project

The project was generated with Cookieplone's `project` template, like any new Plone 6 project today.
It is a monorepo, one repository holding everything that is released together:

```
backend/          Plone, installed with uv. Python package: playclusterdemo
frontend/         Volto. Add-on: volto-playclusterdemo
devops/           The Docker Swarm stack file
.gitlab/          The pipeline
repository.toml   Project settings, and where it is deployed
```

Two tools keep the versions in one place.
`repoplone` reads `repository.toml` and reports the Python, Plone and Volto versions, and both Makefiles ask it while they are parsed.
You can see what the project resolves on your own machine, without deploying anything:

```shell
make debug-settings
```

```console
PROJECT_NAME: playcluster-demo
VOLTO_VERSION: 19.3.0
PLONE_VERSION: 6.2.1
PUBLIC_HOSTNAME: playcluster.plone.org
LOCAL_HOSTNAME: playcluster-demo.localhost
STACK_NAME: playcluster-plone-org
STACK_FILE: devops/stacks/stack.yml
```

Every one of those values comes out of `repository.toml`.
In the reference: {ref}`deploy-ref-project`.

## What was added to cookieplone

Cookieplone generates GitHub Actions workflows, not GitLab CI.
So the project was generated with a subset of the template's options — no Ansible, no Varnish, no GitHub deploy workflow — and a GitLab layer was added on top: seven new files, a few extended ones, and `.github/workflows/` removed.
{ref}`community-resources-label` lists all of them.

Three of the changes shape everything we will see this afternoon:

The pipeline
: `.gitlab-ci.yml` and five files in `.gitlab/ci/`, split by area so that a change to the frontend jobs does not risk the deploy.

The stack file
: `devops/stacks/stack.yml`, renamed from the `devops/stacks/<hostname>.yml` Cookieplone generates.
  It ships **no Traefik**: the cluster already runs one on ports 80 and 443, and only one service can hold those.
  The stack only carries labels that the cluster's Traefik reads.

`repository.toml`
: A new `[deployment]` section, described next.

In the reference: {ref}`deploy-ref-differences`.

## One place for everything host-specific

In a vanilla Cookieplone project, the host name sits in the stack file, the stack name in the Makefile, and the data path in both.
Renaming a site meant editing four files, and the name of one of them.

Here, every value that differs between one deployment and the next is in `repository.toml`, once:

```toml
[deployment]
gitlab_project = "plone-training1/training-deployment-gitlabdeploy"
hostname       = "playcluster.plone.org"
stack_name     = "playcluster-plone-org"
stack_prefix   = "reference"
stack_file     = "devops/stacks/stack.yml"
data_path      = "/srv/playcluster-demo/data"
db_placement   = "node.labels.storage == persistent"
app_placement  = "node.labels.type == worker"

[deployment.traefik]
network          = "nw-public"
constraint_label = "public"
entrypoint       = "https"
certresolver     = "le"
```

The pipeline reads it, the local Docker stack reads it, and the swarm stack file is filled in from it at deploy time.
Change the host name here, and it reaches the router rule, the Volto API path and the Plone virtual host rewrites without touching another file.

Some of these values connect straight to this morning:

- `db_placement` pins the database to the node labelled `storage=persistent`: `play3`.
- `app_placement` keeps the frontend and backend on the workers, `play2` and `play3`, and off the manager.
- `[deployment.traefik]` has to match the cluster's Traefik exactly: its network, the label it filters on, its entrypoint and its certificate resolver.
  Get one wrong, and the site is simply not routed, usually without an error anywhere.

`gitlab_project` is a safety catch that we will meet again when you deploy a copy of this project.

## The images

The pipeline builds two container images, and so can you, with `make build-images`.

The backend
: Plone installed with `uv` from a locked dependency tree, on top of `plone/server-builder` and `plone/server-prod-config`.
  The dependencies are installed before the source code is copied in, so a code change does not rebuild the dependency layer.

The frontend
: Volto, on top of `plone/frontend-builder`.
  Volto itself is not in the repository: `mrs.developer.json` pins a version, and the build fetches it from GitHub.

Both land in the cluster's own registry, under the project's path:

```
registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy/backend
registry.playcluster.plone.org/plone-training1/training-deployment-gitlabdeploy/frontend
```

## Where it runs

This is how the reference deployment is spread over the cluster right now:

| Service | Replicas | Runs on |
| --- | --- | --- |
| `db` (Postgres) | 1 | `play3`, the `storage=persistent` node |
| `backend` (Plone) | 2 | `play2` and `play3` |
| `frontend` (Volto) | 2 | `play2` and `play3` |

The manager, `play1`, runs none of it: it runs Traefik, which routes `playcluster.plone.org` to the frontends, and the frontends and Traefik on to the backends.

The next chapter follows the pipeline that put it there.
