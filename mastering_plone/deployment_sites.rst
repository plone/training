.. _deployment-label:

Buildout II: Getting Ready for Deployment
=========================================


.. _deployment-starzel-label:

The starzel buildout
--------------------

Have a look at the buildout some of the trainers use for their projects: https://github.com/starzel/buildout

It has some notable features:

* It extends to config- and version-files on github shared by all projects that use the same version of Plone:

  .. code-block:: cfg

      [buildout]
      extends =
          https://raw.githubusercontent.com/starzel/buildout/5.0.5/linkto/base.cfg

* It allows to update a project simply by changing the version it extends.
* It allows to update all projects of one version by changing remote files (very useful for HotFixes).
* It is minimal work to setup a new project.
* It has presets for development, testing, staging and production.
* It has all the nice development-helpers we use.

Another noteable buildout to look for inspiration:

* https://github.com/4teamwork/ftw-buildouts

.. _deployment-setup-label:

A deployment setup
------------------

Deploying Plone and production-setups are outside the scope for this training. Please see http://docs.plone.org/manage/deploying/index.html

.. _deployment-tools-label:

Other tools we use
------------------

There are plenty of tools that make developing and managing sites much easier. Here are only some of the ones you might want to check out:

* Fabric (managing sites)
* Sentry (error monitoring)
* Ansible (managing and provisioning machines)
* Greylog, ELK (logging)
* Nagios, Zabbix (server monitoring)
* jenkins, gitlab-ci, travis, drone.io (Continuous Integration)
* piwik (statistics)
* gitlab (code repo and code review)
* redmine, taiga, assembla (project-management and ticket-system)
