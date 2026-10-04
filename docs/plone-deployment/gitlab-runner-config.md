---
myst:
  html_meta:
    "description": "Connect a GitLab project to the playcluster: CI/CD variables for the self-hosted registry and the swarm deployment"
    "property=og:description": "Connect a GitLab project to the playcluster: CI/CD variables for the self-hosted registry and the swarm deployment"
    "property=og:title": "Configuring GitLab for the cluster"
    "keywords": "Plone, deployment, GitLab CI, CI/CD variables, container registry, Docker Swarm"
---

(gitlab-runner-config-label)=

# Configuring GitLab for the cluster

The cluster from {ref}`cluster-provisioning-label` is running, and its runner is registered with GitLab.
One step remains on the GitLab side before any project can use it.
A pipeline needs to know where the registry is, how to log in to it, and how to reach the swarm, and it gets all of that from CI/CD variables.

This chapter is still about the cluster, not about a Plone project.
Everything here is set up once, on the GitLab group, and every project in that group can then build, push and deploy without further configuration.

## The variables

In the reference: {ref}`playcluster-ref-gitlab`.

The pipeline reads eight variables.
None of them is stored in the project's repository.

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

Read the two registry passwords from the vault, in the `training-deployment-playcluster` checkout:

```shell
uv run ansible-vault view inventory/group_vars/all/vault.yml
```

And the private deploy key:

```shell
cat etc/keys/gitlab_ci_deploy
```

What each group of variables does:

`REGISTRY_IMAGE_PREFIX`
: Where images are pushed to, and pulled from.
  Everything before the first `/` is the registry's host name.

`REGISTRY_USER` and `REGISTRY_PASSWORD`
: The `ci` account, used by the build jobs to push images.

`REGISTRY_PULL_USER` and `REGISTRY_PULL_PASSWORD`
: The read-only `deploy` account.
  The deploy job hands these to the swarm, which stores them on every node so it can pull images again after a reboot.
  That is why they must not be the push credentials.

`DEPLOY_HOST`, `DEPLOY_USER` and `DEPLOY_SSH_PRIVATE_KEY`
: How the deploy job logs in to the swarm manager, to run `docker stack deploy`.
  `plone` is the deployment user that provisioning created.
  The key is the CI key pair from {ref}`cluster-vms-label`, not your own.

## Group or project variables

Variables can be set on a single project, or on a group, from where every project in the group inherits them.
The runner in this training is a group runner, so group variables are the natural match:
in {menuselection}`Settings --> CI/CD --> Variables` of the group, add each variable with {guilabel}`Add variable`.

Before you do, be clear about what that grants.
`DEPLOY_SSH_PRIVATE_KEY` logs in as `plone`, and `plone` has passwordless `sudo` on the manager.
A Maintainer of *any* project in the group can read the group's variables through a pipeline, and so can become root on the cluster.
That is fine when only the people who run the cluster create projects in the group.
It is not, once others get Maintainer rights on projects there.
In that case, set the deployment variables on each project instead.

## Settings that are easy to get wrong

**`REGISTRY_IMAGE_PREFIX` must not be protected.**
The pipeline's first job, `config`, runs in every pipeline, including merge request pipelines on unprotected branches, and they do not receive protected variables.
On `gitlab.com`, the job then does not fail.
It quietly falls back to `gitlab.com`'s own container registry, which is always enabled there.
The build pushes to `gitlab.com`, while the deploy looks for the images in your own registry.

**`$CI_PROJECT_PATH` is resolved by the pipeline, not by GitLab.**
The one group variable, `registry.playcluster.plone.org/$CI_PROJECT_PATH`, gives every project its own place in the registry, such as `plone-training1/my-site`.
But GitLab passes that reference to the job literally, as `$CI_PROJECT_PATH`, whatever the *Expand variable reference* setting says.
We found out on the first real pipeline, when the build tried to tag an image called `registry.playcluster.plone.org/$CI_PROJECT_PATH/backend`.
So the deploy project's first job expands the reference itself, and stops with an error if anything is left unresolved.
Container image names must be lowercase, so keep project paths lowercase too.

**Protected variables need protected branches and tags.**
The other seven variables are protected, so jobs only receive them on protected branches and tags.
The default branch is protected by default.
If you build releases from Git tags, add a protected tag rule with the pattern `*` in each project, under {menuselection}`Settings --> Repository --> Protected tags`.
Without it, tag pipelines run without credentials and fail at `docker login`.

**`DEPLOY_SSH_PRIVATE_KEY` is of type *Variable*, not *File*.**
The deploy job expects the key itself in the variable.
A *File* variable contains the path to a temporary file instead, and the job would install that path as its key.
The key cannot be masked, because masked values must fit on one line.
That is acceptable: the deploy job never prints it, and protecting it is what keeps it away from unprotected branches.

**The runner needs both tags.**
The build jobs run on runners tagged `docker`, the deploy job on runners tagged `deploy`.
A job whose tag no runner carries does not fail: it stays pending indefinitely.
