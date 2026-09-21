---
myst:
  html_meta:
    "description": "SSH keys, authorized_keys, and the root and plone users."
    "property=og:title": "1. SSH, keys and the two users"
    "keywords": "SSH, authorized_keys, Ansible, Plone"
---

(playcluster-ref-ssh-and-users)=

# 1. SSH, keys and the two users

% Exported from training-deployment-playcluster 00fc574 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

Ansible is not a daemon. There is no agent on the servers. It opens an SSH
connection, copies a small Python script over, runs it, and reads the result
back. So everything here rests on one thing: can you SSH in as the right user
without being asked for a password?

## How key authentication works

You hold a **private key**. The server holds the matching **public key**. When
you connect, the server sends a challenge; only the private key can answer it.
The private key never leaves your machine.

The server keeps the public keys it will accept in one file per user:

```
~/.ssh/authorized_keys
```

One key per line. If your public key is on a line in that file, you get in as
that user. If it is not, you do not. That is the whole mechanism, and it is why
the file is the thing we care about most.

```{important}
`authorized_keys` belongs to the **user**, not the machine. A key in
`/root/.ssh/authorized_keys` gets you in as `root`. The same key in
`/home/plone/.ssh/authorized_keys` gets you in as `plone`. Two separate
decisions.
```

## Your key

Ansible connects as `root` over SSH. The inventory names no key file, so SSH
picks one the way it always does — from your agent, or from `~/.ssh/`. Whichever
key you end up using, its public half has to be in `/root/.ssh/authorized_keys`
on all four hosts. That is what lets Ansible reach them.

Two ways that happens, and either works:

- **Your own key.** Your public half is added to the four hosts, and you carry
  on using the key you already have.
- **A shared key.** One key pair for a workshop or training, handed out at the start, with
  its public half already installed on the hosts. Point SSH at it explicitly,
  since it will not be your default identity:

  ```
  Host play*.playcluster.plone.org
      User root
      IdentityFile ~/.ssh/playcluster_workshop
  ```

A shared key gets everyone connected quickly, which is why a workshop tends to
use one. It is a workshop measure, not a pattern to copy into production: a key
several people hold cannot be revoked for one person, and nothing in the logs
distinguishes who used it. For lasting access, give people their own accounts.

If your key is a file rather than an agent identity, make sure only you can read
it. SSH refuses to use a key others can read:

```shell
chmod 600 ~/.ssh/id_ed25519
```

Check it works before going any further:

```shell
ssh root@play1.playcluster.plone.org hostname
```

You should get `play1` back and nothing else. No password prompt, no "Permission
denied".

```{tip}
If it asks for a password, the key is not being offered or not accepted. Add
`-v` and look for the `Offering public key` line and what the server says next.
```

Save yourself typing from here on by putting this in
`~/.ssh/config`:

```
Host play*.playcluster.plone.org
    User root
```

Then `ssh play2.playcluster.plone.org` is enough.

```{note}
A host that has been rebuilt comes back with a new host key, and SSH refuses to
connect, warning that the remote host identification has changed. After a
rebuild that is expected. Remove the old entry, then connect again to accept
the new key:

`ssh-keygen -R play1.playcluster.plone.org`
```

## Two users, two jobs

The cluster hosts have two accounts that matter, and the split is deliberate.
A fresh VM has only the first one.

**`root`** is the *setup* user. It is the only account on a freshly provisioned
VM, and it is what Ansible connects as to provision the host: install
packages, write system configuration, set up Docker and the swarm. It is
defined in `inventory/group_vars/all/users.yml`:

```yaml
users:
  setup:
    name: root
    homedir: /root
```

**`plone`** is the *default* user — the deployment account. Once the cluster
exists, nothing needs root any more: the CI pipeline's deploy job logs in over
SSH as `plone` (`DEPLOY_USER`) and runs `docker stack deploy` on the manager.
People who want to look around log in as `plone` too.

```yaml
  default:
    name: plone
    group: sudo
    additional_keys: []
```

`plone` is created *by* the provisioning run in chapter 3; it does not exist on
a fresh host. It is in the `docker` group, so it can run `docker` directly, and
it has passwordless `sudo`.

Keys that can log in as `plone` come from three places, all merged into its
`authorized_keys`:

- **Every key already in root's `authorized_keys`.** Whoever could provision the
  host can also log in as `plone`.
- **Every `etc/keys/*.pub` in this repository.** The first provisioning run
  generates a key pair there, `plone_prod_deploy_ed25519`, for operators. Give
  CI a pair of its own rather than that one — generate it before the first
  provisioning run, so its public half is installed straight away:

  ```shell
  ssh-keygen -t ed25519 -f etc/keys/gitlab_ci_deploy -C "gitlab-ci@playcluster.plone.org" -N ""
  ```

  The private half becomes the `DEPLOY_SSH_PRIVATE_KEY` CI/CD variable in
  chapter 6. Then the pipeline can be cut off by removing one key, without
  touching anyone's access. `etc/keys/` is gitignored, so none of these keys
  reach the repository.
- **`additional_keys` above.** Public keys, one string each, for people — for
  example trainees who should be able to inspect a host. Public keys are not
  secret, so this list can be committed.

```{warning}
Because `etc/keys/` is gitignored, `git status` never shows what is in it. If you
copied this repository from another setup instead of cloning it fresh, the
previous owner's keys may still be there, and the first provisioning run would
give them `plone` — and with it `sudo` — on every host. Look before you run:
`ls -la etc/keys/`, and remove anything you did not create yourself.
```

```{note}
Do not confuse the `plone` SSH account with the container registry's `deploy`
account from chapter 5. `deploy` is a registry login with read-only rights that
the swarm uses to pull images; it is not a user on any of these machines.
```

```{tip}
An account that runs Docker needs `sudo`, or membership of the `docker` group.
Adding someone to `docker` only works on a host where Docker is already
installed, because the group does not exist before that.
```

## The allow-list

Which accounts SSH will accept at all is set in
`inventory/group_vars/all/sshd.yml`:

```yaml
sshd_extra_allow_users: ""

sshd:
  port: 22
  allow_root: "yes"
  allow_users: >-
    {{ ([users.default.name, users.setup.name] + sshd_extra_allow_users.split())
       | unique | join(' ') }}
```

By default `allow_users` comes out as `plone root`.

```{warning}
`allow_users` is an allow-list. An account missing from it cannot log in, even
with a valid key in its `authorized_keys`. If a host has a third account — one
you add for a trainee by hand, or one your hosting provider created — put it in
`sshd_extra_allow_users` *before* running the playbook, or the run will lock it
out.
```

The SSH task guards against the worst case: before it changes anything, it
checks that the account Ansible is connected as would still be allowed in. If
it would not, the run stops with an explanation and `sshd_config` is left
untouched. Every change is also validated with `sshd -t` before it is written,
so a typo cannot leave sshd unable to start.

## Why root stays enabled

`allow_root: "yes"` is a deliberate choice, not an oversight. Ansible needs an
account that can configure the system before any other account exists, and on
a fresh VM that is root.

This playbook also leaves `PasswordAuthentication` alone. How root logs in —
key only, or password as well — stays whatever your provider set up. On a new
VM, root may be reachable only by password, and a provisioning run that
switched passwords off would lock you out the moment sshd restarts. If you want
key-only login, make that change yourself once you have confirmed that your key
works.

## Check before you continue

Run this from your own machine. All four should answer:

```shell
for h in 1 2 3 4; do
  printf 'play%s: ' "$h"
  ssh -o BatchMode=yes root@play$h.playcluster.plone.org hostname 2>&1 | tail -1
done
```

`BatchMode=yes` makes SSH fail instead of prompting, so a hang is a real
failure rather than a question you missed.

If all four print their hostname, you are ready for Ansible.
