============
Introduction
============

The subject of this training is using Amazon Opsworks deployment system to
orchestrate complex, scalable, and redundant multi-server deployments of
Plone.

The tools presented herein provide a mechanism for generically defining
server requirements and resources to launch fully configured Amazon EC2
instances running Plone in a coordinated distributed manner.

Amazon Opsworks does not provide the flexibility of Ansible deployments.
It is tied to Amazon cloud infrastructure, and is only fully tested for servers
running Ubuntu LTS.

It does provide an unique infrastructure to automate
communication among multiple servers, allowing automated discovery and
inclusion of resources, and facilitating features like auto-scaling and auto-
healing.

Opsworks is built on Chef, which is a configuration management system similar
to Ansible, but built on Ruby [*]_.

The tools and concepts described here attempt to ensure that you can deploy a complex Plone site without having to
learn any Chef or Ruby.

.. [*] Yuck!

