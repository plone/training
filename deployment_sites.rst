.. _deployment-label:

Buildout II: Getting Ready for Deployment
=========================================


.. _deployment-starzel-label:

The starzel buildout
--------------------

Have a look at the buildout we use for our projects: https://github.com/starzel/buildout

It has some notable features:

* It extends to files on github shared by all projects of the same version

  .. code-block:: cfg

      [buildout]
      extends =
          https://raw.githubusercontent.com/starzel/buildout/5.0b2/linkto/base.cfg

* Minimal work to setup a new project
* Presets for development, testing, staging and production

.. _deployment-setup-label:

A deployment setup
------------------

* zeoserver and zeoclients
* haproxy
* nagios
* varnish
* monitoring
* supervisor
* backup
* logrotate
* precompiler
* cronjobs


.. _deployment-tools-label:

Other tools we use
------------------

* Fabric (manage sites)
* Sentry (error monitoring)
* Ansible (manage and setup servers and tools)
* Nagios (server monitoring)
* jenkins (tests)
* piwik (statistics)
* gitlab (code repo and code review)
* redmine (ticket system and wiki)
