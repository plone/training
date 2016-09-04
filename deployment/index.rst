===========================
Automating Plone Deployment
===========================

.. warning::

   This chapter is still work in progress! Expect it to be refactored.

.. .. toctree::
..    :maxdepth: 3
..    :numbered: 1

Introduction
------------

The subject of this training is the deployment of Plone for production purposes.
We will, in particular, be focusing on automating deployment using tools which can target a fresh Linux server and create on it an efficient, robust server.

That target server may be a cloud server newly created on AWS, Linode or DigitalOcean.
Or, it may be a virtual machine created for testing on your own desk or laptop.

Our goal is that these deployments be *repeatable*.
If we run the automated deployment multiple times against multiple cloud servers, we should get the same results.
If we run the automated deployment against a virtual machine on our laptop, we should be able to test it as if it was a matching cloud server.

The tools we use for this purpose reflect the opinions of the Plone Installer Team.
*We are opinionated*.
With a great many years of experience administering servers and Plone, we feel we have a right to our opinions.
But, most importantly, we know we have to make choices and support those choices.

The tools we use may not be the ones you would choose.

They may not be the ones we would choose this month if we were starting over.

But, they are tools widely used in the Plone community.
They are well-understood, and you should get few "I've never heard of that" complaints if you ask questions of the Plone community.

Our big choices
^^^^^^^^^^^^^^^

Linux

    BSD is great.
    OS X is familiar.
    Windows works just fine.
    But our experience and the majority experience in the Plone community is with Linux for production servers.
    That doesn't mean you have to use Linux for your laptop or desktop; anything that runs Python is likely fine.

Major distributions

    We're supporting two target distribution families: Debian and EL (RedHat/CentOS).
    We're going to try to keep this working on the most recent LTS (Long-Term Support release) or its equivalent.

Platform packages

    We use platform packages whenever possible.
    We want the non-Plone components on your server to be automatically updatable using your platform tools.
    If a platform package is usable, we'll use it even if it isn't the newest, coolest version.

Ansible

    There are all sorts of great tools for automating deployment.
    People we respect have chosen Puppet, Salt/Minion and lots of other tools.
    We chose Ansible because it requires no preinstalled server component, it's written in Python, and its configuration language is YAML, which is awfully easy to read.

And ...

    We'll discuss particular parts of the deployment stack in the next section.

Intro to Plone Stack
--------------------

If you haven't read the first couple of chapters of "Guide to deploying and installing Plone in production" http://docs.plone.org/manage/deploying/index.html, take a moment to do so. You'll want to be familiar with the main components of a typical Plone install for deployment and know when each is vital and when unnecessary.

.. figure:: full_stack.png
    :align: center

    The generic components of a full-stack Plone installation. Not all are always used.

The Plone Ansible Playbook makes choices for each generic component.


.. figure:: stack-components.png
    :align: center

    The specific components used in Plone's Ansible Playbook.

You are not stuck with our choices. If, for example, you wish to use Apache rather than Nginx for the web server component, that won't be a particular problem. You'll just need to do more work to customize.

Intro to Ansible
----------------

Ansible is an open-source configuration management, provisioning and application deployment platform written in Python and using YAML (YAML Ain't Markup Language) as a configuration language.
Ansible makes its connections from your computer to the target machine using SSH.

There is no server-side component other than an SSH server.
General familiarity with SSH is very desirable if you're using Ansible -- as well as being a baseline skill for server administration.

Installation
^^^^^^^^^^^^

Ansible is typically installed on the orchestrating computer -- typically your desktop or laptop.
It is a large Python application (though a fraction the size of Plone!) that needs many specific Python packages from the Python Package Index (PyPI).

That makes Ansible a strong candidate for a Python *virtualenv* installation
If you don't have virtualenv installed on your computer, do it now.

virtualenv may be installed via an OS package manager, or on a Linux or BSD machine with the command:

    $ sudo easy_install-2.7 virtualenv

Once you've got virtualenv, use it to create a working directory containing a virtual Python:

$ virtualenv ansible_work

Then, install Ansible there:

    $ cd ansible_work
    $ bin/pip install ansible

Now, to use Ansible, activate that Python environment.

    $ source bin/activate
    $ ansible

Trainer: check to make sure everyone understands the basic "source activate" mechanism.

Now, let's get a copy of the Plone Ansible Playbook.
Make sure you're logged to your ansible_work directory.

Unless you're participating in the development of the playbook, or need a particular fix, you'll want to clone the "STABLE" branch.
The STABLE branch is a pointer to the last release of the playbook.

    $ git clone -b STABLE --single-branch https://github.com/plone/ansible-playbook.git

That gives you the Plone Ansible Playbook.
You'll also need to install a few Ansible roles.
Roles are Ansible playbooks packaged for distribution.
Fortunately, you may pick up everything with a single command.

    $ cd ansible-playbook
    $ ansible-galaxy install -p roles -r requirements.yml

If you forget that command, it's in the short README.rst file in the playbook.

Ansible basics
^^^^^^^^^^^^^^

Connecting to remote machines
`````````````````````````````

To use Ansible to provision a remote server, we have two requirements:

1. We must be able to connect to the remote machine using ssh; and,

2. We must be able to issue commands as the on the remote server as root (superuser), usually via `sudo`.

You'll need to familiarize yourself with how to fulfill these requirements on the cloud/virtual environment of your choice.
Examples:

* Using Vagrant/virtualbox, you will initially be able to log in as the "vagrant" user using a private key that's in a file created by Vagrant.
The user "vagrant" may issue `sudo` commands with no additional password.

* Using Linode, you'll set a root password when you create your new machine. If you're willing to use the root user directly, you will not need a `sudo` password.

* When setting up a Digital Ocean machine, you'll usually ...

* AWS ...

The most important thing is that you know your setup. Test that knowledge by trying an ssh login and issuing a superuser command.


    $ ssh myuser@myhost.com   # (what user/hostname did you use? are you asked a password?)

    myhost.com $ sudo ls  # (are you asked for your password?)

Inventories
```````````

Ansible is usually run on a local computer, and it usually acts on one or more remote machines.
We tell Ansible how to connect to remote machines by maintaining a text inventory file.

There is a sample inventory configuration file in your distribution.
It's meant for use with a Vagrant-style virtualbox.

    $ cat vbox.cfg

    myhost ansible_ssh_port=2222 ansible_ssh_host=127.0.0.1 ansible_ssh_user=vagrant ansible_ssh_private_key_file=~/.vagrant.d/insecure_private_key

This inventory file is complicated by the fact that a virtualbox typically has no DNS host name and uses a non-standard port and a special SSH key file.
So, we have to specify all those things.

If we were using a DNS-known hostname, it could be much simpler:

    direct.stevemcmahon.com

Ansible inventory files may list multiple hosts and may have aliases for groups of hosts. See docs.ansible.com for details.

You may run Ansible against one, two, all of the hosts in the inventory file, or against alias groups like "plone-servers".

Smoke test
``````````

Let's see if we can use Ansible to connect to a remote machine that we've specified in our inventory.

    $ ansible -i vbox_host.cfg myhost -u steve -a "whoami" -k --become -K


Playbooks
^^^^^^^^^

Quick intro to YAML
```````````````````

python

    #! /usr/bin/python

    import yaml
    import pprint
    import sys

    pprint.pprint(yaml.load(sys.stdin.read()), indent=2)


Quick intro to Jinja2
`````````````````````

Playbook structure
``````````````````

Variables
:::::::::

Tasks -- pre, main, post
::::::::::::::::::::::::

Notifications and handlers
::::::::::::::::::::::::::

Roles
`````

Galaxy
::::::

The Plone Playbook
------------------

Checkout
^^^^^^^^

Requirements
^^^^^^^^^^^^

Quick review of contents
^^^^^^^^^^^^^^^^^^^^^^^^

Vagrant
```````

Sample configurations
`````````````````````

Basic use
^^^^^^^^^

Local configuration file
````````````````````````

Use with Vagrant
::::::::::::::::

Run against cloud
:::::::::::::::::

Firewalling
:::::::::::

More customized use
^^^^^^^^^^^^^^^^^^^

Common customization points
```````````````````````````

Plone setup
:::::::::::

Eggs and versions
.................

Extra files/directories
.......................

Virtual hosting tricks
::::::::::::::::::::::

Multiple Plones per host
````````````````````````

Maintenance strategies (simple)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Git checkout -- simple
``````````````````````

Git branch or fork
``````````````````

What belongs to the playbook and what doesn't
`````````````````````````````````````````````

Maintenance strategies -- multiple hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The Plone Role -- using it independently
----------------------------------------


.. seealso::

   http://docs.plone.org/manage/deploying/