---
myst:
  html_meta:
    "description": "Introduction for Plone Deployment with Ansible and Docker"
    "property=og:description": "Introduction for Plone Deployment with Ansible and Docker"
    "property=og:title": "Introduction for Plone Deployment with Ansible and Docker"
    "keywords": "Introduction, Plone, Deployment, Ansible, Docker"
---

# Introduction

The subject of this training is the deployment of Plone for production purposes.

We will, in particular, be focusing on automating deployment using tools which can target
a fresh Linux server and create on it an efficient, robust server.

That target server may be a cloud server newly created on {term}`AWS`, {term}`Linode` or {term}`DigitalOcean`.

Or, it may be a virtual machine created for testing on your own desk or laptop.

The goal is that these deployments are _repeatable_.
If you run the automated deployment multiple times against multiple cloud servers, you should get the same results.

If you run the automated deployment against a virtual machine on your laptop, you should be able to test it as if it was a matching cloud server.

The tools to use for this purpose reflect the opinions of the Plone community, but they are not the only way of deploying Plone in production.

In this training we will focus on a basic setup that could be scaled to fit a big Plone installation, if needed.

## Training Choices

Linux

> BSD is great.
> macOS is familiar.
> Windows works fine, too.
> But the majority experience in the Plone community is with Linux for production servers.
> That doesn't mean you have to use Linux for your laptop or desktop; anything that runs Python is likely fine.

Major distributions

> Ubuntu LTS is supported for the server setup and in the training.
> Debian is very similar.
> Other distributions with recent packages might work too.

Platform packages

> Use platform packages whenever possible.
> The non-Plone components on your server should be automatically able to update using your platform tools.
> If a platform package is usable, use it even if it isn't the newest, coolest version.

Ansible

> There are all sorts of great tools for automating deployment.
> People at various times have chosen Puppet, Salt/Minion and other tools.
> This training uses Ansible because it requires no preinstalled server part, it's written in Python,
> and its configuration language is YAML, which is easy to read.

Docker and Docker Swarm

> Containers guarantee repeatable deployments that could run both locally and in production.
> Docker is the most famous solution in this landscape, has good documentation and is in use by our community.
> Docker Swarm is a toolset that's easy to explain and setup, even for new users.

GitHub and GitHub actions

> Plone's development happens on GitHub, and the community is increasingly adopting GitHub actions in their new packages
> Concepts explained here could be adapted to other environments like GitLab and Jenkins

Kubernetes

> This version of the training doesn't (yet) support Kubernetes, but this may change in the near future

And ...

> Particular parts of the deployment stack are discussed in the next section.
