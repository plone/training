---
myst:
  html_meta:
    "description": "Introduction to Plone Deployment with Ansible and Docker"
    "property=og:description": "Learn how to deploy Plone efficiently and robustly using Ansible and Docker."
    "property=og:title": "Plone Deployment with Ansible and Docker"
    "keywords": "Plone, Deployment, Ansible, Docker, Training"
---

# Introduction

This training material provides insights into deploying Plone for production.
We aim to impart skills for automating deployment processes,
ensuring that you can transform a fresh Linux server into an efficient and robust Plone server.

## Target Audience

Whether you are looking to deploy on a newly created cloud server on {term}`AWS`, {term}`Linode`, or {term}`DigitalOcean`,
or considering a virtual machine on your personal computer for testing, this training is tailored for you.

## Objectives

- Achieve repeatable deployments.
- Ensure consistency across multiple deployment instances.
- Impart knowledge on the tools reflecting the Plone community's preferences.

## Training Content

We will delve into a basic setup, scalable to accommodate extensive Plone installations.

### Training Choices

#### Linux

While BSD, macOS, and Windows are viable options, the Plone community predominantly prefers Linux for production servers.
However, any system capable of running Python should suffice for development purposes.

#### Major Distributions

We support and recommend Ubuntu LTS for server setup. Debian and other distributions with up-to-date packages are also compatible.

#### Platform Packages

Prioritize platform packages to leverage automatic updates. Opt for usability over the latest versions to ensure stability and security.

#### Ansible

Ansible stands out for its serverless nature, Python foundation, and user-friendly YAML configuration language,
making it a preferred choice for deployment automation.

#### Docker and Docker Swarm

Embrace the consistency and repeatability offered by containers. Docker, complemented by Docker Swarm,
simplifies the setup process, making it accessible even for beginners.

#### GitHub and GitHub Actions

With Plone's development anchored on GitHub, the community is gravitating towards GitHub Actions for new packages.
The principles outlined are adaptable to GitLab, Jenkins, and similar platforms.

#### Kubernetes

While the current training edition doesn't cover Kubernetes, we anticipate its inclusion in future updates.
