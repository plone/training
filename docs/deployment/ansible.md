---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Intro To Ansible

[Ansible](https://www.ansible.com/) is an open-source configuration management, provisioning and application deployment platform
written in Python and using [YAML](https://yaml.org/about.html) (YAML Ain't Markup Language) as a configuration language.

Ansible makes its connections from your computer to the target machine using SSH.

The one server site requirement is an SSH server.
General familiarity with SSH is desirable if you're using Ansible -- as well as being a baseline skill for server administration.

## Installation

Ansible is installed on the orchestrating computer -- typically your desktop or laptop.
It is a large Python application (though a fraction the size of Plone!) that needs specific Python packages from the Python Package Index (PyPI).

That makes Ansible a strong candidate for a Python {program}`virtualenv` installation
If you don't have {program}`virtualenv` installed on your computer, do it now.

{program}`virtualenv` may be installed via an OS package manager, or on a Linux or BSD machine with the command:

```shell-session
sudo easy_install-2.7 virtualenv
```

Once you've got {program}`virtualenv`, use it to create a working directory containing a virtual Python:

```shell-session
virtualenv ansible_work
```

Then, install Ansible there:

```shell-session
cd ansible_work
bin/pip install ansible
```

Now, to use Ansible, activate that Python environment.

```shell-session
source bin/activate
ansible
```

```{note}
Trainers: check to make sure everyone understands the basic `source activate` mechanism.
```

Now, let's get a copy of the *Plone Ansible Playbook*.
Make sure you're logged in to your `ansible_work` directory.

Unless you're participating in the development of the playbook, or need a particular fix, you'll want to check out the `STABLE` branch.

The `STABLE` branch is a pointer to the last release of the playbook.

```shell-session
git clone -b STABLE --single-branch https://github.com/plone/ansible-playbook.git
```

Or,

```shell-session
git clone https://github.com/plone/ansible-playbook.git
cd ansible-playbook
git checkout STABLE
```

That gives you the Plone Ansible Playbook.
You'll also need to install a few Ansible roles.
Roles are Ansible playbooks packaged for distribution.
You may pick up everything with a single command.

```shell-session
cd ansible-playbook
ansible-galaxy install -p roles -r requirements.yml
```

If you forget that command, it's in the short README.rst file in the playbook.

```{note}
The rationale for checking the Plone Ansible Playbook out inside the virtualenv directory is that it ties the two together.
Months from now, you'll know that you can use the playbook with the Python and Ansible packages in the virtualenv directory.

We check out the playbook as a subdirectory of the virtualenv directory so that we can search our playbooks and roles
without having to search the whole virtualenv set of packages.
```

## Ansible Basics

### Connecting To Remote Machines

To use Ansible to provision a remote server, we have two requirements:

1. We must be able to connect to the remote machine using {command}`ssh`; and,
2. We must be able to issue commands on the remote server as root (superuser) via {command}`sudo`.

You'll need to familiarize yourself with how to fulfill these requirements on the cloud/virtual environment of your choice.
Examples:

Using Vagrant/VirtualBox

> You will initially be able to log in as the "vagrant" user using a private key that's in a file created by Vagrant.
> The user "vagrant" may issue {command}`sudo` commands with no additional password.

Using Linode

> You'll set a root password when you create your new machine.
> If you're willing to use the root user directly, you will not need a {command}`sudo` password.

When setting up a Digital Ocean machine

> New machines are typically created with a root account that contains your ssh public key as an authorized key.

AWS

> AWS EC2 instances are typically created with a an account named "root" or a short name for the OS, like "ubuntu", that contains your ssh public key as an authorized key.
> Passwordless {command}`sudo` is pre-enabled for that account.

The most important thing is that you know your setup.
Test that knowledge by trying an ssh login and issuing a superuser command.

```shell-session
ssh myuser@myhost.com   # (what user/hostname did you use? are you asked a password?)
...
myhost.com $ sudo ls  # (are you asked for your password?)
```

### Inventories

Ansible runs on a local computer, and it acts on one or more remote machines.
We tell Ansible how to connect to remote machines by maintaining a text inventory file.

There is a sample inventory configuration file in your distribution.
It's meant for use with a Vagrant-style VirtualBox.

```shell-session
cat vbox.cfg
```

```none
myhost ansible_port=2222 ansible_host=127.0.0.1 ansible_user=vagrant ansible_private_key_file=~/.vagrant.d/insecure_private_key
```

This inventory file is complicated by the fact that a VirtualBox typically has no DNS host name and uses a non-standard port and a special SSH key file.
Because of this we have to specify all those things.

If we were using a DNS-known hostname and our standard ssh key files, it could be much simpler:

```none
direct.newhost.com ansible_ssh_user=root
```

Ansible inventory files may list multiple hosts and may have aliases for groups of hosts. See <https://docs.ansible.com> for details.

## Playbooks

We're going to cover just enough on Ansible playbooks to allow you to read and customize Plone's playbook.
[Ansible's documentation](https://docs.ansible.com) is excellent if you want to learn more.

In Ansible, an individual instruction for the setup of the remote server is called a \_task\_.
Here's a task that makes sure a directory exists.

% code-block: yaml
%
% - name: Ensure base directory
%   file:
%     path=/usr/local/plone
%     state=directory
%     mode=0755

This uses the Ansible `file` module to check to see if a directory exists with the designated mode.
If it doesn't, it's created.

Tasks may also have execution conditions expressed in Python syntax and may iterate over simple data structures.

In addition to tasks, Ansible's basic units are *host* and *variable* specifications.

An Ansible *playbook* is a specification of tasks that are executed for specified hosts and variables.
All of these specifications are in YAML.

### Quick Intro To YAML

YAML isn't a markup language, and it isn't a programming language either.
It's a data-specification notation like JSON.

Except that YAML -- very much unlike JSON -- is meant to be written and read by humans.
The creators of YAML call it a "human friendly data serialization standard".

```{note}
YAML is actually a superset of JSON.
Every JSON file is also a valid YAML file.

But if we fed JSON to the YAML parser, we'd be missing the point of YAML, which is human readability.
```

Basic types available in YAML include strings, booleans, floating-point numbers, integers, dates, times and date-times.
Structured types are sequences (lists) and mappings (dictionaries).

Sequences are indicated by list-member lines with leading dashes:

```yaml
- item one
- item two
- item three
```

Mappings are indicated with key/value pairs with colons separating keys and values:

```yaml
one: item one
two: item two
three: item three
```

Complex data structures are designated with indentation:

```yaml
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
```

Basic types read as you'd expect:

```yaml
- one  # string "one"
- 1    # integer 1
- 1.0  # float 1.0
- True # boolean True
- true # also boolean True
- yes  # also boolean True
```

Finally, remember that this is a superset of JSON:

```yaml
- {a: one, b: two}   # mapping
- [one, two, three]  # sequence
```

Want to turn YAML into Python data structures?
Or Python into YAML?

Python has several YAML parser/generators.
The most commonly used is PyYAML.

Quick code to read YAML from the standard input and turn it into pretty-printed Python data:

```{literalinclude} read_yaml.py
:language: python
```

### Quick Intro To Jinja2

YAML doesn't have any built-in way to read a variable.
Ansible uses the Jinja2 templating language for this purpose.

A quick example: Let's say we have a variable `timezone` containing the target server's desired timezone setting.
We can use that variable in a task via Jinja2's double-brace notation: `{{ timezone }}`.

Jinja2 also supports limited Python expression syntax and can read object properties or mapping key/values with a dot notation:

```
{{ instance_config.plone_version < '5.0' }}
```

There are also various filters and tests available via a pipe notation.
For example, we use the `default` filter to supply a default value if a variable is undefined.

```yaml
- name: Set timezone variables
  tags: timezone
  copy: content={{ timezone|default("UTC\n") }}
        dest=/etc/timezone
        owner=root
        group=root
        mode=0644
        backup=yes
```

Jinja2 also is used as a full templating language whenever we need to treat a text file as a template to fill in variable values or execute loops or branching logic.

Here's an example from the template used to construct a buildout.cfg:

```none
zcml =
{% if instance_config.plone_zcml_slugs %}
{% for slug in instance_config.plone_zcml_slugs %}
    {{ slug }}
{% endfor %}
{% endif %}
```

## Playbook Structure

An Ansible "play" is a mapping (or dictionary) with keys for hosts, variables and tasks.
A playbook is a sequence of such dictionaries.

A simple playbook:

```yaml
- hosts: all
  vars:
    ... a dictionary of variables
  tasks:
    ... a sequence of tasks
```

The value of hosts could be a single host name, the name of a group of hosts, or "all".

### Variables

### Notifications And Handlers

We may also specify "handlers" that are run if needed.

```yaml
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
```

Handlers are run if a matching notification is registered.
A particular handler is only run once, even if several notifications for it are registered.

### Roles

Ansible has various ways to include the contents of YAML files into your playbook.
"Roles" do it in a more structured way -- much more like a package.

Roles contain their own variables, tasks and handlers.
They inherit the global variable environment and you may pass particular variables when they are called.

Plone's Ansible Playbook includes several roles for chores such as setting up the load balancer and web server.

Other roles are fetched (the role source itself is fetched) by `ansible-galaxy` when we use it to set up requirements.
Most are fetched from GitHub.

An simple Ansible playbook using roles:

```yaml
- hosts: all
  vars:
    ... a dictionary of variables
  pre-tasks:
    ... tasks executed before roles are used.
  roles:
    ... a sequence of role invocation mappings like:
    - role: haproxy
      var1: value1
      var2: value2
      when: install_loadbalancer|default(True)
    ...
  tasks:
    ... other tasks, executed after the roles
  handlers:
    ... handlers for our own tasks; roles usually have their own
```

If we want to pass variables to roles, we add their keys and values to the mapping.

Take a look at the `when: install_loadbalancer|default(True)` line above.
A `when` key in a role or task mapping sets a condition for execution.
For conditionals like `when`, Ansible expects a Jinja2 expression.

We could also have expressed that `when` condition as `"{{ install_loadbalancer|default(True) }}"`.
Ansible interprets all literal strings as little Jinja2 templates.
