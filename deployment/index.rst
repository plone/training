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

If you haven't read the first couple of chapters of `Guide to deploying and installing Plone in production <http://docs.plone.org/manage/deploying/index.html>`_, take a moment to do so. You'll want to be familiar with the main components of a typical Plone install for deployment and know when each is vital and when unnecessary.

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

Ansible is usually installed on the orchestrating computer -- typically your desktop or laptop.
It is a large Python application (though a fraction the size of Plone!) that needs many specific Python packages from the Python Package Index (PyPI).

That makes Ansible a strong candidate for a Python ``virtualenv`` installation
If you don't have virtualenv installed on your computer, do it now.

``virtualenv`` may be installed via an OS package manager, or on a Linux or BSD machine with the command:

.. code-block:: bash

    sudo easy_install-2.7 virtualenv

Once you've got ``virtualenv``, use it to create a working directory containing a virtual Python:

.. code-block:: bash

    virtualenv ansible_work

Then, install Ansible there:

.. code-block:: bash

    cd ansible_work
    bin/pip install ansible

Now, to use Ansible, activate that Python environment.

.. code-block:: bash

    source bin/activate
    ansible

.. note::

    Trainers: check to make sure everyone understands the basic ``source activate`` mechanism.

Now, let's get a copy of the *Plone Ansible Playbook*.
Make sure you're logged to your ansible_work directory.

Unless you're participating in the development of the playbook, or need a particular fix, you'll want to clone the ``STABLE`` branch.
The STABLE branch is a pointer to the last release of the playbook.

.. code-block:: bash

    git clone -b STABLE --single-branch https://github.com/plone/ansible-playbook.git

Or,

.. code-block:: bash

    git clone https://github.com/plone/ansible-playbook.git
    cd ansible-playbook
    git checkout STABLE

That gives you the Plone Ansible Playbook.
You'll also need to install a few Ansible roles.
Roles are Ansible playbooks packaged for distribution.
Fortunately, you may pick up everything with a single command.

.. code-block:: bash

    cd ansible-playbook
    ansible-galaxy install -p roles -r requirements.yml

If you forget that command, it's in the short README.rst file in the playbook.

.. note::

The rationale for checking the Plone Ansible Playbook out inside the virtualenv directory is that it ties the two together.
Months from now, you'll know that you can use the playbook with the Python and Ansible packages in the virtualenv directory.
We check out the playbook as a subdirectory of the virtualenv directory so that we can search our playbooks and roles without having to search the whole virtualenv set of packages.

Ansible basics
^^^^^^^^^^^^^^

Connecting to remote machines
`````````````````````````````

To use Ansible to provision a remote server, we have two requirements:

1. We must be able to connect to the remote machine using ``ssh``; and,

2. We must be able to issue commands as the on the remote server as root (superuser), usually via ``sudo``.

You'll need to familiarize yourself with how to fulfill these requirements on the cloud/virtual environment of your choice.
Examples:

Using Vagrant/virtualbox

    You will initially be able to log in as the "vagrant" user using a private key that's in a file created by Vagrant.
    The user "vagrant" may issue ``sudo`` commands with no additional password.

Using Linode

    You'll set a root password when you create your new machine. If you're willing to use the root user directly, you will not need a ``sudo`` password.

When setting up a Digital Ocean machine

    New machines are typically created with a root account that contains your ssh public key as an authorized key.


AWS

    AWS EC2 instances are typically created with a an account named "root" or a short name for the OS, like "ubuntu", that contains your ssh public key as an authorized key.
    Passwordless ``sudo`` is pre-enabled for that acount.

The most important thing is that you know your setup. Test that knowledge by trying an ssh login and issuing a superuser command.


.. code-block:: bash

    ssh myuser@myhost.com   # (what user/hostname did you use? are you asked a password?)
    ...
    myhost.com $ sudo ls  # (are you asked for your password?)

Inventories
```````````

Ansible is usually run on a local computer, and it usually acts on one or more remote machines.
We tell Ansible how to connect to remote machines by maintaining a text inventory file.

There is a sample inventory configuration file in your distribution.
It's meant for use with a Vagrant-style virtualbox.

.. code-block:: bash

    cat vbox.cfg

.. code-block:: ini

    myhost ansible_ssh_port=2222 ansible_ssh_host=127.0.0.1 ansible_ssh_user=vagrant ansible_ssh_private_key_file=~/.vagrant.d/insecure_private_key

This inventory file is complicated by the fact that a virtualbox typically has no DNS host name and uses a non-standard port and a special SSH key file.
So, we have to specify all those things.

If we were using a DNS-known hostname and our standard ssh key files, it could be much simpler:

.. code-block:: ini

    direct.newhost.com ansible_ssh_user=root

Ansible inventory files may list multiple hosts and may have aliases for groups of hosts. See docs.ansible.com for details.

You may run Ansible against one, two, all of the hosts in the inventory file, or against alias groups like "plone-servers".

Smoke test
``````````

Create or pick a remote machine to which you have adequate access.
Create an inventory.cfg file and an entry for the new host.

Now, let's see if we can use Ansible to connect to the remote machine that we've specified in our inventory.

Does the new machine allow an ssh key login, then you ought to be able to use the command:

.. code-block:: bash

    ansible -i inventory.cfg myhost -a "whoami"

If you need a password for login, try:

.. code-block:: bash

    ansible -i inventory.cfg myhost -a "whoami" -k

And, if that fails, ask for verbose feedback from Ansible:

.. code-block:: bash

    ansible -i inventory.cfg myhost -a "whoami" -k -vvvv

Now, let's test our ability to become superuser on the remote machine.
If you have passwordless sudo, this should work:

.. code-block:: bash

    ansible -i inventory.cfg myhost -a "whoami" -k --become
    # omit the "-k" if you need no login password.

If sudo requires a password, try:

.. code-block:: bash

    ansible -i inventory.cfg myhost -a "whoami" -k --become -K
    # again,  omit the "-k" if you need no login password.

If all that works, congratulations, you're ready to use Ansible to provision the remote machine.

.. note::

    The "become" flag tells Ansible to carry out the action while becoming another user on the remote machine.
    If no user is specified, we become the superuser.
    If no method is specified, it's done via ``sudo``.

    You won't often use the ``--become`` flag because the playbooks that need it specify it themselves.

Playbooks
^^^^^^^^^

In Ansible, an individual instruction for the setup of the remote server is called a task.
Here's a task that makes sure a directory exists.

.. code-block: yaml

    - name: Ensure base directory
      file:
        path=/usr/local/plone
        state=directory
        mode=0755

This uses the Ansible ``file`` module to check to see if a directory exists with the designated mode.
If it doesn't, it's created.

Tasks may also have execution conditions expressed in Python syntax and may iterate over simple data structures.

In addition to tasks, Ansible's basic units are host and variable specifications.

An Ansible ``playbook`` is a specification of tasks that are executed for specified hosts and variables.
All of these specifications are in YAML.

Quick intro to YAML
```````````````````

YAML isn't a markup language, and it isn't a programming language either.
It's a data-specification notation.
Just like JSON.
Except that YAML -- very much unlike JSON -- is meant to be written and read by humans.
The creators of YAML call it a "human friendly data serialization standard".

.. note::

    YAML is actually a superset of JSON.
    Every JSON file is also a valid YAML file.
    But if we just fed JSON to the YAML parser, we'd be missing the point of YAML, which is human readability.

Basic types available in YAML include strings, booleans, floating-point numbers, integers, dates, times and date-times.
Structured types are sequences (lists) and mappings (dictionaries).

Sequences are indicated by list-member lines with leading dashes:

.. code-block:: yaml

    - item one
    - item two
    - item three

Mappings are indicated with key/value pairs with colons separating keys and values:

.. code-block:: yaml

    one: item one
    two: item two
    three: item three

Complex data structures are designated with indentation:

.. code-block:: yaml

    # a mapping of sequences
    american:
      - Boston Red Sox
      - Detroit Tigers
      - New York Yankees
    national:
      - New York Mets
      - Chicago Cubs
      - Atlanta Braves

    # a sequence of mappings
    -
      name: Mark McGwire
      hr:   65
      avg:  0.278
    -
      name: Sammy Sosa
      hr:   63
      avg:  0.288

Basic types read as you'd expect:

.. code-block:: yaml

    - one  # string "one"
    - 1    # integer 1
    - 1.0  # float 1.0
    - True # boolean True
    - true # also boolean True
    - yes  # also boolean True

Finally, remember that this is a superset of JSON:

.. code-block:: yaml

    - {a: one, b: two}   # mapping
    - [one, two, three]  # sequence

Want to turn YAML into Python data structures?
Or Python into YAML?
Python has several YAML parser/generators.
The most commonly used is PyYAML.

Quick code to read YAML from the standard input and turn it into pretty-printed Python data:

.. literalinclude:: read_yaml.py
   :language: python

Quick intro to Jinja2
`````````````````````

YAML doesn't have any built-in way to read a variable.
Ansible uses the Jinja2 templating language for this purpose.

A quick example: Let's say we have a variable ``timezone`` containing the target server's desired timezone setting.
We can use that variable in a task via Jinja2's double-brace notation: ``{{ timezone }}``.

Jinja2 also supports limited Python expression syntax and can read object properties or mapping key/vaues with a dot notation::


    {{ instance_config.plone_version < '5.0' }}

There are also various filters and tests available via a pipe notation.
For example, we use the ``default`` filter to supply a default value if a variable is undefined.

.. codeblock:: yaml

    - name: Set timezone variables
      tags: timezone
      copy: content={{ timezone|default("UTC\n") }}
            dest=/etc/timezone
            owner=root
            group=root
            mode=0644
            backup=yes

Jinja2 also is used as a full templating language whenever we need to treat a text file as a template to fill in variable values or execute loops or branching logic.
Here's an example from the template used to construct a buildout.cfg::

    zcml =
    {% if instance_config.plone_zcml_slugs %}
    {% for slug in instance_config.plone_zcml_slugs %}
        {{ slug }}
    {% endfor %}
    {% endif %}


Playbook structure
``````````````````

An Ansible "play" is a mapping (or dictionary) with keys for hosts, variables and tasks.
A playbook is a sequence of such dictionaries.

A simple playbook:

.. codeblock:: yaml

    - hosts: all
      vars:
        ... a dictionary of variables
      tasks:
        ... a sequence of tasks

The value of hosts could be a single host name, the name of a group of hosts, or "all".

Variables
:::::::::

Tasks -- pre, main, post
::::::::::::::::::::::::

Notifications and handlers
::::::::::::::::::::::::::

We may also specify "handlers" that are run if needed.

.. codeblock:: yaml

    - hosts: all
      vars:
        ... a dictionary of variables
      tasks:
        - name: Change webserver setup
          ...
          notify: restart webserver
        ...
      handlers:
        - name: restart webserver
          service: webserver
          state: restarted

Handlers are run if a matching notification is registered.
A particular handler is only run once, even if several notifications for it are registered.

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