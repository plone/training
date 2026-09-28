---
myst:
  html_meta:
    "description": "Provision the swarm manager with setup.yml and --limit."
    "property=og:title": "3. Provision the manager"
    "keywords": "Ansible, Docker Swarm, manager, Traefik, Portainer"
---

(playcluster-ref-manager)=

# 3. Provision the manager

% Exported from training-deployment-playcluster b880f28 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

The manager goes first, and alone. It initialises the swarm and produces the
join token the workers need, so there is nothing for a worker to join until this
finishes.

## Look before you run

```shell
uv run ansible-playbook playbooks/setup.yml --limit play1.playcluster.plone.org --check --diff
```

`--check` makes a dry run: Ansible reports what it *would* change without
changing anything. `--diff` shows the actual file differences. Read it — this is
the cheapest moment to notice a wrong hostname or an unexpected package.

```{note}
`--check` is not perfect. A task that depends on an earlier task's result may
report oddly, because that earlier change never happened. Treat unexpected
`skipped` entries in a check run as noise rather than a problem.

On a brand-new host a check run cannot get far: installing Docker depends on a
package repository that only the real run adds, and everything after that needs
Docker. A dry run is most useful on a host that has been provisioned before.
```

## Run it

```shell
uv run ansible-playbook playbooks/setup.yml --limit play1.playcluster.plone.org
```

`--limit` is what confines this to `play1`. Without it, `setup.yml` targets
`all` — every host in the inventory, including the runner.

`play1` is the only member of the inventory group `cluster_manager`, so
`--limit cluster_manager` does exactly the same. The rest of this chapter uses
the group name for re-runs; the first time, naming the host makes it obvious
which machine you are working on.

About five minutes. In order, it:

1. Configures the proxy and installs base packages
2. Sets hostname and timezone
3. Configures swap and mounts data disks
4. Creates the `plone` user and applies its keys
5. Applies the SSH configuration from `sshd.yml`
6. Installs Docker
7. Initialises the swarm and applies the node labels from `hosts.yml`
8. Deploys the initial stacks — Traefik, the cronjob stack and Portainer

Watch the recap at the end: `failed=0` and `unreachable=0`.

## What just happened to the swarm

```shell
ssh root@play1.playcluster.plone.org docker node ls
```

One node, `Leader`. The workers are not there yet.

```shell
ssh root@play1.playcluster.plone.org docker stack ls
```

`traefik`, `cronjob` and `portainer`, deployed as part of the run. Traefik is the
cluster's single ingress: it holds ports 80 and 443, and every application stack
you deploy later routes through it.

Traefik asks Let's Encrypt for its certificates as soon as it starts. Check you
got a real one, not Traefik's self-signed default:

```shell
curl -sI https://traefik.playcluster.plone.org/ | head -1
```

`HTTP/2 401` is right: TLS worked, and the dashboard wants its password. A
certificate error means the DNS name or port 443 is not in order — see "Before
you start" in the overview.

```{important}
Only one service in the whole swarm can publish port 80 and 443. Traefik is that
service. An application stack that ships its own Traefik will fail to deploy
with `port '80' is already in use`. Applications attach to Traefik with labels
instead — that is the subject of the deployment project.
```

## Where Traefik's settings live

`etc/stacks/traefik.yml`, deployed by `tasks/stacks/`. Two parts are worth
knowing now, because everything you deploy later has to match them.

Discovery — which services Traefik will even look at:

```yaml
- --providers.swarm.constraints=Label(`traefik.constraint-label`, `public`)
- --providers.swarm.network=nw-public
```

A service without `traefik.constraint-label=public`, or not attached to
`nw-public`, is invisible to Traefik. No error, no router — just nothing.

Entrypoints and certificates:

```yaml
- --entrypoints.http.address=:80
- --entrypoints.http.http.redirections.entrypoint.to=https
- --entrypoints.https.address=:443
- --certificatesresolvers.le.acme.tlschallenge=true
```

The redirection lines send all plain HTTP to HTTPS for every stack on the
cluster, so no application needs its own redirect. `le` is the name of the
Let's Encrypt resolver that application routers ask for TLS certificates from.

Traefik's own dashboard is behind basic auth at
<https://traefik.playcluster.plone.org>.

## Portainer

The third stack is a web UI for the swarm — services, tasks, logs and volumes,
without an SSH session:

<https://portainer.playcluster.plone.org>

It is worth knowing how it is put together, because it is not the obvious
arrangement. Portainer runs as two services:

- an **agent**, in `global` mode, so one copy lands on every node in the swarm.
  The agent is the part that holds `/var/run/docker.sock`.
- the **server**, a single replica, which asks the agents for everything over
  `tasks.agent:9001`.

So the server itself needs no Docker socket. That matters: it is the service
exposed to the internet, and a socket mount would hand it root-equivalent
control of the host. The same reasoning put a `socket-proxy` in front of Traefik
rather than mounting the socket there.

### Claiming Portainer

A new Portainer has no administrator, and it does not let the first visitor
create one. At startup it writes a one-time **setup token** to its log, and the
administrator account can only be created with that token — so only someone who
can read the logs on the manager can claim it.

The token is valid for about five minutes after the service starts. After that
Portainer locks itself, and the log says *"the Portainer instance timed out for
security purposes"*. A restart gives a new token and a new five minutes:

```shell
ssh root@play1.playcluster.plone.org docker service update --force portainer_portainer
```

Read the token. The log lines carry terminal colour codes, which the `sed`
strips:

```shell
ssh root@play1.playcluster.plone.org "docker service logs --raw portainer_portainer 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -o 'setup_token=[^ ]*' | tail -1"
```

Then open <https://portainer.playcluster.plone.org> straight away, give it the
token, and create the administrator account.

Its data lives in a `portainer_data` local volume, which is why the server is
constrained to the manager — the volume exists on that node and nowhere else.

## Re-running one part

If you change something later, you do not need the whole playbook:

```shell
uv run ansible-playbook playbooks/setup.yml --limit cluster_manager --tags docker
```

Available tags include `base`, `hostname`, `timezone`, `disks`, `user`, `ssh`,
`docker`, `swarm` and `stacks`.

## Redeploying only the stacks

`--tags stacks` is the one you will reach for most. It skips every system task
and re-runs just the stack deployments — Traefik, cronjob and Portainer:

```shell
uv run ansible-playbook playbooks/setup.yml --limit cluster_manager --tags stacks
```

Use it after editing anything under `etc/stacks/` or the `stacks` dictionary in
`inventory/group_vars/all/stacks.yml`. It takes seconds rather than the
minutes of a full run, and it touches nothing else on the host.

For a single stack there is a second playbook, with one tag per stack:

```shell
uv run ansible-playbook playbooks/deploy.yml --limit cluster_manager --tags portainer
```

Both end up in the same place — `tasks/stacks/task_deploy.yml` templates the
stack file to `/srv/<stack>/` on the manager and runs `docker stack deploy`.
`setup.yml --tags stacks` is for bringing a host up to date; `deploy.yml` is for
working on one stack.

```{note}
Stack files are Ansible templates, and the `env_vars` block for each stack in
`stacks.yml` supplies the `${VARIABLES}` inside them. A variable used in a stack
file but missing from `env_vars` does not fail the deploy — it interpolates to
an empty string, and you get a service with an empty setting instead of an
error.
```

## If it fails

Read the failed task's name — it tells you which file in `tasks/` to look at.
Fix the cause, then re-run the same command in full. Ansible skips everything
already correct, so a re-run after a fix is usually quick.

If it failed at the swarm step, check that nothing is half-initialised:

```shell
ssh root@play1.playcluster.plone.org docker info | grep -i swarm
```
