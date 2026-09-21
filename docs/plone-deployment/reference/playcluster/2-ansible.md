---
myst:
  html_meta:
    "description": "Ansible for people who have not used it: inventory, playbooks, tasks and variables."
    "property=og:title": "2. Ansible in one sitting"
    "keywords": "Ansible, inventory, playbook, group_vars, Plone"
---

(playcluster-ref-ansible)=

# 2. Ansible in one sitting

% Exported from training-deployment-playcluster b880f28 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

Ansible has two halves, and almost everything makes sense once you see which
half you are looking at.

```
       WHAT EXISTS                          WHAT TO DO TO IT
  ┌─────────────────────┐              ┌─────────────────────────┐
  │  inventory/         │              │  playbooks/             │
  │   hosts.yml         │  ─────────>  │   setup.yml             │
  │   group_vars/       │   applied    │   setup_ci.yml          │
  │                     │     to       │   deploy.yml            │
  │  hosts, groups,     │              │        │                │
  │  and their settings │              │        v                │
  └─────────────────────┘              │  tasks/  the actual     │
                                       │          steps          │
                                       └─────────────────────────┘
```

The left side is description: which servers exist, how they are grouped, what
settings apply to them. The right side is action: ordered steps to bring a
server into that state. Neither knows anything until you run one against the
other.

## The inventory: which servers, in which groups

`inventory/hosts.yml` lists the machines and sorts them into groups. Trimmed:

```yaml
cluster:
  hosts:
    play1.playcluster.plone.org:
      ansible_user: root
      swarm_node:
        labels:
          type: manager
    play2.playcluster.plone.org:
      swarm_node:
        labels:
          type: worker
    play3.playcluster.plone.org:
      swarm_node:
        labels:
          type: worker
          storage: persistent
  children:
    cluster_managers:
      children:
        cluster_manager:
          hosts:
            play1.playcluster.plone.org:
    cluster_workers:
      hosts:
        play2.playcluster.plone.org:
        play3.playcluster.plone.org:

standalone:
  hosts:
    play4.playcluster.plone.org:
```

Groups are just names you can aim a playbook at. `cluster`, `cluster_manager`,
`cluster_workers` and `standalone` are the four the playbooks are aimed at. A host can
be in several at once — `play1` is in both `cluster` and `cluster_manager`.

Note `swarm_node.labels`. Those become Docker Swarm node labels, and later a
stack can say "put the database only on a node labelled `storage: persistent`".
That is how `play3` ends up holding the data.

## Variables: settings that travel with a group

`inventory/group_vars/` holds settings, split by which group they apply to:

```
group_vars/all/          applies to every host
  base.yml  users.yml  sshd.yml  docker.yml  swarm.yml
  packages.yml  disks.yml  swap.yml  ufw.yml  proxy.yml
  stacks.yml  vault.yml

group_vars/standalone/   applies only to play4
  runners.yml  registry.yml  docker.yml  compose.yml
```

This is where you change things. Almost nothing in these chapters involves editing a
playbook — you edit a variable and re-run.

```{note}
`group_vars/all/vault.yml` is encrypted. Ansible decrypts it on the fly using
the vault password you were given. Never commit the password file itself;
`.vault_pass` is already in `.gitignore`.
```

## Playbooks and tasks

A **playbook** says which hosts to target and which task files to run, in order.
`playbooks/setup.yml` is the one you will use next:

```yaml
- name: "Bootstrap a server"
  hosts: "all"
  become: true
  tasks:
    - name: "Hostname"
      tags: [base, hostname]
      ansible.builtin.import_tasks: ../tasks/base/task_hostname.yml
    - name: "Docker: Setup"
      tags: [base, docker]
      ansible.builtin.import_tasks: ../tasks/docker/task_setup.yml
```

The real steps live in `tasks/`, grouped by area: `tasks/base/`, `tasks/docker/`,
`tasks/stacks/`, `tasks/compose/`.

Two things to notice, because you will use both:

**`hosts: "all"`** — the playbook itself targets everything. You narrow it at
the command line with `--limit`. That is what lets one playbook provision the
manager first and the workers afterwards.

`--limit` takes a host name or a group name from the inventory:

```shell
uv run ansible-playbook playbooks/setup.yml --limit play2.playcluster.plone.org
```

```shell
uv run ansible-playbook playbooks/setup.yml --limit cluster_workers
```

The first provisions `play2` only; the second provisions `play2` and `play3`
together, in parallel. These chapters provision **one host at a time** the
first time round, so each run's output belongs to a single server and you can
see exactly what happened where. Once you know the playbooks, the groups are
the everyday form — the inventory's groups exist precisely so you do not have to
list hosts one by one.

**`tags:`** — each task carries labels, so you can re-run one part instead of
everything. `--tags docker` runs only the Docker steps.

## Idempotence, and why re-running is safe

Ansible tasks describe a desired end state, not commands. "This package is
installed", not "run apt-get install". Running a playbook twice does not do the
work twice — the second run reports `ok` for everything already correct and
changes nothing.

You will lean on this. When something fails half-way, you fix it and re-run the
whole playbook.

Every run ends with a `PLAY RECAP`, one line per host:

```console
play1.playcluster.plone.org : ok=76   changed=46   unreachable=0    failed=0    skipped=24
```

Read it in these terms:

- `ok` — already as desired, nothing done
- `changed` — Ansible altered something. High on a first run; a second run of
  the same playbook should bring it close to zero.
- `skipped` — the task did not apply to this host, such as the manager-only
  steps on a worker. Normal.
- `unreachable` — Ansible could not connect at all: an SSH problem, see chapter 1
- `failed` — stopped; that host is skipped for the rest of the run

`failed` and `unreachable` are the two that must be zero. When a task fails it
prints `fatal:`; scroll up to the *first* `fatal:` line, not the last one.

## Set up your checkout

Everything from here runs on your own machine. There is no control server: you
work in a local checkout, and Ansible reaches the cluster over SSH.

```shell
git clone git@github.com:plone/training-deployment-playcluster.git
cd training-deployment-playcluster
```

Dependencies are managed with `uv`, so there is nothing to install globally:

```shell
uv sync
```

```shell
uv run ansible-galaxy install -r requirements.yml
```

The second command fetches third-party roles this repo depends on, such as
`geerlingguy.swap` and the GitLab runner role. `make install` runs both.

Put the vault password where `ansible.cfg` expects it — a file called
`.vault_pass` in the root of the checkout, readable only by you:

```shell
chmod 600 .vault_pass
```

The file has to have exactly that name. `ansible.cfg` points there, and
`.gitignore` keeps it out of git.

### Setting up your own vault

In a workshop or training the password may be handed out. Setting up your own cluster, you need
your own vault: the `vault.yml` in this repository is encrypted with the
maintainer's password, and is of no use to anyone else.

Create a password first:

```shell
openssl rand -hex 32 > .vault_pass
```

The vault holds these secrets:

| Key | Used for | How to generate |
| --- | --- | --- |
| `traefik.ui_basic_auth` | Login for both Traefik dashboards | `htpasswd -nbB admin '<password>'` |
| `registry.accounts.ci` | Registry account CI pushes with | `openssl rand -hex 24` |
| `registry.accounts.deploy` | Read-only registry account the swarm pulls with | `openssl rand -hex 24` |
| `gitlab.runner_tokens.play4` | Registers the runner on `play4` | From GitLab, see chapter 5 |
| `proxy_credentials` | Only if your hosts need an HTTP proxy | leave empty |

The vault stores only a *hash* of the Traefik password, so keep the password
itself in a password manager — the vault cannot give it back.

The repository has a template with placeholders for all of them. Copy it, fill
in the copy, encrypt it into place, and delete the copy:

```shell
cp etc/vault.template.yml vault.plain.yml
```

```shell
uv run ansible-vault encrypt --output inventory/group_vars/all/vault.yml vault.plain.yml
```

```shell
rm vault.plain.yml
```

Fill in the *copy*, never the template: the template is tracked by git, and a
filled-in template is one `git add` away from publishing your secrets in plain
text. `vault.plain.yml` is in `.gitignore` for the same reason.

Check that the new vault opens:

```shell
uv run ansible-vault view inventory/group_vars/all/vault.yml
```

Later changes, such as adding the runner token, go through `edit`, which
decrypts into your editor and encrypts again when you save:

```shell
uv run ansible-vault edit inventory/group_vars/all/vault.yml
```

```{warning}
Do not add `--vault-password-file .vault_pass` to these commands. `ansible.cfg`
already supplies it, and naming it a second time fails with *"The vault-ids
default,default are available to encrypt"*.
```

### Using your own domain

This repository describes `playcluster.plone.org`. To build the cluster under
another domain, change the host names in these files, and nowhere else:

`inventory/hosts.yml`
: The four hosts.

`inventory/group_vars/all/stacks.yml`
: `TRAEFIK_UI_HOSTNAME` and `PORTAINER_HOSTNAME`.

`inventory/group_vars/standalone/registry.yml`
: `registry.hostname`.

`inventory/group_vars/standalone/runners.yml`
: The runner's `name`, and `gitlab_runner_coordinator_url` if you use your own
  GitLab.

`inventory/group_vars/all/base.yml`
: `devops.email`, the address your Let's Encrypt account is registered with.

Then search for the old domain to catch anything left over:

```shell
git grep -n "playcluster.plone.org"
```

Now confirm Ansible can reach every host — this is the same check as chapter 1,
but through Ansible's own connection handling:

```shell
uv run ansible -i inventory/hosts.yml all -m ping
```

Every host should answer `"ping": "pong"`. If one does not, fix that before
running a playbook; a connection problem half-way through a provisioning run is
tedious to unpick.

`playbooks/_connect.yml` does the same check through a playbook, and also prints
each host's Ubuntu release and IP addresses — a quick way to confirm all four
are on the release you expect:

```shell
uv run ansible-playbook playbooks/_connect.yml
```

```{tip}
`ansible` (singular) runs one module against hosts — useful for checks.
`ansible-playbook` runs a playbook. You will use the second for everything else.
```
