---
myst:
  html_meta:
    "description": "Provision the swarm workers and verify the cluster."
    "property=og:title": "4. Provision the workers"
    "keywords": "Ansible, Docker Swarm, worker, node labels"
---

(playcluster-ref-workers)=

# 4. Provision the workers

% Exported from training-deployment-playcluster b880f28 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

Same playbook, different `--limit`. The workers join the swarm the manager
created in chapter 3.

## The swarm's ports

The swarm runs over the hosts' public addresses. If your provider puts a
firewall in front of the servers, the nodes must be able to reach each other on
these ports:

| Port | Protocol | Used for |
| --- | --- | --- |
| 2377 | TCP | Joining the swarm, and managing it |
| 7946 | TCP and UDP | Communication between nodes |
| 4789 | UDP | Overlay network traffic between containers |

A worker that cannot reach 2377 on the manager hangs at *Add Worker to cluster*
until it times out.

## Run it

One worker at a time, the first time round:

```shell
uv run ansible-playbook playbooks/setup.yml --limit play2.playcluster.plone.org
```

```shell
uv run ansible-playbook playbooks/setup.yml --limit play3.playcluster.plone.org
```

Both workers are in the inventory group `cluster_workers`, so once you know what
to expect, one run covers them:

```shell
uv run ansible-playbook playbooks/setup.yml --limit cluster_workers
```

Ansible then works on both in parallel and the output interleaves, each line
prefixed with its host. That is fine for a routine re-run, and noisy for a first
look.

The steps are the same as the manager's, with one difference at the end: instead
of initialising a swarm, they join the manager's. Watch the swarm tasks — several
show `-> play1.playcluster.plone.org`. That is Ansible *delegating* the task to
the manager, to fetch the join token and to set this node's labels there, while
the run itself is limited to the worker. The manager-only steps, initialising the
swarm and deploying stacks, show as `skipped`.

```{warning}
The manager has to be provisioned first. A worker run fetches its join token
from `play1`; if `play1` is not a swarm manager yet, there is no token, and the
run fails at *Docker Swarm: Swarm Info*.
```

## Verify the cluster

```shell
ssh root@play1.playcluster.plone.org docker node ls
```

Three nodes, all `Ready` / `Active`, with `play1` marked `Leader`.

Now the labels, which matter more than they look:

```shell
ssh root@play1.playcluster.plone.org \
  'docker node inspect play3 --format "{{json .Spec.Labels}}"'
```

You should see `storage: persistent` and `type: worker`. Those came from
`swarm_node.labels` in `inventory/hosts.yml` — inventory data turned into
cluster state.

Portainer's agent is a `global` service: the swarm runs one copy on every node,
including nodes that join later. You deployed nothing to the workers, and still:

```shell
ssh root@play1.playcluster.plone.org docker service ps portainer_agent
```

shows an agent running on all three.

## Why the labels matter

Swarm decides which node runs a task. Usually you do not care. Two cases where
you must:

**Data on disk.** A stack that bind-mounts a host directory is tied to the node
holding that directory. If Swarm reschedules it elsewhere, the mount points at a
different — empty — directory, and a database comes up blank. A placement
constraint prevents this:

```yaml
deploy:
  placement:
    constraints:
      - node.labels.storage == persistent
```

**Keeping workloads off the manager.** Application services are constrained to
`node.labels.type == worker`, leaving the manager to run Traefik and manage the
cluster.

```{warning}
A constraint no node satisfies does not error. The task simply stays pending
forever with "no suitable node". If a service never starts, check its constraint
against the actual node labels first.
```

## Check Traefik sees the cluster

Traefik runs on the manager but routes to services anywhere in the swarm, over
the `nw-public` overlay network:

```shell
ssh root@play1.playcluster.plone.org docker network ls | grep nw-public
```

`nw-public` should be `overlay` and `swarm`-scoped. Application stacks attach to
it as an **external** network — they use it, they do not create it.

## A quick end-to-end test

Optional, but it proves routing works before any real application depends on it.
On the manager:

```shell
docker service create --name hello \
  --network nw-public \
  --label traefik.enable=true \
  --label traefik.constraint-label=public \
  --label traefik.swarm.network=nw-public \
  --label 'traefik.http.routers.hello.rule=Host(`hello.play1.playcluster.plone.org`)' \
  --label traefik.http.routers.hello.entrypoints=https \
  --label traefik.http.routers.hello.tls=true \
  --label traefik.http.services.hello.loadbalancer.server.port=80 \
  traefik/whoami
```

Then remove it again:

```shell
docker service rm hello
```

```{note}
Set `traefik.swarm.network`, never `traefik.docker.network` as well. Defining
both makes Traefik skip the service entirely, logging
`both Docker and Swarm labels are defined` — the service simply never appears,
with no router and no obvious cause.
```

If the router does not show up, check the manager's Traefik logs:

```shell
docker service logs traefik_traefik --tail 50
```
