---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Maintenance Strategies

```{note} About
This section covers strategies for long-run maintenance of your playbook.
```

If you're successful with Plone's Ansible Playbook, you will wish to keep an eye on its continued development.
You may wish to be able to integrate bug fixes and new features that have become part of the distribution.

But, since this project targets production servers, you'll wish to be careful in integrating those changes so that you minimize risk of breaking a live server configuration.

```{caution}
Rule 1: If it changes, test it.
```

Using Ansible (or other configuration-management systems) makes it easier to test a whole server configuration.
Make use of that fact!
You may test by running your playbook against a Vagrant box or against a staging server.

Make sure your test server matches the current live configuration.
Copy backup Plone data from the live server; restore it on the test server.
Then, make your changes in the playbook (or its Ansible support) and run it against the test server.
Only on testing success should you run against the live server.

## Virtualenv

If you followed our installation instructions, you have a Python virtualenv attached to your playbook checkout.
That virtualenv has its own installation of Ansible.
That's good, because it protects your playbook against unexpected changes in the global environment -- such as Ansible being updated by the OS update mechanisms.

You may need or wish to update the installation of Ansible in your virtualenv.
If so, make sure you use the copy of {program}`pip` in your virtualenv.
Then, test running your playbook with your new Ansible.

## What Belongs To The playbook And What Doesn't

The general strategy for playbook changes is to not modify anything that's included with the playbook.
We've gone to some trouble to make sure that you can make most foreseeable setup changes without touching distribution files.

The {file}`local-configure.yml` is an example of this strategy.
It is **not** included with the distribution files.
It never will be.
We will also never include an {file}`inventory.cfg` file.

That means that you may safely merge changes from the STABLE branch of <https://github.com/plone/ansible-playbook> without fear of overwriting those files.
You may also create new playbooks; just give them different names.
The extra playbooks might handle installs of extra components, firewalling, user setup, whatever.

## Git Forks

But, what if you want to use version control with your own added files?

In this case, you will wish to *fork* <https://github.com/plone/ansible-playbook>.
Add your extra files to those included with your local checkout of the git fork and push upstream to your git repository.

Then, occasionally merge changes from the Plone GitHub account's repository into your fork, typically by rebasing from Plone's upstream repository STABLE branch.
Make sure you keep your added files when you do so.

## Maintenance Strategies -- Multiple Hosts

The {file}`local-configure.yml` file strategy makes it easy to get going with Plone's playbook fast.

But it breaks down if you wish to maintain multiple, different hosts with the playbook.
Fortunately, there's an easy way to handle the problem.

Create a {file}`host_vars` directory inside your playbook directory (the one containing playbook.yml).
Now, inside that directory, create one file per target host, each with a name that matches the inventory entry for the host, plus `.yml`.

Each of these files should be the same as the local-configure.yml file that would be used if this was a single host.
Delete the no-longer-needed {file}`local-configure.yml` file.
