---
myst:
  html_meta:
    "description": "Configuring the project in GitLab, reading a failed pipeline, rolling back, and creating the Plone site."
    "property=og:title": "6. Operating it"
    "keywords": "GitLab CI variables, rollback, create-site, troubleshooting"
---

(deploy-ref-operating)=

# 6. Operating it

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

## What has to be configured in GitLab

The runner and the CI/CD variables are set once, on the GitLab group, and every
project in the group inherits them. The `training-deployment-playcluster`
documentation, chapter 6, explains each in full; in short:

| Variable | Value | Protected | Masked |
| --- | --- | --- | --- |
| `REGISTRY_IMAGE_PREFIX` | `registry.playcluster.plone.org/$CI_PROJECT_PATH` | **No** | No |
| `REGISTRY_USER` / `REGISTRY_PASSWORD` | zot push account `ci` | Yes | password only |
| `REGISTRY_PULL_USER` / `REGISTRY_PULL_PASSWORD` | zot read-only account `deploy`, handed to the swarm | Yes | password only |
| `DEPLOY_HOST` | the swarm manager, `play1.playcluster.plone.org` | Yes | No |
| `DEPLOY_USER` | `plone`, the deployment user on the cluster | Yes | No |
| `DEPLOY_SSH_PRIVATE_KEY` | its private key, as type *Variable* | Yes | Not possible, multi-line |

`$CI_PROJECT_PATH` in `REGISTRY_IMAGE_PREFIX` is expanded by the `config` job,
not by GitLab, which passes a group variable's reference to a predefined variable
through literally. That is what lets one group variable serve every project.

```{important}
**Protected** variables are only exposed on protected refs. Since deploys only
run from `main` and from tags, that is what you want — but `main` must be a
protected branch, and release tags need a protected tag rule, `*`. Otherwise the
variables arrive empty and the deploy fails with an SSH error rather than
anything that mentions variables.
```

Everything else — hostname, stack name, placement, Traefik settings — lives in
`repository.toml` and is version-controlled. Only secrets and the registry
prefix are configured in the GitLab UI.

## The first deploy

The cluster provides the `nw-public` network and the node labels when it is
provisioned. One thing is per project, and has to exist before that project's
first deploy: its **data directory**, on the node that holds persistent data.
That is the node labelled `storage=persistent`, which is `play3`:

```shell
ssh root@play3.playcluster.plone.org mkdir -p /srv/playcluster-demo/data
```

It has to be on `play3`. `db_placement` only ever schedules the database there,
so the same directory on any other node is never used, and without it on `play3`
the database task fails with `failed to populate volume`.

Once the stack is running, the Plone site itself has to be created — the
database is empty until it is. First find where the backend replicas landed; the
`NODE` column says which host:

```shell
ssh root@play1.playcluster.plone.org docker service ps playcluster-plone-org_backend --filter desired-state=running
```

Then, on one of those nodes — `play2` in this example:

```shell
ssh root@play2.playcluster.plone.org 'docker exec $(docker ps -qf name=playcluster-plone-org_backend | head -1) ./docker-entrypoint.sh create-site'
```

Filter on the full `<stack>_backend` name, not just `_backend`: with more than
one project on the cluster, a node can run several stacks' backends, and a loose
filter can pick another project's container.

This is a one-off. Later deploys keep the database.

## Deploying a copy of this project

A second project on the cluster starts as a copy of this repository in a new
GitLab project in the same group. The runner and the variables come with the
group, and `REGISTRY_IMAGE_PREFIX` gives the copy its own path in the registry
through `$CI_PROJECT_PATH`. What it must not inherit is this project's
`[deployment]` section.

A fresh copy's first pipeline on `main` stops in the `config` job:

```
repository.toml [deployment] still describes plone-training1/training-deployment-gitlabdeploy,
but this pipeline runs in plone-training1/project2.
Set your own hostname, stack_name, stack_prefix and data_path in [deployment],
then set gitlab_project = "plone-training1/project2".
```

That is on purpose. With the original's values, the copy would replace the
original's stack, and its database would write into the original's data
directory. Branches and merge requests of the copy still lint and test; only
building and deploying waits.

So, in the copy's `repository.toml`:

```toml
[deployment]
gitlab_project = "plone-training1/project2"
hostname       = "project2.playcluster.plone.org"
stack_name     = "project2-playcluster-plone-org"
stack_prefix   = "project2"
data_path      = "/srv/project2/data"
```

Change all five together. The check only catches a copy that changed nothing:
one that updates `gitlab_project` but keeps `data_path` would still share the
original's database directory.

Then the same two one-off steps as above: the data directory on `play3` before
the first deploy, and `create-site` after it. The host name also needs a DNS
record pointing at `play1`.

Some mistakes along the way are instructive rather than harmful, and chapter 5
explains each: a `stack_prefix` shared with another project makes Traefik's
router names collide, a host name without DNS gets no certificate, and a missing
data directory stops the database from starting.

## Triggering a deploy

Three ways, in the order you will reach for them:

**Push to `main`.** The normal path. Builds both images tagged
`sha-<short-sha>` and deploys them. No tag, no ceremony.

**Run a pipeline by hand.** {menuselection}`Build --> Pipelines --> Run
pipeline` on `main`. The same thing, on demand — useful when the deploy failed
for a reason outside the code, or to redeploy an older image (see below).

**Cut a release tag.** When you want the deployed thing to carry a name you
chose rather than a sha:

```shell
make release-tag
```

That tags the current commit with the contents of `version.txt`, pushes the
tag, and the pipeline builds and deploys it — images named after the release,
which is what you want when someone asks six months later what is running. It
refuses on a dirty tree, off `main`, with unpushed commits, or when the tag
already exists, because each of those produces a tag that does not mean what
it says.

Only version-shaped tags deploy — `1.0.0a1`, `2.0`, `v1.4.2`. Any other tag is
still linted and tested, but builds nothing and deploys nothing.

## Rolling back

Every build published an immutable `sha-…` tag, so rolling back is deploying an
older one. Two ways:

**From the UI.** {menuselection}`Deploy --> Environments --> production`, then
`Re-deploy` on an earlier deployment.

**From a new pipeline.** {menuselection}`Build --> Pipelines --> Run pipeline`
on `main`, with a variable:

| Key | Value |
| --- | --- |
| `IMAGE_TAG` | `sha-abc1234` |

A variable set by hand outranks the one `config` computes, so the deploy uses
the tag you gave it. The build jobs do not run in such a pipeline: their rules
skip them when `IMAGE_TAG` is set by hand. Otherwise they would build today's
code and push it under the old tag, the "rollback" would deploy today's code,
and the old image would lose its tag.

```{note}
On GitLab.com, new projects do not allow pipeline variables: the form under
{menuselection}`Run pipeline` then shows no variables section at all. To allow
them, set {menuselection}`Settings --> CI/CD --> Variables --> Minimum role to use pipeline variables`
to *Maintainer*. The first way, **Re-deploy** from the environment, works
either way.
```

## Reading a failure

The pipeline is designed so the *stage* that fails tells you where to look.

| Fails at | Almost always |
| --- | --- |
| `config` | A missing variable, or `repository.toml` missing a required key. It prints what it resolved — read that first |
| `backend:lint` | Real lint findings. `ruff --diff` shows exactly what it wants |
| `frontend:i18n` | Locales regenerate differently from what is committed. Run `make i18n` and commit the result |
| `backend:test` | Real test failures |
| `build:*` | Registry credentials, or a genuine build error. `Login Succeeded` early in the log rules out the first |
| `deploy:production` | See below |

Deploy failures are worth reading precisely, because the phase lines narrow it
down immediately:

| Last line seen | Meaning |
| --- | --- |
| nothing, or "No pull credentials" | `REGISTRY_PULL_*` unset and no deploy token |
| `Container Registry: Logged in` | Registry fine; SSH is next |
| `SSH connect: Failed` | `DEPLOY_HOST` / `DEPLOY_USER` / key wrong, or the key is not in `authorized_keys` |
| `Deploy: Failed to deploy` | The stack file was rejected. Read the Docker error immediately above it |
| `Deploy: Checking status` then a timeout | The stack deployed but a service never became healthy |

That last one is the interesting case. The deploy succeeded as far as Swarm is
concerned, and the problem is in the cluster:

```shell
docker stack ps <stack> --no-trunc
```

`--no-trunc` matters — the useful part of a Swarm error is always past the
truncation point. Common causes, all seen while building this:

- **`no suitable node`** — a placement constraint no node satisfies. Check the
  constraint against the actual node labels.
- **`failed to populate volume`** — the bind-mount path does not exist on that
  node.
- **`port is already in use`** — something else holds 80/443. Only the cluster
  Traefik may.

## When the site does not answer

The deploy succeeded, services are running, and the URL does nothing. That is
almost always Traefik discovery rather than the application.

Work through it in this order:

```shell
docker service logs traefik_traefik --tail 50 | grep -i "error\|skip"
```

`Skip container ... both Docker and Swarm labels are defined` means the service
defines both network labels and Traefik ignored it entirely.

If there is no mention of your service at all, it is not being discovered:
check `traefik.constraint-label` matches what the cluster Traefik filters on,
and that the service is attached to `nw-public`.

If a router exists but requests 404, the router is there and the rule does not
match — compare the `Host()` rule with the hostname you are actually requesting.

## A couple of things that look broken but are not

**Backends crash-looping for a few seconds after a deploy.** `depends_on` is
silently ignored by `docker stack deploy`, so backends start before Postgres is
accepting connections. Swarm restarts them and it settles. Noisy, harmless.

**`cache: not found` in a build log.** Expected on the first build of an image,
or after the cache is garbage-collected. It should disappear on the next run —
if it never does, the cache export is not working.

**Errors in the `create-site` output.** Creating the site logs a page of
`WARNING:GenericSetup…` and `Redefining mime type` lines, and two errors:

    ERROR:plone.dexterity.schema:Error resolving behavior plone.allowdiscussion for factory Document
    ERROR:plone.dexterity.schema:Error resolving behavior plone.translatable for factory Document

The default Document type mentions behaviors from discussion and multilingual
support, which are separate add-ons that this project does not install. The site
is created correctly regardless.

## Where to go next

- `devops/README-GITLAB.md` in this repository — the reference version of the
  setup, kept next to the code
- The `training-deployment-playcluster` repository — the cluster this deploys onto
- `.gitlab/ci/templates.yml` — the templates every job extends, and the most
  useful single file to read once
