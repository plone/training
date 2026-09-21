---
myst:
  html_meta:
    "description": "Prepare four clean Ubuntu VMs, SSH access and an Ansible vault before provisioning the playcluster"
    "property=og:description": "Prepare four clean Ubuntu VMs, SSH access and an Ansible vault before provisioning the playcluster"
    "property=og:title": "Preparing the cluster VMs"
    "keywords": "Plone, deployment, Ansible, vault, Ubuntu, SSH, GitLab Runner, Docker Swarm"
---

(cluster-vms-label)=

# Preparing the cluster VMs

This chapter covers everything that happens *before* Ansible installs anything.
We start from four freshly installed virtual machines and end with two things:

- four hosts that Ansible can reach as `root` over SSH, and
- an encrypted vault that holds every secret the provisioning run needs.

Nothing is installed on the machines yet at the end of this chapter.
That is deliberate: when something goes wrong later, you know the starting point was clean.

All commands run from a checkout of the [training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, unless stated otherwise.

## The four machines

The cluster consists of four VMs with one job each.

| Host | Role | Runs |
| --- | --- | --- |
| `play1` | Swarm manager | Traefik, Portainer, the deployed Plone stacks |
| `play2` | Swarm worker | Plone stack services |
| `play3` | Swarm worker | Plone stack services |
| `play4` | Standalone, **not** in the swarm | GitLab Runner, the zot container registry |

`play4` stays out of the swarm on purpose.
It runs its own Traefik on ports 80 and 443, and CI jobs should not land in an orchestrated environment.

### DNS first

Create the DNS records *before* the first provisioning run.
Traefik requests its TLS certificates from Let's Encrypt when it starts, and that only works for names that already resolve to the right host.

| Name | Type | Points to |
| --- | --- | --- |
| `play1.playcluster.plone.org` … `play4.playcluster.plone.org` | A | each VM's public IP |
| `traefik.playcluster.plone.org` | CNAME | `play1` |
| `portainer.playcluster.plone.org` | CNAME | `play1` |
| `registry.playcluster.plone.org` | CNAME | `play4` |

Check them all at once:

```shell
for n in play1 play2 play3 play4 traefik portainer registry; do
  printf '%-34s %s\n' "$n.playcluster.plone.org" "$(dig +short $n.playcluster.plone.org | tr '\n' ' ')"
done
```

Every line needs an address.
Port 443 must also be reachable from the internet, because Let's Encrypt validates on it.

## Step 1: four clean Ubuntu 26.04 VMs

Create the VMs from your hosting provider's Ubuntu 26.04 image.
A fresh VM has exactly one account that matters, `root`.
The provisioning run creates everything else.

Bring all four to the same patch level before you start:

```shell
ssh root@play1.playcluster.plone.org 'apt-get update && apt-get -y full-upgrade && reboot'
```

Repeat for `play2` to `play4`.
Provisioning refreshes the package lists but never upgrades.
Machines created from the "same" image minutes apart can still differ.
While preparing this training, `play1` came up as 26.04 and the other three as 26.04.1.

```{warning}
If you *reset* a VM, make sure it really is clean before you provision it.
Check that it reports Ubuntu 26.04, that `docker` is not installed, and that only port 22 is listening.
A machine that silently kept its old disk still runs its old services, and provisioning on top of them mixes two setups.
```

## Step 2: SSH access as root

In the reference: {ref}`playcluster-ref-ssh-and-users`.

Ansible provisions the hosts over SSH as `root`.
Use a key pair dedicated to this cluster, rather than your everyday key:

```shell
ssh-keygen -t ed25519 -f ~/.ssh/playcluster-ansible -C "playcluster provisioning"
```

Put the *public* half, `~/.ssh/playcluster-ansible.pub`, into root's `authorized_keys` on all four VMs.
Most providers let you select an SSH key when you create the VM, which is the easiest way.

Then tell SSH to use that key and user for these hosts, in `~/.ssh/config`:

```
Host *.playcluster.plone.org
    User root
    IdentityFile ~/.ssh/playcluster-ansible
    IdentitiesOnly yes
```

`IdentitiesOnly yes` stops SSH from offering every other key first.
Some servers count those as failed attempts and disconnect.

A reset VM gets a new host key, so SSH refuses to connect and warns that the host identification has changed.
That is expected after a reset.
Remove the old entries, then connect once to accept the new keys:

```shell
for h in 1 2 3 4; do ssh-keygen -R play$h.playcluster.plone.org; done
```

```shell
for h in 1 2 3 4; do ssh -o StrictHostKeyChecking=accept-new root@play$h.playcluster.plone.org hostname; done
```

Finally, let Ansible confirm it can reach all four:

```shell
make install
```

```shell
uv run ansible-playbook playbooks/_connect.yml
```

It prints the Ubuntu release and IP addresses of each host.
All four should report Ubuntu 26.04.

```{note}
`root` is the *setup* user.
The provisioning run creates a second account, `plone`, which is the *deployment* user that CI later logs in as to run `docker stack deploy`.
The repository's documentation, chapter "SSH, keys and the two users", explains both.
Provisioning does not switch off password authentication, and it refuses to write an SSH configuration that would lock out the account Ansible is connected as.
```

## Step 3: a new vault

Every secret the cluster needs lives in one encrypted file, `inventory/group_vars/all/vault.yml`.
The `vault.yml` in the repository is encrypted with the maintainer's password, so it is of no use to you.
Replace it with your own.

### The vault password

Ansible reads the vault password from `.vault_pass` in the repository root.
`ansible.cfg` points there, and `.gitignore` keeps it out of Git.
The file has to have exactly that name.

```shell
openssl rand -hex 32 > .vault_pass
```

```shell
chmod 600 .vault_pass
```

Store this password in your password manager too.
Without it, the vault cannot be opened, and everything in it has to be regenerated.

### What goes into the vault

The vault in more detail, including how to edit it later: {ref}`playcluster-ref-ansible`.

| Key | Used for | How to generate |
| --- | --- | --- |
| `traefik.ui_basic_auth` | Login for both Traefik dashboards | `htpasswd -nbB admin '<password>'` |
| `registry.accounts.ci` | Registry account that pushes images from CI | `openssl rand -hex 24` |
| `registry.accounts.deploy` | Read-only registry account the swarm pulls with | `openssl rand -hex 24` |
| `gitlab.runner_tokens.play4` | Registers the GitLab Runner on `play4` | From GitLab, see step 4 |
| `proxy_credentials` | Only if your hosts need an HTTP proxy | leave empty |

`htpasswd` stores only a *hash* of the Traefik password in the vault.
Keep the plain password in your password manager, because the vault cannot give it back.

The `ci` and `deploy` passwords become CI/CD variables in GitLab later, see {ref}`gitlab-runner-config-label`.
`ci` can push, while `deploy` can only pull.
Keep them separate.
The swarm stores the pull credentials on every node, and push rights must never end up there.

### Creating the vault

The repository has a template with a placeholder for each secret, `etc/vault.template.yml`.
Copy it, fill in the copy, encrypt it into place, and delete the copy:

```shell
cp etc/vault.template.yml vault.plain.yml
```

```shell
uv run ansible-vault encrypt --output inventory/group_vars/all/vault.yml vault.plain.yml
```

```shell
rm vault.plain.yml
```

Fill in the *copy*, never the template.
The template is tracked by Git, so a filled-in template is one `git add` away from publishing your secrets in plain text.
`vault.plain.yml` is in `.gitignore` for exactly this reason.

Check that the new vault opens:

```shell
uv run ansible-vault view inventory/group_vars/all/vault.yml
```

```{warning}
Do not add `--vault-password-file .vault_pass` to these commands.
`ansible.cfg` already supplies it, and naming it twice fails with *"The vault-ids default,default are available to encrypt"*.
```

The runner token is still a placeholder at this point.
The GitLab side comes next.

## Step 4: a runner token from GitLab

In the reference: {ref}`playcluster-ref-ci-runner`.

The GitLab Runner on `play4` runs the CI jobs.
GitLab does not hand you a runner *configuration*, only a token.
Ansible does the rest: it installs the runner, registers it with that token, and writes its configuration.

Register the runner on a GitLab *group*, rather than on a single project.
A group runner picks up jobs from every project in that group, so a new project can use the cluster without any extra setup.
For this training that group is [plone-training1](https://gitlab.com/plone-training1) on GitLab.com; any group on your own GitLab instance works the same way.

1. In the group, go to {menuselection}`Build --> Runners`, and choose {guilabel}`New group runner`.
2. Under **Tags**, enter `docker` and `deploy`.
3. Create the runner.
4. Copy the token that starts with `glrt-`.
   GitLab shows it once.
   Ignore the `gitlab-runner register` command on the same page; Ansible runs the equivalent for you.

A project runner, created under {menuselection}`Settings --> CI/CD --> Runners` in a single project, works just as well if only one project will ever use the cluster.

```{important}
The tags have to match the pipeline.
The demo project sends its build jobs to runners tagged `docker` and its deploy job to runners tagged `deploy`.
Those are the `RUNNER_TAG_BUILD` and `RUNNER_TAG_DEPLOY` variables in its `.gitlab-ci.yml`.
A job whose tag no runner carries does not fail, it waits in the queue indefinitely.
```

The runner must register with the same GitLab instance that issued the token.
That is set in `inventory/group_vars/standalone/runners.yml`:

```yaml
gitlab_runner_coordinator_url: "https://gitlab.com"
```

## Step 5: put the token in the vault

```shell
uv run ansible-vault edit inventory/group_vars/all/vault.yml
```

Replace the `REPLACE-ME` placeholder under `gitlab.runner_tokens.play4` with the `glrt-` token, and save.
The file is re-encrypted when the editor closes.

## Step 6: the keys in `etc/keys/`

Every public key in `etc/keys/*.pub` is installed for the `plone` user on all four hosts.
`plone` has passwordless `sudo`, so each of those keys amounts to root access to the whole cluster.
Look at what is in there before the first run:

```shell
ls -la etc/keys/
```

`etc/keys/` is in `.gitignore`, so Git never shows you its contents.
If you copied this repository from another setup rather than cloning it fresh, the previous owner's keys may still be sitting there, invisible to `git status`, and would be installed on your servers.
Remove anything you did not create yourself.

Then create a key pair for CI.
The pipeline's deploy job uses it to log in to the swarm manager as `plone`:

```shell
ssh-keygen -t ed25519 -f etc/keys/gitlab_ci_deploy -C "gitlab-ci@playcluster.plone.org" -N ""
```

The public half is installed by the provisioning run.
The private half, `etc/keys/gitlab_ci_deploy`, becomes the `DEPLOY_SSH_PRIVATE_KEY` CI/CD variable later.
Keeping CI on its own key means you can cut off the pipeline by removing one key, without touching anyone else's access.

The first provisioning run also creates a second pair here by itself, `plone_prod_deploy_ed25519`, for operators.

## Using your own domain

To build this cluster under a different domain, change the host names in these files, and nowhere else:

`inventory/hosts.yml`
: The four hosts.

`inventory/group_vars/all/stacks.yml`
: `TRAEFIK_UI_HOSTNAME` and `PORTAINER_HOSTNAME`.

`inventory/group_vars/standalone/registry.yml`
: `registry.hostname`.

`inventory/group_vars/standalone/runners.yml`
: The runner `name` and `gitlab_runner_coordinator_url`.

`inventory/group_vars/all/base.yml`
: `devops.email`, the address your Let's Encrypt account is registered with.

Then search for the old domain to catch anything left over:

```shell
git grep -n "playcluster.plone.org"
```

## Checklist before provisioning

- All seven DNS names resolve, and port 443 is reachable from the internet.
- All four VMs report Ubuntu 26.04 at the same patch level, with nothing else installed.
- `uv run ansible-playbook playbooks/_connect.yml` reaches all four hosts.
- `uv run ansible-vault view inventory/group_vars/all/vault.yml` opens the vault.
- The vault contains the `glrt-` runner token, not the placeholder.
- The runner in GitLab carries the tags `docker` and `deploy`.
- `etc/keys/` holds only keys you created yourself, including the `gitlab_ci_deploy` pair.

With all of that in place, continue with {ref}`cluster-provisioning-label`, which provisions the hosts one at a time.
