---
myst:
  html_meta:
    "description": "What was changed in a vanilla cookieplone project to make it deployable on this cluster."
    "property=og:title": "2. What differs from vanilla cookieplone"
    "keywords": "cookieplone, GitLab CI, GitHub Actions, repository.toml"
---

(deploy-ref-differences)=

# 2. What differs from vanilla cookieplone

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

Generate a project with cookieplone today and you get GitHub Actions, no
`.gitlab-ci.yml`, and a stack file with the hostname written into it in eleven
places. This chapter is the diff.

## Start by not generating GitHub Actions

cookieplone asks which CI provider you want. Answer GitLab and you still get
`.github/workflows/` — the template only has GitHub Actions implemented. Delete
them at generation time rather than living with two CI systems:

```shell
rm -rf .github/workflows .github/dependabot.yml
```

Keep `.github/instructions/` if it is there; those are editor and assistant
instructions, unrelated to CI.

```{note}
The generated workflows would not have worked here anyway. They call
plone/meta's image job without a `registry` input, so it authenticates to
`ghcr.io` while naming images after `container_images_prefix` — two different
registries in one command. It is a template gap, not something you configured
wrongly.
```

Worth knowing for later: cookieplone-templates ships
`devops/README-GITLAB.md` describing a `.gitlab-ci.yml` it never generates, and
its `erral-gitlab-*` branches were abandoned in 2025, before the uv and
repoplone rewrite. They are not a starting point.

## What was added

```
.gitlab-ci.yml            stages, workflow rules, image pins, includes
.gitlab/ci/templates.yml  reusable job templates and the config job
.gitlab/ci/backend.yml    backend:lint, backend:test
.gitlab/ci/frontend.yml   frontend:lint, frontend:i18n, frontend:test
.gitlab/ci/changelog.yml  towncrier checks on merge requests
.gitlab/ci/deploy.yml     build:backend, build:frontend, deploy:production
```

Split by area rather than kept in one file, so a change to the frontend jobs
does not risk the deploy.

## What was changed

### repository.toml grew a deployment section

Vanilla cookieplone puts the hostname in the stack file, the stack name in the
Makefile, and the data path in both. Renaming a site meant editing four files
and the stack file's own name.

Now `repository.toml` declares it once:

```toml
[deployment]
gitlab_project = "plone-training1/training-deployment-gitlabdeploy"
hostname      = "playcluster.plone.org"
stack_name    = "playcluster-plone-org"
stack_prefix  = "reference"
stack_file    = "devops/stacks/stack.yml"
data_path     = "/srv/playcluster-demo/data"
db_placement  = "node.labels.storage == persistent"
app_placement = "node.labels.type == worker"

[deployment.local]
hostname = "playcluster-demo.localhost"

[deployment.traefik]
network = "nw-public"
constraint_label = "public"
entrypoint = "https"
certresolver = "le"
```

```{important}
`repoplone` parses `repository.toml` and **ignores unknown sections** — it does
not error, but it does not expose them either. So `repoplone settings dump`
will not show `[deployment]`. The pipeline and the Makefile read it directly
with `tomllib`.
```

Chapter 5 follows those values through to the running services.

`gitlab_project` is a safety catch. A copy of this repository in another GitLab
project would otherwise deploy with these exact values, replacing this
project's stack and writing into its database directory. The `config` job
refuses to build or deploy while `gitlab_project` does not match the project
the pipeline runs in; chapter 6 shows what a copy has to change.

### The stack file was rewritten

Renamed from `devops/stacks/<hostname>.yml`, the name cookieplone generates, to
`devops/stacks/stack.yml` — a hostname in a filename defeats the point — and
changed in three ways:

**It no longer ships Traefik.** The cluster already runs one holding ports 80
and 443, and only one service can. Deploying a second gives you:

```
failed to create service ..._traefik: port '80' is already in use
by service 'traefik_traefik' as an ingress port
```

The `traefik` service and every `ports:` entry are gone; routing is expressed
purely as labels for the cluster's instance.

**Nothing is hardcoded.** Every host-specific value is `${VAR}`, interpolated
by `docker stack deploy`. Required ones fail loudly:

```yaml
device: "${DATA_PATH:?set DATA_PATH to deployment.data_path from repository.toml}"
```

**Traefik object names are namespaced.** Router, service and middleware names
are global to the Traefik instance, not scoped to the stack. Two projects both
defining `rt-frontend` collide silently, so everything is prefixed:

```yaml
- traefik.http.routers.${STACK_PREFIX}-frontend.rule=Host(`${PUBLIC_HOSTNAME}`)
```

`gzip` is deliberately *not* prefixed — it belongs to the cluster's Traefik.

### The backend lint job does not use `make lint`

This one is worth remembering because the failure is invisible.
`backend/Makefile`'s `lint` runs `ruff check --fix` and `zpretty -i src`, and
`format` runs `ruff format`. All three **rewrite the files** and exit 0. Used in
CI, the job passes forever regardless of the code.

The pipeline calls the tools directly, in read-only mode:

```yaml
- uvx ruff@latest format --diff
- uvx ruff@latest check --diff
- uvx zpretty@latest --check src
```

The frontend's `make lint` is genuinely read-only (`eslint --max-warnings=0`,
`prettier --check`, stylelint) and is used as-is.

## Summary of the diff

| Vanilla cookieplone | Here |
| --- | --- |
| `.github/workflows/` | `.gitlab-ci.yml` + `.gitlab/ci/` |
| Hostname in 11 places | `repository.toml` `[deployment]` |
| Stack file named after the host | `devops/stacks/stack.yml` |
| Stack ships its own Traefik | Labels for the cluster's Traefik |
| Unprefixed Traefik names | `${STACK_PREFIX}-*` |
| `make lint` in CI | ruff/zpretty called directly |
| Images to `ghcr.io` | zot on `play4`, at `registry.playcluster.plone.org` |
