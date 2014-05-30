Buildout II: Getting ready for deployment
=========================================


The starzel-buildout
--------------------

Have a look at the buildout we use for our projects: https://github.com/starzel/buildout

It has some noteable features:

* It extends to files on github shared by all projects of the same version

  .. code-block:: cfg

      [buildout]
      extends =
          https://raw.github.com/starzel/buildout/4.3.3/linkto/base.cfg

* Minimal work to setup a new project
* Presets for development, testing, staging and production

A deployment-setup
------------------

* zeoserver and zeoclients
* haproxy
* nagios
* marnish
* monitoring
* supervisor
* backup
* logrotate
* precompiler
* cronjobs


Other tools we use
------------------

* Fabric (manage sites)
* Sentry (error-monitoring)
* Ansible (manage and setup servers and tools)
* Nagios (server-monitoring)
* jenkins (tests)
* piwik (statictics)
* gitlab (code-repo and code-review)
* redmine (ticket-system and wiki)
