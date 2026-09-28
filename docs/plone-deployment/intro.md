---
myst:
  html_meta:
    "description": "Introduction to Plone Deployment Training 2026"
    "property=og:description": "Learn how to deploy Plone efficiently and robustly using Ansible and Docker."
    "property=og:title": "Plone Deployment Autonomously"
    "keywords": "Plone, Deployment, Ansible, Docker, Training"
---

# Introduction

This training provides practical guidance for deploying Plone in production.

In line with last year's (2025) deployment training, this training still focusses on automating Plone deployments. As opposed to last year, instead of letting participants practise with setting up cookieplone, and use the devops/ansible templates in cookieplone in a single repository to set up a single host, I want to present a possible 'end result', once you start customising and personalising the setup for your own organisation.

## Target Audience

This training will show intermediate/experienced developers and system administrators how you can use the available community tooling to set up a more elaborate training setup, with a multi-node cluster. Where we extend the cookieplone generated default scaffolding to customise the setup for use at an integrator or client.

## Objectives

- Understand the current cookieplone scaffolding scope, and where you should start to customise the setup for your own purposes
- Demonstrate a small multi-node cluster, which adds extra deployment config and requirements.
- Showcase the challenges when you deploy multiple projects with colleagues/friends to a single cluster.
- Document a setup you could host yourself fully without using any cloud/saas services.
- Document a full GitLab CI/CD configuration

## Digital Autonomy / Sovereignty

The main theme of Plone Conference 2026 is "Own your digital future" and autonomy. For training purposes, convenience and exposure, the Plone Community has been using GitHub for many years now. We use GitHub to develop Plone to a large extent, but also host Documentation, training materials, and use GitHub's CI/CD automation, both for Plone deliverables and for educational purposes. We also use GitHub Container Registry to save images, and use the provided cloud hosted runners.

But what if you want to develop, test and deploy a Plone website fully autonomously, from your own managed servers and fully open source software also for the tooling? GitLab is currently the best known source code platform with integrated CI/CD and many other features, distributed under a license that you can install on your own servers. It also has good enough features in the open source edition, where you are not obligated (but still can) extend GitLab with extra paid features, either self-hosted or SaaS.

There are other existing open source projects where you can host your source code, run automations, run tests and deploy, but you have to integrate them yourself. Forgejo is a promising project that packages the existing projects further in a fully open source GitHub/GitLab replacement, of which I wonder if future trainings could be built on it.

## From abstraction to instance, main deliverables

The 'value' of this training is mainly in two example repositories, which have been generated with Cookieplone, and then extended / customised to cater for real-world scenarios, when you start working together on several Plone projects using containerisation as the deployment strategy.

This is the part that you don't see in public repositories/setups, as the setup becomes customised for the specific demands of a single organisation or Plone integrator. And we don't share the details of those setups, for security reasons, and because documenting our individual permutation (code control tool X, with CI solution Y, with config/solution Z) is too niche.

The Plone Community doesn't have the resources to support and maintain 'production grade' fully abstracted scaffolding in cookieplone for all the combinations of these required tooling, CI/CD solution, and Server Deployments. This training is an experiment where we begin with a specific end result in mind: an autonomous training cluster that can lead to a production deployment.

## GitLab.com

We will use gitlab.com as a hosted service so that we have exposure, and don't need to set up a full GitLab locally hosted instance. If time permits, I also want to offer you to experiment in the afternoon with deploying a project to our demo cluster. But you can also host GitLab yourself. From there on everything else (ci/cd, deployment) is running on systems you host and manage yourself.

## Kubernetes

This edition of the training still does not cover Kubernetes. Last year's (2025) deployment training documented our interest in providing Kubernetes examples, but we didn't manage so far as a community. In that regard, this year's training could be a starting point, where we begin with a 'customised' setup, and then swap out the docker swarm containerisation part of the setup for a small kubernetes cluster.


## History of this training

Working at a Plone integrator (kitconcept), we got a request in 2026 to organise and give a full in-house training program for a client. Before this request, I already had the idea of a 'playcluster' at the beginning of 2026 for internal use at kitconcept. A training ground where we can set up a cluster with Ansible, where everything can be done and broken, no customer projects involved, by whoever wants to train and experiment on devops.

A secondary wish was to have a full GitLab CI/CD setup documented. With GitLab's option to self-host, and adding a bit more digital autonomy on the runner, a fully 'stand alone' Plone deployment pipeline was the new goal.

Cookieplone has reached traction in the community, has excellent documentation now on both docs.plone.org and on its own documentation at <https://plone.github.io/cookieplone/>, and got a major update this year with interesting new features.

Combined with the insight that we have a grey area between local development setup and 'serious' deployment setup, the idea was to do a 'show and tell' training instead of trying to provide an interactive training this year.

