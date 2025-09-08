---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Introduction

The subject of this training is using the {term}`Amazon OpsWorks` deployment system to orchestrate complex, scalable,
and redundant multi-server deployments of Plone.

The tools presented herein provide a mechanism for generically defining server requirements and resources
to launch fully configured Amazon EC2 instances running Plone in a coordinated distributed manner.

Amazon OpsWorks does not provide the flexibility of {term}`Ansible` deployments.
It is tied to Amazon cloud infrastructure, and is only fully tested for servers running Ubuntu LTS.

It does provide an unique infrastructure to automate communication among multiple servers,
allowing automated discovery and inclusion of resources, and facilitating features like auto-scaling and auto- healing.

OpsWorks is built on {term}`Chef`, which is a configuration management system similar to Ansible, but built on Ruby [^id2].

The tools and concepts described here attempt to ensure that you can deploy a complex Plone site without having to
learn any Chef or Ruby.

[^id2]: Yuck!
