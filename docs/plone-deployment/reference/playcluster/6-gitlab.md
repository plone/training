---
myst:
  html_meta:
    "description": "The GitLab CI/CD variables a pipeline needs to push to the cluster's registry and deploy to its swarm."
    "property=og:title": "6. Connecting GitLab"
    "keywords": "GitLab CI, CI/CD variables, registry, Docker Swarm, deploy"
---

(playcluster-ref-gitlab)=

# 6. Connecting GitLab

% Exported from training-deployment-playcluster 00fc574 by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-playcluster](https://github.com/plone/training-deployment-playcluster) repository, and is maintained
there.
```

The runner is registered, but a pipeline still needs to know where the registry
is, how to log in to it, and how to reach the swarm. It gets all of that from
CI/CD variables, set once in GitLab. This chapter is still about the cluster,
not about a particular project: with the variables on the GitLab group, every
project in the group can build, push and deploy.

## The variables

| Key | Value | Protected | Masked |
| --- | --- | --- | --- |
| `REGISTRY_IMAGE_PREFIX` | `registry.playcluster.plone.org/$CI_PROJECT_PATH` | **No** | No |
| `REGISTRY_USER` | `ci` | Yes | Not possible, too short |
| `REGISTRY_PASSWORD` | `registry.accounts.ci` from the vault | Yes | Yes |
| `REGISTRY_PULL_USER` | `deploy` | Yes | Not possible, too short |
| `REGISTRY_PULL_PASSWORD` | `registry.accounts.deploy` from the vault | Yes | Yes |
| `DEPLOY_HOST` | `play1.playcluster.plone.org` | Yes | No |
| `DEPLOY_USER` | `plone` | Yes | No |
| `DEPLOY_SSH_PRIVATE_KEY` | contents of `etc/keys/gitlab_ci_deploy` | Yes | Not possible, multi-line |

The two passwords are in the vault:

```shell
uv run ansible-vault view inventory/group_vars/all/vault.yml
```

The deploy key is the private half of the CI key pair from chapter 1:

```shell
cat etc/keys/gitlab_ci_deploy
```

What they are for:

`REGISTRY_IMAGE_PREFIX`
: Where images are pushed to and pulled from. Everything before the first `/` is
  the registry's host name.

`REGISTRY_USER`, `REGISTRY_PASSWORD`
: The `ci` account. Build jobs push images with it.

`REGISTRY_PULL_USER`, `REGISTRY_PULL_PASSWORD`
: The read-only `deploy` account. The deploy job passes these to the swarm, which
  stores them on every node so it can pull again after a reboot. That is why
  they must not be the push credentials.

`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_PRIVATE_KEY`
: How the deploy job logs in to the manager to run `docker stack deploy`.

## Group or project

Set the variables on the group, under {menuselection}`Settings --> CI/CD --> Variables`,
and every project in it inherits them. That matches the group runner from
chapter 5.

Be clear about what that grants. `DEPLOY_SSH_PRIVATE_KEY` logs in as `plone`,
which has passwordless `sudo`. A Maintainer of *any* project in the group can
read the group's variables through a pipeline, and so can become root on the
cluster. That is fine while only the people who run the cluster create projects
there. Once others get Maintainer rights on projects in the group, set the
deployment variables per project instead.

## Settings that are easy to get wrong

**`REGISTRY_IMAGE_PREFIX` must not be protected.** The first job of the pipeline
runs in every pipeline, including merge requests on unprotected branches, which
do not receive protected variables. On GitLab.com the pipeline then does not
fail: it falls back to GitLab's own container registry, which is always enabled
there. Images get pushed to GitLab.com while the deploy looks for them in your
registry.

**`$CI_PROJECT_PATH` is resolved by the pipeline, not by GitLab.** One group
variable, `registry.playcluster.plone.org/$CI_PROJECT_PATH`, gives every project
its own place in the registry, such as `plone-training1/my-site`. But GitLab
hands a group variable's reference to a predefined variable to the job as it is,
literally `$CI_PROJECT_PATH` — whatever the *Expand variable reference* setting
says. The deploy project's first job therefore expands the reference itself, and
stops with an error if anything is left unresolved. Image names must be
lowercase, so keep project paths lowercase.

**Protected variables need protected branches and tags.** The default branch is
protected by default. If you build releases from Git tags, add a protected tag
rule `*` under {menuselection}`Settings --> Repository --> Protected tags` in
each project, or tag pipelines run without credentials and fail at
`docker login`.

**`DEPLOY_SSH_PRIVATE_KEY` is of type *Variable*, not *File*.** The deploy job
expects the key itself. A *File* variable holds the path to a temporary file,
and the job would install that path as its key. The key cannot be masked, since
masked values must fit on one line; protecting it is what keeps it away from
unprotected branches.

**The runner needs both tags**, `docker` and `deploy` — see chapter 5. A job
whose tag no runner carries stays pending indefinitely, without an error.
