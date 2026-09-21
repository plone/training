---
myst:
  html_meta:
    "description": "Provision a Docker Swarm manager, two workers and a CI and registry host with Ansible, one server at a time"
    "property=og:description": "Provision a Docker Swarm manager, two workers and a CI and registry host with Ansible, one server at a time"
    "property=og:title": "Provisioning the cluster"
    "keywords": "Plone, deployment, Ansible, Docker Swarm, Traefik, Portainer, zot, GitLab Runner"
---

(cluster-provisioning-label)=

# Provisioning the cluster

In {ref}`cluster-vms-label` we prepared four clean VMs and a vault.
In this chapter, Ansible turns them into a working cluster:

- `play1` becomes the Docker Swarm manager, running Traefik, Portainer and a cron scheduler.
- `play2` and `play3` join the swarm as workers.
- `play4` gets the GitLab Runner and the zot container registry, outside the swarm.

Ansible can provision all of this in a single run.
The first time, do it **one server at a time**, and look at each one before you move on.
If you have not used Ansible before, this is how you learn what it actually does.
And if something breaks, you know which server and which step caused it.

All commands run from the root of the `training-deployment-playcluster` checkout.

## Before the first run

Check once more that Ansible reaches all four hosts:

```shell
uv run ansible-playbook playbooks/_connect.yml
```

All four should report Ubuntu 26.04, with no unreachable hosts.

## Reading the output

In the reference: {ref}`playcluster-ref-ansible`, which also explains `--limit` by host and by group.

Each run ends with a `PLAY RECAP` line per host:

```console
play1.playcluster.plone.org : ok=76   changed=46   unreachable=0    failed=0    skipped=24
```

`failed=0` and `unreachable=0`
: The only numbers that must be zero.

`changed`
: How many tasks modified the server.
  On a first run that is a lot.
  Run the same playbook again and it should drop to nearly zero, because every task only changes what is not already in the desired state.

`skipped`
: Tasks that did not apply to this host, such as the swarm manager steps on a worker.
  Skipping is normal.

A task that fails prints `fatal:` and stops the run for that host.
Scroll up to the first `fatal:` line, not the last one.

## Order matters: the manager first

The workers cannot join a swarm that does not exist yet.
When a worker is provisioned, Ansible logs in to `play1` to fetch the swarm's join token.
If `play1` is not a manager yet, there is no token, and the worker run fails.

So the order is fixed: `play1`, then `play2` and `play3`, then `play4`.
`play4` is not in the swarm and could go at any point, but it is easiest to reason about last.

## Step 1: the manager, `play1`

In the reference: {ref}`playcluster-ref-manager`.

```shell
uv run ansible-playbook playbooks/setup.yml --limit play1.playcluster.plone.org
```

`--limit` restricts the run to one host out of the inventory.
It also accepts a group from the inventory: `play1` is the only member of `cluster_manager`, so `--limit cluster_manager` does exactly the same.
We name the host the first time, so it is obvious which machine we are working on; the group names are the everyday form.
The playbook works through these stages, and you can follow them in the task names:

1. Base system: proxy settings, packages, a swap file, host name and time zone.
2. The `plone` user, with passwordless `sudo`.
3. SSH: `authorized_keys` for `plone`, and the allow-list in `sshd_config`.
   The task named *Refuse to lock out the account Ansible connects as* runs before anything changes.
4. Docker, from Docker's own package repository, with `plone` in the `docker` group.
5. The swarm: initialise it, label the node, create the shared overlay network `nw-public`, and install cron jobs that purge unused Docker resources.
6. The first stacks: Traefik, the cron scheduler, and Portainer.

It takes about five minutes, most of it installing packages.

### Check the manager

```shell
ssh root@play1.playcluster.plone.org docker node ls
```

One node, `play1`, with `MANAGER STATUS` `Leader`.

```shell
ssh root@play1.playcluster.plone.org docker service ls
```

Five services, all `1/1`: Traefik and its Docker socket proxy, the cron scheduler, and the Portainer server and agent.

Traefik requests its certificates from Let's Encrypt as soon as it starts.
Check that they are real certificates, not Traefik's self-signed default:

```shell
curl -sI https://traefik.playcluster.plone.org/ | head -1
```

`HTTP/2 401` is correct: the Traefik dashboard is protected by basic authentication, and the TLS connection worked.
A certificate error here means DNS or port 443 is not in order, see {ref}`cluster-vms-label`.

### Claim Portainer, within five minutes

Portainer is now reachable at <https://portainer.playcluster.plone.org>, and has no administrator yet.
It does not let the first visitor create one.
At startup, it writes a one-time **setup token** to its log, and the administrator can only be created with that token.
So only someone with access to the manager can claim it.

The token is only valid for about five minutes after Portainer starts.
After that, Portainer locks itself, and the log says *"the Portainer instance timed out for security purposes"*.
Restart it to get a fresh token and a fresh five minutes:

```shell
ssh root@play1.playcluster.plone.org docker service update --force portainer_portainer
```

Read the token from the log.
The log lines contain terminal colour codes, which the `sed` removes:

```shell
ssh root@play1.playcluster.plone.org "docker service logs --raw portainer_portainer 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -o 'setup_token=[^ ]*' | tail -1"
```

Then open <https://portainer.playcluster.plone.org> straight away, enter the token, and create the administrator account.

## Step 2: the workers, `play2` and `play3`

In the reference: {ref}`playcluster-ref-workers`.

The swarm runs over the hosts' public IP addresses.
If your provider has a firewall in front of the VMs, the nodes must be able to reach each other on these ports:

| Port | Protocol | Used for |
| --- | --- | --- |
| 2377 | TCP | Joining the swarm, and managing it |
| 7946 | TCP and UDP | Communication between nodes |
| 4789 | UDP | Overlay network traffic between containers |

A worker that cannot reach 2377 on the manager hangs at *Add Worker to cluster* until it times out.

Provision the workers one after the other.
Both are in the inventory group `cluster_workers`, so `--limit cluster_workers` would do them in a single run, in parallel, with their output interleaved.
For a first look, one at a time is easier to follow:

```shell
uv run ansible-playbook playbooks/setup.yml --limit play2.playcluster.plone.org
```

```shell
uv run ansible-playbook playbooks/setup.yml --limit play3.playcluster.plone.org
```

The first half of the run is identical to `play1`.
Then watch the swarm tasks: several show `-> play1.playcluster.plone.org`.
That is Ansible *delegating* the task to the manager, to fetch the join token and to set the node's labels, while the run is limited to the worker.
The steps that only belong on a manager, such as initialising the swarm and deploying the stacks, are skipped.

### Check the workers

```shell
ssh root@play1.playcluster.plone.org docker node ls
```

Three nodes, all `Ready` and `Active`, with `play1` as `Leader`.

Each node carries the labels from `inventory/hosts.yml`.
Stacks use them to decide where a service may run:

```shell
ssh root@play1.playcluster.plone.org 'docker node inspect play3 --format "{{json .Spec.Labels}}"'
```

`play3` also has `"storage":"persistent"`.
Nothing requires it yet, but it is how a stack keeps a service that stores data, such as a database, on one known node.
The service gets a placement constraint `node.labels.storage == persistent`, and the swarm never schedules it anywhere else.

Portainer's agent is a *global* service: Docker Swarm runs one copy on every node, including nodes that join later.
You did not deploy anything to the workers, and still:

```shell
ssh root@play1.playcluster.plone.org docker service ps portainer_agent
```

shows an agent running on all three.

## Step 3: CI and the registry, `play4`

In the reference: {ref}`playcluster-ref-ci-runner`.

`play4` uses a different playbook, because it is not part of the swarm:

```shell
uv run ansible-playbook playbooks/setup_ci.yml --limit play4.playcluster.plone.org
```

This run takes longer than the others, because installing and registering the GitLab Runner adds several minutes.

The base system, the `plone` user, SSH and Docker are set up exactly as on the other hosts.
Then two things are specific to this host.

**The GitLab Runner.**
Ansible installs it, registers it with GitLab using the runner token from the vault, and writes its configuration to `/etc/gitlab-runner/config.toml`.
Several tasks show `(censored due to no_log)` instead of their details.
That is deliberate: those tasks handle the token, and the role keeps it out of the output.

**The registry.**
zot, behind its own Traefik, deployed with Docker Compose into `/srv/registry`.
Ansible writes zot's configuration, generates the password file for the `ci` and `deploy` accounts from the vault, and starts both containers.

### Check the runner

In GitLab, the runner should now be listed as online, under {menuselection}`Build --> Runners` of your group.
On the host:

```shell
ssh root@play4.playcluster.plone.org systemctl is-active gitlab-runner
```

```{warning}
`gitlab-runner list` on the host prints the runner's authentication token in full.
Do not run it while sharing your screen, and do not paste its output anywhere.
Anyone with that token can pose as your runner and receive your CI jobs, including their CI/CD variables.
```

### Check the registry

From your own machine:

```shell
curl -sI https://registry.playcluster.plone.org/v2/ | head -1
```

`HTTP/2 401`: TLS works and anonymous access is refused.
The registry has three entrances on the same host name:

`https://registry.playcluster.plone.org/v2/`
: The registry API that `docker` uses, on port 443.

`https://registry.playcluster.plone.org:7443/`
: zot's web UI.
  Sign in with the `ci` or `deploy` account.

`https://registry.playcluster.plone.org:8443/dashboard/`
: The dashboard of the Traefik in front of the registry.
  Same credentials as the cluster's Traefik dashboard.

The two registry accounts have different rights, and this is worth proving once.
On a machine with Docker, log in as `ci` and push a throwaway image:

```shell
docker login registry.playcluster.plone.org -u ci
```

```shell
docker pull alpine:3 && docker tag alpine:3 registry.playcluster.plone.org/probe/alpine:test && docker push registry.playcluster.plone.org/probe/alpine:test
```

Now log in as `deploy` instead.
Pulling works, pushing must fail with *requested access to the resource is denied*:

```shell
docker login registry.playcluster.plone.org -u deploy
```

```shell
docker pull registry.playcluster.plone.org/probe/alpine:test && docker push registry.playcluster.plone.org/probe/alpine:test
```

The swarm will pull with `deploy`, and it stores those credentials on every node.
That is why the account the swarm uses must not be able to push.

## When something goes wrong

| Symptom | Likely cause |
| --- | --- |
| A worker hangs at *Add Worker to cluster* | A firewall blocks port 2377, or the other swarm ports, between the nodes. |
| A worker fails at *Swarm Info* | `play1` was not provisioned first, so there is no swarm to join. |
| A site shows a certificate for *TRAEFIK DEFAULT CERT* | Let's Encrypt could not issue a certificate: the DNS name is missing or wrong, or port 443 is not reachable from the internet. |
| A site answers `404` from Traefik | No router matches the host name you used. Check for a typo, and use the exact name from the inventory. |
| Portainer says it *timed out for security purposes* | The five minutes to claim it have passed. Restart the service and read the new token. |
| *Refuse to lock out the account Ansible connects as* fails | `inventory/group_vars/all/sshd.yml` would shut out the user Ansible connects as. Nothing was changed; fix the file and run again. |

## Where to find what

The cluster now has five web addresses, on two hosts:

| Address | What | Login |
| --- | --- | --- |
| <https://traefik.playcluster.plone.org/> | The cluster's Traefik dashboard, on `play1` | `admin`, and the Traefik password |
| <https://portainer.playcluster.plone.org/> | Portainer, a web UI for the swarm, on `play1` | the administrator you created with the setup token |
| `https://registry.playcluster.plone.org/v2/` | The registry API, on `play4`: what `docker` talks to | `ci` or `deploy` |
| <https://registry.playcluster.plone.org:7443/> | The registry's web UI | `ci` or `deploy` |
| <https://registry.playcluster.plone.org:8443/dashboard/> | The dashboard of `play4`'s own Traefik; the trailing slash matters | `admin`, the same password as the cluster's Traefik |

`https://registry.playcluster.plone.org/` on its own gives a 404, and that is correct.
zot serves its API and its web UI from one listener, so port 443 is kept for the API alone and the UI has its own port.

## Next

The cluster is ready.
{ref}`gitlab-runner-config-label` finishes the GitLab side: the CI/CD variables a pipeline needs to push images to the registry and deploy them to the swarm.
