---
myst:
  html_meta:
    "description": "Deploying your own copy of the deploy demo onto the playcluster, and how Cookieplone's extends could turn the GitLab layer into a template."
    "property=og:description": "Deploying your own copy of the deploy demo onto the playcluster, and how Cookieplone's extends could turn the GitLab layer into a template."
    "property=og:title": "Your own project, and what comes next"
    "keywords": "Plone, cookieplone, extends, GitLab CI, Docker Swarm, repository.toml"
---

(cookieplone-extends-label)=

# Your own project, and what comes next

So far, one project runs on the cluster.
In this chapter, two or three groups each deploy a copy of it next to the reference, and see where that goes smoothly and where it does not.
Afterwards we look at how the setup could become something you generate instead of copy.

## Deploying a copy

### What you get for free

Each group gets its own project in the `plone-training1` group on `gitlab.com`, as a copy of `training-deployment-gitlabdeploy`.
A lot comes with the GitLab group, without any setup in the new project:

- **The runner** on `play4` is a group runner, so it picks up the new project's jobs.
- **The CI/CD variables** are group variables: registry accounts, the swarm manager, the deploy key.
- **Its own place in the registry.**
  The registry prefix is `registry.playcluster.plone.org/$CI_PROJECT_PATH`, so a project called `plone-training1/project2` pushes to `…/plone-training1/project2/backend`, not over the reference's images.

```{warning}
The group variables include the deploy key, which logs in to the cluster as `plone`, and `plone` has `sudo`.
They are protected, so they only reach pipelines on `main` and on release tags — but a Maintainer of any project in the group can push there, and so read them.
Everyone with that role today is trusted with the cluster.
That is fine for a training cluster that is taken down after the training; on a cluster that matters, the deployment variables belong on each project instead.
```

### The first pipeline stops, on purpose

Push the copy, and its first pipeline on `main` stops in `config`:

```console
repository.toml [deployment] still describes plone-training1/training-deployment-gitlabdeploy,
but this pipeline runs in plone-training1/project2.
Set your own hostname, stack_name, stack_prefix and data_path in [deployment],
then set gitlab_project = "plone-training1/project2".
```

Without that check, the copy would deploy with the reference's settings: same stack name, so it would replace the reference site, and same data directory, so its database would write into the reference's.
Branches and merge requests of the copy still lint and test; only building and deploying wait.

### Describe your own deployment

In your copy's `repository.toml`, change all five together:

```toml
[deployment]
gitlab_project = "plone-training1/project2"
hostname       = "project2.playcluster.plone.org"
stack_name     = "project2-playcluster-plone-org"
stack_prefix   = "project2"
data_path      = "/srv/project2/data"
```

The host names `project1.playcluster.plone.org` and `project2.playcluster.plone.org` already point at the cluster.
The check only catches a copy that changed nothing: one that updates `gitlab_project` but keeps the reference's `data_path` would still share its database directory.

### The same two steps by hand

Before the first deploy, the data directory on `play3`:

```shell
ssh root@play3.playcluster.plone.org mkdir -p /srv/project2/data
```

After it, `create-site` in one of your backend containers, filtering on your own stack name, as in {ref}`build-deploy-gitlab-label`.

### Small problems worth running into

These are the mistakes this setup makes easy, and each teaches something about how the pieces connect:

| You forgot | What you see | Why |
| --- | --- | --- |
| to change `stack_prefix` | One or both sites stop answering, and Traefik's log reports a router defined more than once | Traefik's router names are global to the cluster, so two stacks must not define the same one |
| a DNS record for your host name | A certificate warning, *TRAEFIK DEFAULT CERT* | Let's Encrypt cannot issue a certificate for a name that does not resolve |
| the data directory on `play3` | The deploy times out, the database task says `failed to populate volume` | Docker does not create bind-mount directories |
| `create-site` | Volto's *"This page does not seem to exist…"* | The backend runs, but has no Plone site yet |
| to filter on your own stack in `docker ps` | `create-site` runs in someone else's container | Several stacks' backends can share a node |

The reference documentation explains each in more depth: {ref}`deploy-ref-operating`.

## From copying to generating

Copying a finished project is a good way to learn, and a poor way to start real ones: every copy carries this project's name, its package, and its history.
What you actually want is a new Cookieplone project that comes out with the GitLab layer already in place.

Cookieplone 2.0 makes that possible with **extends**: your own templates repository points at `plone/cookieplone-templates`, and Cookieplone lays your files over the upstream template when it generates a project.
The GitLab layer is small enough to fit — the table in {ref}`community-resources-label` is, in effect, the list of files such a templates repository would contain.

It is not done yet.
New files are easy to add this way, but the files the layer extends, such as `repository.toml` and the Makefiles, have to be carried as full copies of the upstream templates, and kept in step with them.
That is the next step for this training's material, as a third repository next to the two used today.
Until then, the deploy demo is the reference: read it, copy what you need, and keep `repository.toml` as the one place where your deployment is described.
