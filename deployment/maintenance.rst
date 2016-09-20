
Maintenance strategies
^^^^^^^^^^^^^^^^^^^^^^

This section covers strategies for long-run maintenance of your playbook.
If you're successful with Plone's Ansible Playbook, you will wish to keep an eye on its continued development.
You may wish to be able to integrate bug fixes and new features that have become part of the distribution.
But, since this project targets production servers, you'll wish to be very careful in integrating those changes so that you minimize risk of breaking a live server configuration.

.. caution::

    Rule 1: If it changes, test it.

Using Ansible (or other configuration-management systems) makes it easier to test a whole server configuration.
Make use of that fact!
You may test by running your playbook against a Vagrant box or against a staging server.

Make sure your test server matches the current live configuration.
Copy backup Plone data from the live server; restore it on the test server.
Then, make your changes in the playbook (or its Ansible support) and run it against the test server.
Only on testing success should you run against the live server.

Virtualenv
``````````

If you followed our installation instructions, you have a Python virtualenv attached to your playbook checkout.
That virtualenv has its own installation of Ansible.
That's good, because it protects your playbook against unexpected changes in the global environment -- such as Ansible being updated by the OS update mechanisms.

You may need or wish to update the installation of Ansible in your Virtualenv.
If so, make sure you use the copy of ``pip`` in your virtualenv.
Then, test running your playbook with your new Ansible.

What belongs to the playbook and what doesn't
`````````````````````````````````````````````



Branches
````````

Single-host strategies
^^^^^^^^^^^^^^^^^^^^^^

Git checkout
````````````

Git branch or fork
``````````````````

Maintenance strategies -- multiple hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

