---
myst:
  html_meta:
    "description": "Provision the standalone GitLab CI runner and container registry host."
    "property=og:title": "5. The CI runner host"
    "keywords": "GitLab Runner, registry, Ansible, Docker"
---

(playcluster-ref-ci-runner)=

# 5. The CI runner host

% Exported from training-deployment-playcluster 00fc574 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

`play4` is deliberately **not** part of the swarm. It builds container
images and hosts the registry. Keeping it separate means a runaway build cannot
disturb the cluster serving traffic.

It gets its own playbook and its own inventory group. The group `standalone`
contains only `play4`, and `group_vars/standalone/` holds settings that apply to
nothing else.

## Before you run: a runner token

The runner registers with GitLab using a token that GitLab issues, so create the
runner on the GitLab side first. Register it on a **group** rather than a single
project: a group runner takes jobs from every project in the group, so a new
project can use the cluster without further setup.

1. In the group, go to {menuselection}`Build --> Runners` and choose
   {guilabel}`New group runner`. (For a single project:
   {menuselection}`Settings --> CI/CD --> Runners`, {guilabel}`New project runner`.)
2. Under **Tags**, enter `docker` and `deploy`.
3. Create the runner, and copy the token that starts with `glrt-`. GitLab shows
   it once. Ignore the `gitlab-runner register` command on the same page —
   Ansible runs the equivalent.

Put the token in the vault, in place of the placeholder under
`gitlab.runner_tokens.play4`:

```shell
uv run ansible-vault edit inventory/group_vars/all/vault.yml
```

## Run it

```shell
uv run ansible-playbook playbooks/setup_ci.yml --limit play4.playcluster.plone.org
```

This run takes longer than the others: installing and registering the GitLab
Runner adds several minutes.

`--limit standalone` does the same, since `play4` is the only host in that group.

## What it sets up

Base configuration as before — proxy, packages, hostname, users, SSH, Docker —
and then two things specific to this host:

- **A GitLab Runner**, registered against `gitlab.com`, running jobs in
  Docker containers.
- **A container registry** (zot) at <https://registry.playcluster.plone.org>,
  deployed with Docker Compose rather than as a swarm stack, since this host is
  not in the swarm. It has its own web UI on port 7443, and its settings live in
  `inventory/group_vars/standalone/registry.yml`.

Several runner tasks show `(censored due to no_log)` instead of their details.
That is deliberate: they handle the runner token, and the role keeps it out of
the output.

Re-run just the registry when you change it:

```shell
uv run ansible-playbook playbooks/setup_ci.yml --limit standalone --tags registry
```

## Where the runner is configured

`inventory/group_vars/standalone/runners.yml`. This is the file you edit when
CI behaves oddly, and it is worth reading now rather than when something breaks:

```yaml
gitlab_runner_coordinator_url: "https://gitlab.com"
gitlab_runner_registration_token_type: "authentication-token"

gitlab_runner_runners:
  - name: "play4.playcluster.plone.org"
    concurrent_specific: 4
    token: "{{ vault.gitlab.runner_tokens.play4 }}"
    executor: "docker"
    docker_image: "docker:latest"
    docker_volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "/builds:/builds"
      - "/cache"
    extra_configs:
      runners.docker:
        privileged: true
```

Four lines deserve attention.

**`token`** comes from the encrypted vault, not from this file. It is the
runner's authentication token, and anyone holding it can pose as this runner
and receive your CI jobs — including their CI/CD variables.

**`concurrent_specific: 4`** caps parallel jobs on this runner. Too low and
pipeline stages queue; too high and builds fight over CPU. Match it to the
host's core count.

**`docker_volumes` mounts the Docker socket.** This is the single most
consequential line here. It lets CI jobs use the host's Docker daemon directly,
which makes image builds fast and keeps the layer cache warm between jobs.

It also has two consequences worth stating plainly:

- A job that starts a `docker:dind` service will find that service unable to
  create its own socket — it fails with `device or resource busy` after a 30
  second timeout, while the build quietly proceeds against the host daemon
  anyway. Pipelines on this runner should not use `dind`.
- A CI job can control every container on this host. That is acceptable because
  the host is dedicated to CI and is outside the swarm. It would not be
  acceptable on a cluster node.

**`privileged: true`** is required by some build tooling. With the socket
already mounted it adds little further exposure, but both are reasons this host
stays separate.

## Runner tags

A GitLab job can require a runner tag, and will sit pending forever if no runner
carries it — reported as "no runners for the protected branch, or no runners
that match all of the job's tags". The pipelines this cluster is built for send
build jobs to runners tagged `docker` and deploy jobs to runners tagged `deploy`,
so the runner needs both.

With an authentication token (`glrt-…`), tags belong to GitLab, not to the
runner. They are set in GitLab when the runner is created, and changed there
afterwards: in the group, {menuselection}`Build --> Runners`, then edit the
runner. They are not written in `config.toml` on the host, and adding `tags:` to
`runners.yml` does not change them — `gitlab-runner register` does not accept
tags together with an authentication token.

## Verify

On `play4`:

```shell
systemctl status gitlab-runner
```

```shell
grep -E '^(concurrent|check_interval) =' /etc/gitlab-runner/config.toml
```

`concurrent` should match the vCPU count. Then confirm GitLab agrees the runner
is online, under {menuselection}`Build --> Runners` in the group — a runner can
be healthy locally and still not be registered.

```{warning}
`gitlab-runner list` prints the runner's authentication token in full. Do not
run it while sharing your screen, and do not paste its output anywhere.
```

## Check the registry

From your own machine:

```shell
curl -sI https://registry.playcluster.plone.org/v2/ | head -1
```

`HTTP/2 401`: TLS works and anonymous access is refused. The registry has three
entrances on the same host name:

`https://registry.playcluster.plone.org/v2/`
: The registry API that `docker` uses, on port 443. Only `/v2/` is served here.

`https://registry.playcluster.plone.org:7443/`
: zot's web UI. Sign in with the `ci` or `deploy` account.

`https://registry.playcluster.plone.org:8443/dashboard/`
: The dashboard of the Traefik in front of the registry, with the same
  credentials as the cluster's Traefik dashboard.

The two accounts have different rights, and it is worth proving that once. Log
in as `ci` and push a throwaway image:

```shell
docker login registry.playcluster.plone.org -u ci
```

```shell
docker pull alpine:3 && docker tag alpine:3 registry.playcluster.plone.org/probe/alpine:test && docker push registry.playcluster.plone.org/probe/alpine:test
```

Then log in as `deploy`. Pulling works; pushing must fail with *requested access
to the resource is denied*:

```shell
docker login registry.playcluster.plone.org -u deploy
```

```shell
docker pull registry.playcluster.plone.org/probe/alpine:test && docker push registry.playcluster.plone.org/probe/alpine:test
```

The swarm pulls with `deploy` and stores those credentials on every node, which
is why that account must not be able to push.

Running the registry from here on — its layout, the web UI and dashboard ports,
and the retention policy that is still in dry-run mode — is covered in chapter 7.

## You are done

The cluster runs, Traefik is routing, and CI has somewhere to build. One step
remains on the GitLab side: chapter 6 sets the CI/CD variables that let a
pipeline push to this registry and deploy to this swarm.

The other half is a cookieplone Plone 6 project with a GitLab pipeline that
lints, tests, builds images into this registry, and deploys a stack onto this
swarm.

Two things from these chapters carry directly into it — the Traefik discovery settings
from chapter 3 (`constraint-label`, `nw-public`, the `le` resolver, the entrypoint
names), and the socket-mounted runner from this chapter, which decides how the
build jobs must be written.
