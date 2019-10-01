===========================
Useful Addons and Utilities
===========================

Sentry
======

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c sentry.cfg

`Sentry <https://sentry.io>`_ is a widely used open source monitoring and error tracking tool.
The existing Zope integration in the legacy `ravem <https://pypi.python.org/project/raven>`_ package does not work in the WSGI pipeline.
This is because it's component definition depends on logging components that are only available through zopeschema.xml but not wsgischema.xml.
zopeschema.xml has been moved from the core Zope package to ZServer.

The more recent `Sentry SDK <https://github.com/getsentry/sentry-python>`_ however integrates with the standard Python logging infrastructure.
All we need to do to create sentry events corresponding to log file entries is to `initialize the SDK <https://docs.sentry.io/platforms/python/logging>`_.
This is realized in a PasteDeploy filter factory implemented by plone.recipe.zope2instance.
We can also configure the logging levels for sentry events and breadcrumbs, respectively, and pass a list of loggers for which we do not want to forward messages to Sentry.

`collective.sentry` offers more advanced options that you might or might not need in your project.

haufe.requestmonitoring
=======================

.. sidebar:: Build now

    Run buildout for this section:

    ..  code-block:: bash

        buildout -c longrequests.cfg

haufe.requestmonitoring is a Zope addon that allows you to monitor long running requests.
It will log tracebacks of requests that take longer than a configured threshold in order to allow you to find out where Zope spends the time.
You can also use it to simply log request durations for all requests or to log successful and failing requests.
haufe.requestmonitoring uses zope.components event machinery and more specifically the IPubStart, IPubSuccess and IPubFailure events to determine relevant information.
This information is not WSGI specific but the Publisher creates these event signals.
