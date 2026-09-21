---
myst:
  html_meta:
    "description": "Plone deployment with Ansible and Docker"
    "property=og:description": "Plone deployment with Ansible and Docker"
    "property=og:title": "Plone deployment with Ansible and Docker"
    "keywords": "Plone, deployment, Ansible, Docker"
---

(deployment-label)=

# Plone deployment

About
: Plone deployment to a Docker Swarm training cluster

Level
: All levels

```{note}
This training is, different from previous years, not a course that you can work through as an individual user.

It will be a 'show/point/tell' workshop to showcase the matured tooling that Plone Community members have been building, extending and providing as open source for the last 5 years.

If you want to deploy your own small stack using cookieplone to a single host, please check last year's [2025 deployment training](https://2025.training.plone.org/).
```

The training comes in blocks. Each narrative block tells the story of one part
of the day. After it comes the reference documentation of the repository that
part is built from, copied here unchanged, for when you want the details.

```{toctree}
:caption: Introduction
:hidden: true
:maxdepth: 3

intro
deploy-challenges
community-resources
```

```{toctree}
:caption: Building the cluster
:hidden: true
:maxdepth: 3

cluster-vms
cluster-provisioning
gitlab-runner-config
```

```{toctree}
:caption: "Reference: the playcluster repository"
:hidden: true
:maxdepth: 3

reference/playcluster/index
reference/playcluster/1-ssh-and-users
reference/playcluster/2-ansible
reference/playcluster/3-manager
reference/playcluster/4-workers
reference/playcluster/5-ci-runner
reference/playcluster/6-gitlab
reference/playcluster/7-registry
```

```{toctree}
:caption: Deploying a Plone site
:hidden: true
:maxdepth: 3

playcluster
build-deploy-gitlab
cookieplone-extends
```

```{toctree}
:caption: "Reference: the deploy demo repository"
:hidden: true
:maxdepth: 3

reference/deploy-demo/index
reference/deploy-demo/1-project
reference/deploy-demo/2-differences
reference/deploy-demo/3-pipeline
reference/deploy-demo/4-registry
reference/deploy-demo/5-deploy
reference/deploy-demo/6-operating
```
