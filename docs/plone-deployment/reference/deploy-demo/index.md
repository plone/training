---
myst:
  html_meta:
    "description": "How a cookieplone Plone 6 project is built, published and deployed to the cluster by GitLab CI/CD."
    "property=og:description": "How a cookieplone Plone 6 project is built, published and deployed to the cluster by GitLab CI/CD."
    "property=og:title": "From repository to running site"
    "keywords": "Plone, cookieplone, GitLab CI, Docker Swarm, zot, Traefik"
---

(deploy-ref-overview)=

# From repository to running site

% Exported from training-deployment-gitlabdeploy 2d11b5e by
% docs/export_to_training.py. Do not edit this copy; edit the repository.

```{note}
This chapter is part of the reference documentation of the
[training-deployment-gitlabdeploy](https://gitlab.com/plone-training1/training-deployment-gitlabdeploy) repository, and is maintained
there.
```

The other half of the picture. The `training-deployment-playcluster`
repository builds the cluster; these chapters follow a Plone project from a
`git push` to a running site on it.

They are written to be read: the aim is that afterwards you can read this
pipeline, change it, and work out why it broke. Chapter 6 covers what it takes
to deploy a copy of the project yourself.

## The example

`training-deployment-gitlabdeploy`, generated with cookieplone and then adapted for
this cluster. Everything shown is in that repository, and every path mentioned
is real.

## What you should already know

From the cluster documentation: the cluster runs Docker Swarm with a single shared
Traefik on `play1`, application services attach to `nw-public` and
announce themselves with labels, and `play4` runs the CI runner and the
registry outside the swarm.

Those facts constrain nearly every decision here.

## Chapters

| | Chapter | |
| --- | --- | --- |
| 1 | [The project and its images](1-project.md) | |
| 2 | [What differs from vanilla cookieplone](2-differences.md) | |
| 3 | [The pipeline](3-pipeline.md) | |
| 4 | [Images and the registry](4-registry.md) | |
| 5 | [The deploy](5-deploy.md) | |
| 6 | [Operating it](6-operating.md) | |

## The shape of it, in one picture

```
  git push
     |
     v
  +---------------------------- play4 ----------------------------+
  |  GitLab Runner                                                        |
  |                                                                       |
  |  config --> check --> test --> build --------> deploy                 |
  |    |                            |                |                    |
  |    | reads repository.toml      | buildx         | over SSH           |
  |    | publishes settings         v                |                    |
  |    |                        zot registry         |                    |
  |    +----------------------------+----------------+                    |
  +-------------------------------  |  ---------------------------------+-+
                                    |                                   |
                                    | pull                       docker stack deploy
                                    v                                   v
  +------------------------ the swarm: play1/2/3 ---------------+
  |  Traefik --> frontend (x2) --> backend (x2) --> postgres (pinned)     |
  +-----------------------------------------------------------------------+
```

Five stages, one registry, one SSH connection. Everything else is detail.
