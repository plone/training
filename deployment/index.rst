===========================
Automating Plone Deployment
===========================

.. warning::

   This chapter is still work in progress!

.. .. toctree::
..    :maxdepth: 3
..    :numbered: 1

Intro to Plone Stack
--------------------

.. figure:: full_stack.png
    :align: center

    Caption for full stack

.. figure:: stack-components.png
    :align: center

    Caption for stack components

Intro to Ansible
----------------

Installation
^^^^^^^^^^^^

Quick commands
^^^^^^^^^^^^^^

Playbooks
^^^^^^^^^

Quick intro to YAML
```````````````````

Inventories
```````````

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