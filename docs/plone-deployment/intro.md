---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Introduction

The subject of this training is the deployment of Plone for production purposes.

We will, in particular, be focusing on automating deployment using tools which can target
a fresh Linux server and create on it an efficient, robust server.

That target server may be a cloud server newly created on {term}`AWS`, {term}`Linode` or {term}`DigitalOcean`.

Or, it may be a virtual machine created for testing on your own desk or laptop.

Our goal is that these deployments be *repeatable*.
If we run the automated deployment multiple times against multiple cloud servers, we should get the same results.

If we run the automated deployment against a virtual machine on our laptop, we should be able to test it as if it was a matching cloud server.

The tools we use for this purpose reflect the opinions of our community, but they are not the only way of deploying Plone in production.

In this training we will focus on a simple setup that could be scaled to fit a big Plone installation, if needed.

## Training Choices

Linux

> BSD is great.
> macOS is familiar.
> Windows works fine, too.
> But our experience and the majority experience in the Plone community is with Linux for production servers.
> That doesn't mean you have to use Linux for your laptop or desktop; anything that runs Python is likely fine.

Major distributions

> We're supporting Ubuntu LTS for the server setup.

Platform packages

> We use platform packages whenever possible.
> We want the non-Plone components on your server to be automatically updatable using your platform tools.
> If a platform package is usable, we'll use it even if it isn't the newest, coolest version.

Ansible

> There are all sorts of great tools for automating deployment.
> People we respect have chosen Puppet, Salt/Minion and lots of other tools.
> We chose Ansible because it requires no preinstalled server component, it's written in Python,
> and its configuration language is YAML, which is awfully easy to read.

Docker and Docker Compose

> We believe containers guarantee repeatable deploys that could run both locally and in production.
> Docker is the most famous solution in this landscape, have good documentation and it is used by our community.
> Docker compose is a tool that is easy to explain and setup, even for new users.

Github and Github actions

> Plone's development happens on Github, and our community is slowly adopting Github actions in their new packages
> Concepts explained here could be easily adapted to other enviroments like Gitlab and Jenkins

Kubernetes

> This version of the training does not (yet) support Kubernetes, but this may change in the near future

And ...

> We'll discuss particular parts of the deployment stack in the next section.
