---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# The Plone Playbook

## Supported Platforms

We support two Linux families: Debian and RHEL.
*Support* means that the playbook knows how to load platform package dependencies and how to set up users, groups, and the platform's method for setting up daemons to start and stop with the operating system.

```{note}
There's no particular reason why we can't extend that support to other families, like BSD.
All we need is a champion to take responsibility for extending and testing on other platforms.
```

Debian

> Our goal is to support the current Ubuntu LTS and the Debian equivalent.
> Currently we're doing a bit better than that.
> On Ubuntu we're supporting everything from Trusty to Xenial.
> On Debian, we're working with both Jessie and Wheezy.

RHEL

> We're currently only testing on CentOS 7.
> If you're using Plone on RHEL, we could use your help on extending that support.

### Quick review of contents

Let's review what you're getting when you check out the Plone Ansible Playbook.

#### Playbooks

We include two playbooks:

playbook.yml

> The main playbook that sets everything except the firewall.

firewall.yml

> A separate playbook to set up the software firewall.
> Most sysadmins have their own firewall experience, and may or may not choose to use this playbook.

#### roles

Roles are basically pre-packaged subroutines with their own default variables.
Several roles are part of the Plone Ansible Playbook kit and will be present in your initial checkout.
These include roles that set up the HAProxy load balancer, varnish cache, nginx `http` server, postfix SMTP agent, munin-node monitoring, logwatch log analysis, message-of-the-day and a fancy setup for restarting ZEO clients.

Other roles, including the role that actually sets up Plone, are loaded when you use `ansible-galaxy` to fetch the items listed in {file}`requirements.yml`.
Except for the Plone server role, these are generally generic Ansible Galaxy roles that we liked.

#### Vagrant

Vagrant/VirtualBox is a handy way to test your playbook, both during development and for future maintenance.
We include a couple of files to help you get started with Vagrant testing.

Vagrantfile

> A Vagrant setup file that will allow you to create guest virtual hosts for any of the platforms we support and will run Ansible as the provisioner with playbook.yml.
> This defaults to building a Xenial box, but you may pick others by naming them on the {command}`vagrant up` command line.

vbox_host.cfg

> When you use vagrant commands, vagrant controls the ssh connection.
> {file}`vbox_host.cfg` is an Ansible inventory file that should allow you to run your playbook directly (without the {command}`vagrant` command) against your guest box.

#### Sample configurations

The playbook kit contains several sample configuration files.

sample-very-small.yml

> Targets a server with 512MB of memory and one CPU core.
> Sets up one ZEO client with two threads with small object caches.
> No load balancer.
> Varnish cache is file-based.

sample-small.yml

> Targets a server with 1GB of memory and one CPU core.
> Sets up one ZEO client with two threads with small object caches.
> No load balancer.
> Varnish cache is file-based.

sample-medium.yml

> Targets a server with 2GB of memory and two CPU cores.
> Sets up two ZEO clients, each with one thread with a medium object cache.
> Uses load balancer to manage the queue to the ZEO clients.
> Varnish cache is memory-based.

`sample-multiserver.yml`

> A configuration that demonstrates how to run multiple Zope/Plone installs with different versions and virtual hosting.

The first four samples are meant to be immediately useful.
Copy and customize.
The `multiserver` sample is a demonstration of several customization techniques.
Read it for examples, but don't expect to use it without substantial customization.

Why no `sample-large.yml`?
Because a larger server installation is always going to require more thought and customization.
We'll discuss those customization points later.
The `sample-medium.yml` file will give you a starting point.

#### Tests

You'll find a {file}`tests.py` program file and a {file}`tests` directory.
The {file}`tests` directory contains Doctest files to test our sample configurations.
You may add your own.

The {file}`tests.py` program is a convenience script that will run one or more of the Vagrant boxes against one or more of the Doctest files.
Run it with no command line argument for usage help.
Or, read the source ;)
