---
myst:
  html_meta:
    "description": "Build the playcluster from scratch: SSH, Ansible, Docker Swarm and the CI runner."
    "property=og:description": "Build the playcluster from scratch: SSH, Ansible, Docker Swarm and the CI runner."
    "property=og:title": "Building the cluster"
    "keywords": "Plone, playcluster, Ansible, Docker Swarm"
---

(playcluster-ref-overview)=

# Building the cluster

% Exported from training-deployment-playcluster 00fc574 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

From four bare Linux servers to a working Docker Swarm cluster, with a GitLab CI
runner and a container registry attached.

These chapters build the platform only. Deploying a Plone site onto it is the
subject of the deployment project that goes with this cluster.

## What you end up with

| Host | Role |
| --- | --- |
| `play1` | Swarm manager, runs Traefik and Portainer |
| `play2` | Swarm worker |
| `play3` | Swarm worker, holds persistent storage |
| `play4` | GitLab CI runner and container registry, **not** in the swarm |

Ansible runs from **your own machine**, not from a server. There is no fifth
host: you check the repository out locally, and every command in these chapters
is one you type on your laptop. Ansible reaches the four servers over SSH and
needs nothing installed on them beforehand.

That is worth stating because it changes what "where am I?" means throughout.
Unless a section says otherwise, you are on your own machine, in a checkout of
this repository.

## Where to find what

Once the cluster runs, it has five web addresses on two hosts:

| Address | What | Login |
| --- | --- | --- |
| `https://traefik.playcluster.plone.org/` | The cluster's Traefik dashboard, on `play1` | `admin`, password from `vault.traefik.ui_basic_auth` |
| `https://portainer.playcluster.plone.org/` | Portainer, a web UI for the swarm, on `play1` | the administrator created with Portainer's setup token |
| `https://registry.playcluster.plone.org/v2/` | The registry API, on `play4` — what `docker` talks to | `ci` (push) or `deploy` (pull) |
| `https://registry.playcluster.plone.org:7443/` | The registry's web UI | `ci` or `deploy` |
| `https://registry.playcluster.plone.org:8443/dashboard/` | The dashboard of `play4`'s own Traefik — the trailing slash matters | `admin`, the same password as the cluster's Traefik |

The registry answers on three ports because zot serves its API and its web UI
from one listener: port 443 is kept for the API alone, so
`https://registry.playcluster.plone.org/` itself gives a 404. Chapter 7 explains
the arrangement.

## Chapters

| | Chapter |
| --- | --- |
| 1 | [SSH, keys and the two users](1-ssh-and-users.md) |
| 2 | [Ansible in one sitting](2-ansible.md) |
| 3 | [Provision the manager](3-manager.md) |
| 4 | [Provision the workers](4-workers.md) |
| 5 | [The CI runner host](5-ci-runner.md) |
| 6 | [Connecting GitLab](6-gitlab.md) |
| 7 | [The registry in detail](7-registry.md) |

Provisioning a host takes about five minutes; `play4` takes longer, because it
also installs the GitLab Runner. Chapter 3 is where a wrong host name or a
missing key tends to surface first.

## Before you start

You need:

- Four servers running a clean Ubuntu 26.04, all at the same patch level, and
  DNS names that point at them (see below).
- A working `ssh` on your own machine, and an SSH key whose public half is in
  `/root/.ssh/authorized_keys` on `play1` through `play4`.
- A vault password. In a workshop or training it may be handed out. Setting up your
  own cluster, you create your own vault, as described in chapter 2 — the
  `vault.yml` in this repository is encrypted with the maintainer's password.
- Access to <https://github.com/plone/training-deployment-playcluster>.

The DNS names have to resolve *before* the first provisioning run: Traefik asks
Let's Encrypt for certificates as soon as it starts, and that fails for a name
that does not point at the host yet.

| Name | Type | Points to |
| --- | --- | --- |
| `play1.playcluster.plone.org` … `play4.playcluster.plone.org` | A | each server |
| `traefik.playcluster.plone.org`, `portainer.playcluster.plone.org` | CNAME | `play1` |
| `registry.playcluster.plone.org` | CNAME | `play4` |

Port 443 must be reachable from the internet, because Let's Encrypt validates
on it.

Machines created from the "same" image can still differ in patch level, and the
playbooks refresh package lists but never upgrade. Bring all four up to date
once, before you start:

```shell
ssh root@play1.playcluster.plone.org 'apt-get update && apt-get -y full-upgrade && reboot'
```

and the same for `play2` to `play4`.

```{note}
Everything in these chapters runs from your own machine. You will not log in to
the cluster hosts by hand except to look at something — Ansible does the work.
```
