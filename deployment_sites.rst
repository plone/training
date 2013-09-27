Buildout II: Deploying your site
================================


The starzel-buildout
--------------------

If you want you can have a look at the buildout we use for our projects: https://github.com/starzel/buildout

It has some noteable features:

* It extends to files on github shared by all projects of the same version

  .. code-block:: cfg

      [buildout]
      extends =
          https://raw.github.com/starzel/buildout/4.3.2/linkto/base.cfg

* Minimal work to setup a new project

Other tools
-----------

* Fabric (manage sites)
* Chef (manage and setup servers and tools)
* Sentry (error-monitoring)
* Nagios (server-monitoring)
* jenkins (tests)
* piwik (statictics)
* gitlab (code-repo and code-review)
* redmine (ticket-system and wiki)

