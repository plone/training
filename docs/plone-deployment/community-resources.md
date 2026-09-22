---
myst:
  html_meta:
    "description": "The community templates and tools this training is built from, and what was added on top of them."
    "property=og:description": "The community templates and tools this training is built from, and what was added on top of them."
    "property=og:title": "Community resources"
    "keywords": "Plone, cookieplone, cookieplone-templates, GitLab CI, Ansible, Docker Swarm"
---

(community-resources-label)=

# Community resources

This training shows an end result, not how to generate it. But almost nothing in the two
repositories was written from scratch. Most of it comes from templates and tools the Plone
Community already maintains, and this chapter says which, so you can find your way back to the
source when you build your own setup.

## Cookieplone

[Cookieplone](https://github.com/plone/cookieplone) generates Plone projects from the templates in
[cookieplone-templates](https://github.com/plone/cookieplone-templates). It is how a new Plone 6
project is started today; see
[Create a project with Cookieplone](https://6.docs.plone.org/install/create-project-cookieplone.html)
in the Plone documentation, and Cookieplone's own documentation at
<https://plone.github.io/cookieplone/>.

Both training repositories started as Cookieplone output:

[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster)
: The cluster. It started from the Ansible setup Cookieplone's `project` template can generate
  under `devops/ansible`, and grew from a single host into four: a Docker Swarm manager, two
  workers, and a separate host for the GitLab Runner and the container registry.

[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy)
: The deploy demo, a Plone 6 project with a Volto frontend. It was generated with the `project`
  template, using a subset of its options: no Ansible playbooks, since the cluster repository
  covers those; no Varnish cache; no GitHub Actions deploy workflow; and `gitlab` as the container
  registry.

## What was added: the GitLab CI/CD layer

Cookieplone generates GitHub Actions workflows. Choosing GitLab gives you a `devops/README-GITLAB.md`
describing a pipeline, but no `.gitlab-ci.yml`. So the deploy demo adds a GitLab layer on top of
what Cookieplone generates, and this is all of it:

| | File | What it is |
| --- | --- | --- |
| new | `.gitlab-ci.yml` | Stages, workflow rules, image pins, includes |
| new | `.gitlab/ci/config.yml` | The first job: reads `repository.toml` and publishes the settings to every later job |
| new | `.gitlab/ci/templates.yml` | Shared job templates and rules |
| new | `.gitlab/ci/backend.yml`, `frontend.yml`, `changelog.yml` | Lint, test, i18n, changelog checks |
| new | `.gitlab/ci/deploy.yml` | Image builds and the swarm deploy |
| replaced | `devops/stacks/stack.yml` | Instead of `devops/stacks/<hostname>.yml`: no own Traefik, every host-specific value a variable |
| rewritten | `devops/README-GITLAB.md` | The CI/CD reference |
| extended | `repository.toml` | `[deployment]`, `[deployment.local]` and `[deployment.traefik]`: every host-specific value, once |
| extended | `Makefile`s | `debug-settings`, `release-tag`, and targets that read `[deployment]` |
| extended | `backend/Dockerfile`, `frontend/Dockerfile` | A `MAINTAINER` build argument |
| extended | `docker-compose.yml` | The local stack, from `[deployment.local]` |
| removed | `.github/workflows/` | |

Seven new files, a handful of extended ones, one directory removed. The part I like most is the
`[deployment]` section in `repository.toml`: every value that differs between one deployment and
the next lives there, so the pipeline, the stack file and the local stack never need editing for a
new host name.

## Tools the pipeline reuses

[repoplone](https://pypi.org/project/repoplone/)
: Reads `repository.toml` and reports the project's Python, Plone and Volto versions. The pipeline's
  first job asks it, so no version is written down twice.

The Plone container images
: `plone/server-builder` and `plone/server-prod-config` for the backend, `plone/frontend-builder`
  for the frontend. The project's Dockerfiles build on them.

[docker-stack-deploy](https://github.com/kitconcept/docker-stack-deploy)
: A small image that logs in to a registry, connects to a Docker Swarm manager over SSH, and runs
  `docker stack deploy`. It was written as a GitHub Action by kitconcept, and works unchanged as the
  image of a GitLab job.

[zot](https://zotregistry.dev/)
: The container registry on the CI host: one container, with per-repository access control.

Ansible roles
: `geerlingguy.docker` and `geerlingguy.swap` for the hosts, and
  [`riemers.gitlab-runner`](https://galaxy.ansible.com/ui/standalone/roles/riemers/gitlab-runner/)
  to install and register the GitLab Runner.

## Where this could go next: extending Cookieplone

Cookieplone 2.0 can **extend** an upstream templates repository. You create your own templates
repository, point its `cookieplone-config.json` at `gh:plone/cookieplone-templates`, and redeclare
the templates you want to change. At generation time Cookieplone lays your files over the upstream
template: see
[Extend an upstream template repository](https://plone.github.io/cookieplone/how-to-guides/extend-an-upstream-template-repository.html).

That fits the GitLab layer above almost exactly. The table is, in effect, the specification of such
a templates repository: a Cookieplone project, generated as usual, that comes out with GitLab CI/CD
already in place. Three things make it more than copying files:

- **New files** are easy: the overlay adds them. They are close to static, because everything
  host-specific comes from `repository.toml`.
- **Extended files** are harder: the overlay replaces a file completely, so each one becomes a copy
  of the upstream template with the changes on top, to be kept in step with upstream.
- **Removals**, such as `.github/workflows/`, are not possible with an overlay alone.

I did not get to build it before this training. It is the next step, as a third repository next to
the two used today, so that a GitLab-based Plone project becomes one Cookieplone command instead of
a training day.

## Last year's training

If you want to deploy your own first project to a single host, step by step, the
[2025 deployment training](https://2025.training.plone.org/) is still the better starting point. It
uses Cookieplone's defaults directly, where this training shows where they lead.
