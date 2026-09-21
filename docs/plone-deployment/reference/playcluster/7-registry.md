---
myst:
  html_meta:
    "description": "The zot container registry on play4: layout, accounts, web UI, Traefik dashboard and retention."
    "property=og:title": "7. The registry in detail"
    "keywords": "zot, container registry, Docker Compose, Traefik, retention, GitLab CI"
---

(playcluster-ref-registry)=

# 7. The registry in detail

% Exported from training-deployment-playcluster 00fc574 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

Chapter 5 brings `play4` up and checks that the registry answers. This chapter
is the reference for running it afterwards: how it is put together, why it has
two accounts, what its three ports are for, and what to change before it starts
deleting old images.

Everything here is configured in `inventory/group_vars/standalone/registry.yml`.

## Why a Compose project, not a swarm stack

`play4` is deliberately not a swarm node. Joining it to the swarm would put a
second Traefik into the cluster, competing for ports 80 and 443, and would drop
the CI runner's containers into an orchestrated environment. So the registry,
[zot](https://zotregistry.dev/) behind its own Traefik, is a plain Docker
Compose project, deployed by Ansible in the same shape as the swarm stacks:

| | Swarm (`play1`–`play3`) | Compose (`play4`) |
| --- | --- | --- |
| Definition | `stacks` in `inventory/group_vars/all/stacks.yml` | `compose_projects` in `inventory/group_vars/standalone/compose.yml` |
| Deployment | `tasks/stacks/task_deploy.yml` | `tasks/compose/task_deploy.yml` |
| Files | `etc/stacks/*.yml` | `etc/compose/*.yml` |

Deploy or redeploy just the registry:

```shell
uv run ansible-playbook playbooks/setup_ci.yml --limit standalone --tags registry
```

Everything lands in `/srv/registry` on the host, as `compose.yml` plus a
generated `.env`, so the usual Compose commands work there directly:

```shell
ssh root@play4.playcluster.plone.org 'cd /srv/registry && docker compose ps && docker compose logs --tail=50 registry'
```

## Two accounts, on purpose

| Account | Rights | Used by |
| --- | --- | --- |
| `ci` | read, create, update, delete | CI build jobs, pushing images and the BuildKit layer cache |
| `deploy` | read only | The swarm, pulling images during `docker stack deploy` |

The split is not cosmetic. `docker stack deploy --with-registry-auth` copies the
deploying client's registry credentials onto every swarm node, where they stay,
so the nodes can pull again after a reboot. Push rights must never land there,
so the swarm only ever gets `deploy`.

These are registry logins, not accounts on the hosts. The SSH account that runs
`docker stack deploy` is `plone`; see chapter 1.

Anonymous access is refused. The passwords live in the vault, and Ansible turns
them into a bcrypt `htpasswd` file on the host. Read them back with:

```shell
uv run ansible-vault view inventory/group_vars/all/vault.yml
```

In GitLab they become the CI/CD variables `REGISTRY_USER` and `REGISTRY_PASSWORD`
(`ci`), and `REGISTRY_PULL_USER` and `REGISTRY_PULL_PASSWORD` (`deploy`) — see
chapter 6.

## The web UI, on port 7443

zot ships its own web UI:
<https://registry.playcluster.plone.org:7443/>

It is not a second container. The `ghcr.io/project-zot/zot` image already has
the extensions compiled in — its startup log reports a `binary-type` ending in
`…-search-sync-ui-userprefs` — so the UI is switched on purely by `registry.ui`
in `registry.yml`. Sign in with the registry accounts themselves, `ci` or
`deploy`. There is no separate UI login, and no Traefik basic auth in front of
it, which would only mean a second password prompt.

**Why a separate port.** zot serves the UI and the registry API from one
listener, so enabling the UI would also put it on port 443, at `/`. To keep 443
an API-only endpoint, its router is narrowed to `PathPrefix(/v2/)` — the whole
OCI distribution API, and all a `docker` client ever uses — and the UI gets its
own entrypoint. Setting `registry.ui.enabled: false` removes that entrypoint and
restores the unrestricted rule on 443.

Anonymous visitors to 7443 get the static page and `/v2/_zot/ext/mgmt`, which the
UI reads to find out how to log in. That endpoint returns the zot version and
`{"htpasswd":{}}`, no user names. Every data path — search, `/v2/_catalog`,
manifests — returns 401 without credentials. The one trade-off is that the exact
zot version can be read publicly on that port.

**CVE scanning is off.** It is the expensive half of the UI: zot downloads
Trivy's vulnerability databases into `_trivy/` under its storage directory and
rescans on a timer, on a host that also runs the CI builds. Set
`registry.ui.cve_scanning: true` to turn it on, and keep an eye on memory.

## The Traefik dashboard, on port 8443

The Traefik in front of the registry shows its own dashboard:
<https://registry.playcluster.plone.org:8443/dashboard/> — the trailing slash
matters.

Log in as `admin`, with the same password as the cluster's Traefik dashboard:
both read `vault.traefik.ui_basic_auth`. Here that credential is mounted into
the container as a file rather than set in a label, for two reasons. The
password hash contains `$` characters, which Docker Compose would try to
interpolate. And container labels are readable by anything that can reach the
Docker socket — on `play4` that includes every CI job.

It answers on the registry's own host name, so it reuses that Let's Encrypt
certificate instead of requesting a second one.

```{warning}
This is an administration interface on the public internet, on a host without a
firewall. Switch it off when you do not need it: set
`traefik_dashboard.enabled: false` in `registry.yml` and redeploy the registry.
The entrypoint, the published port, the mounted file and the labels all go
together.
```

## Retention: check before it deletes

zot prunes old images on a schedule, so that the `*/cache` repositories do not
grow without bound: with `mode=max`, BuildKit's layer cache turns over on every
build. The policies are under `registry.retention` in `registry.yml`:

- `**/cache`: keep only the most recently pushed tag;
- `**`: keep `latest` and version tags such as `1.2` or `v1.2.3`, plus the
  twenty most recently pushed tags of the last ninety days — in practice the
  `sha-…` tags CI pushes for every build.

Untagged images, and anything that only referred to deleted images, go too.

The second pattern, `**`, matches the cache repositories as well. Which of the
two policies zot applies to them is the thing to confirm in the dry-run logs
before you switch deletion on.

It ships with **`dryRun: true`**: zot only logs what it *would* delete. After a
few pipelines have run, read those log lines and check that each policy matches
the repositories you expect — overlapping patterns are the part to look at
yourself:

```shell
ssh root@play4.playcluster.plone.org 'cd /srv/registry && docker compose logs registry | grep -i retention'
```

When you are satisfied, set `registry.retention.dryRun: false` and redeploy the
registry.
