---
myst:
  html_meta:
    "description": "Stages, workflow rules, the config job, and how jobs reach the runner."
    "property=og:title": "3. The pipeline"
    "keywords": "GitLab CI, stages, dotenv, runner tags, workflow rules"
---

(deploy-ref-pipeline)=

# 3. The pipeline

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

Five stages. `.pre` is built into GitLab and runs before everything else.

```
.pre      config
check     backend:lint  frontend:lint  frontend:i18n  changelog:*
test      backend:test  frontend:test
build     build:backend  build:frontend
deploy    deploy:production
```

## When a pipeline runs at all

`workflow:rules` in `.gitlab-ci.yml` decides, before any job is considered:

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
```

Rules are evaluated top to bottom and the first match wins. The third is the
interesting one: without it, pushing to a branch with an open merge request
creates *two* pipelines for the same commit.

Then each job narrows further. Two shared rule sets, in
`.gitlab/ci/templates.yml`:

```yaml
.rules-code:      # merge requests, branches, main, tags
.rules-release:   # main and tags only
```

`build` and `deploy` use `.rules-release`. Nothing publishes an image or touches
the cluster from a branch.

## The config job

One job resolves everything, so no other job re-derives it.

```yaml
config:
  extends: .uv-job
  stage: .pre
```

It does four things:

1. Runs `uvx repoplone settings dump` for the Python, Plone and Volto versions.
2. Picks the registry (chapter 4).
3. Computes the image tag: the git tag on a tag pipeline, `sha-<short>`
   otherwise.
4. Reads `[deployment]` from `repository.toml` with `tomllib`.

Its log prints everything it resolved, which makes it the first place to look
when a deploy goes somewhere unexpected.

### Two kinds of output, for one specific reason

GitLab caps a **dotenv report at 20 variables** and rejects a larger one with an
unhelpful `400 Bad Request`. This pipeline needs more than 20 values, so they
are split by what they are *for*:

```yaml
  artifacts:
    paths:
      - deploy.env      # ordinary artifact, no limit
    reports:
      dotenv: build.env # real CI/CD variables, max 20
```

**`build.env`** holds only what must become an actual CI/CD variable — the build
arguments, and `DEPLOY_URL`, because `environment:url` is resolved by GitLab
rather than by a shell. Seven entries.

**`deploy.env`** holds everything the stack file interpolates. The deploy job
sources it:

```yaml
- set -a && . ./deploy.env && set +a
```

Values are written with `shlex.quote`, because several contain spaces —
`node.labels.storage == persistent` would otherwise become three words.

A guard fails the job with a clear message if the dotenv report ever exceeds 20
again, rather than letting GitLab's 400 appear at upload time.

## How jobs reach the runner

Every job carries a tag, and GitLab matches it against the runner's registered
tags:

```yaml
variables:
  RUNNER_TAG_BUILD: docker
  RUNNER_TAG_DEPLOY: deploy
```

```yaml
tags:
  - ${RUNNER_TAG_BUILD}
```

Two names rather than one, so a deploy runner closer to the cluster can be
introduced later without touching any job.

If no runner carries the tag, the job sits pending and GitLab reports "no
runners that match all of the job's tags". The runner registers with an
authentication token (`glrt-…`), and with those the tags belong to GitLab: they
are set when the runner is created, and changed under
{menuselection}`Build --> Runners` in the group. They are **not** in
`config.toml` on the runner host, where grepping for them finds nothing, and not
in the `training-deployment-playcluster` repository's Ansible settings either.

## Why there is no docker:dind

The obvious way to build images in CI is a `docker:dind` service. This pipeline
deliberately has none, because of how the runner is configured:

```yaml
docker_volumes:
  - "/var/run/docker.sock:/var/run/docker.sock"
```

With the host's socket mounted into job containers, a dind service cannot create
its own socket:

```
failed to load listeners: can't create unix socket /var/run/docker.sock:
device or resource busy
```

It then fails its health check for the full 30 second timeout — on every build
job — while the build proceeds against the host daemon regardless. Removing the
service costs nothing and saves 30 seconds twice per pipeline.

```{warning}
The consequence is that builds are **not isolated** from `play4`'s
Docker daemon. A job can control every container on that host. That is
tolerable because the host is dedicated to CI and sits outside the swarm; it
would not be on a cluster node. If the socket mount is ever removed from the
runner, put `services: [docker:dind]` and `DOCKER_TLS_CERTDIR` back.
```

## Parallelism

Each check and test job declares `needs: ["config"]`:

```yaml
"backend:lint":
  stage: check
  needs: ["config"]
```

With `needs`, a job starts as soon as its dependency finishes rather than
waiting for the whole preceding stage. So all five start together instead of
three, then two. The runner allows four concurrent jobs
(`concurrent_specific: 4`), so that is roughly the useful width.

`build` and `deploy` deliberately have **no** `needs`, which leaves them under
plain stage ordering — they wait for every check and test to pass.

The trade-off: a fast lint failure no longer prevents the slower test jobs from
starting. On a dedicated runner that is a good trade.

## Validating a change before pushing

```shell
npx --yes gitlab-ci-local@latest --list
```

Resolves `extends`, `include` and `!reference` exactly as GitLab does, validates
against GitLab's CI JSON schema, and prints the resolved job list.

```{tip}
One trap a YAML syntax check cannot catch: a `: ` — colon followed by a space —
inside an unquoted `script` line turns that entry into a mapping. GitLab then
rejects the job with `script config should be a string or a nested array of
strings`, while the file remains perfectly valid YAML. Avoid colon-space in
script lines, or quote the whole entry.
```
