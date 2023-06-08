---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Useful Add-ons and Utilities

## Sentry

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c sentry.cfg
```
````

[Sentry](https://sentry.io/welcome/) is a widely used open source monitoring and error tracking tool.
The existing Zope integration in the legacy [raven](https://pypi.org/project/raven/) package does not work in the WSGI pipeline.
This is because its component definition depends on logging components that are only available through `zopeschema.xml` but not `wsgischema.xml`.
`zopeschema.xml` has been moved from the core Zope package to ZServer.

The more recent [Sentry SDK](https://github.com/getsentry/sentry-python) however integrates with the standard Python logging infrastructure.
To create Sentry events corresponding to log file entries, [initialize the SDK](https://docs.sentry.io/platforms/python/guides/logging/).
This is realized in a PasteDeploy filter factory implemented by `plone.recipe.zope2instance`.
We can also configure the logging levels for Sentry events and breadcrumbs, respectively, and pass a list of loggers for which we do not want to forward messages to Sentry.

`collective.sentry` offers more advanced options that you might or might not need in your project.

## haufe.requestmonitoring

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c longrequests.cfg
```
````

`haufe.requestmonitoring` is a Zope add-on that allows you to monitor long running requests.
It will log tracebacks of requests that take longer than a configured threshold in order to allow you to find out where Zope spends the time.
You can also use it to log request durations for all requests or to log successful and failing requests.
`haufe.requestmonitoring` uses `zope.components` event machinery and, more specifically, the `IPubStart`, `IPubSuccess` and `IPubFailure` events to determine relevant information.
This information is not WSGI specific but the Publisher creates these event signals.
