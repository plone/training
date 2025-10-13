---
myst:
  html_meta:
    "description": "Introduction to Plone Deployment with Ansible and Docker"
    "property=og:description": "Learn how to deploy Plone efficiently and robustly using Ansible and Docker."
    "property=og:title": "Plone Deployment with Ansible and Docker"
    "keywords": "Plone, Deployment, Ansible, Docker, Training"
---

# Introduction

This training provides practical guidance for deploying Plone in production.
It focuses on automating deployments so you can reliably transform a fresh Linux server into a production-ready Plone instance.

## Target Audience

Whether you are looking to deploy on a newly created cloud server on {term}`AWS`, {term}`Linode`, or {term}`DigitalOcean`,
or considering a virtual machine on your personal computer for testing, this training is tailored for you.

## Objectives

- Describe the lifecycle of a Plone project.
- Achieve repeatable deployments.
- Ensure consistency across multiple deployment instances.
- Impart knowledge on the tools reflecting the Plone community's preferences.

## Different types of Plone codebases

In the Plone ecosystem there are three common codebase types:

| Type | Definition | Example |
| --  | -- | -- |
| Distribution  | An opinionated packaging of Plone, usually focused on a vertical market or specific use case. | kitconcept Intranet, Quaive, ioCommune |
| Add-On  | A package (or group of packages) that extends Plone with new features. | EEA Accordion, Volto Form Support, Volto Light Theme, Collective Tech Event |
| Project  | A specific implementation of Plone (or a Plone-based distribution) used to create a site, intranet, or knowledge base. | Plone Conference Site, Plone.org, DLR.de |

Add-ons are typically tested against a matrix of supported versions: backend add-ons against multiple Python and Plone versions, and frontend add-ons against Node and Volto version matrices. Distributions are released with a narrower, opinionated set of pinned dependencies to reduce integration complexity.

Project codebases generally require strict repeatability and therefore pin exact dependency versions.
For projects managed with `zc.buildout`, it has been best practice to include a `versions.cfg` file that controls package versions. In this training we follow the same principle: we use a backend lockfile ( `uv.lock`) and `pnpm-lock.yaml` for the frontend.

(deployment-training-choices)=

### Training choices

#### Linux

While BSD, macOS, and Windows are viable options, the Plone community predominantly prefers Linux for production servers.
However, any system capable of running Python should suffice for development purposes.

#### Major Distributions

We recommend Ubuntu LTS for server deployments. Debian and other stable distributions with up-to-date packages are also supported.

#### Platform Packages

Prefer using distribution-packaged system packages where practical to benefit from automatic security updates and easier maintenance. Favor stability and maintainability over running the absolute latest upstream versions on production systems.

#### Ansible

Ansible is a natural fit for our automation needs: it's agentless, written in Python, and uses readable YAML playbooks. Its idempotent design and role-based structure make it a good choice for repeatable server provisioning.

#### Docker and Docker Swarm

Containers provide consistency and repeatability. Docker (and Docker Compose for local orchestration) is used throughout this training; Docker Swarm is the recommended option for lightweight orchestration in production scenarios covered here.

#### GitHub and GitHub Actions

With Plone's development anchored on GitHub, the community is gravitating towards GitHub Actions for new packages.
The principles outlined are adaptable to GitLab, Jenkins, and similar platforms.

#### Kubernetes

This edition of the training does not cover Kubernetes, but we expect to include Kubernetes-based deployment patterns in a future update. The Plone community maintains Helm charts that can be used as a starting point: https://github.com/plone/helm-charts
