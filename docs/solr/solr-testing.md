---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Solr Testing

`collective.solr` comes with a few test fixtures that make it easier to test Solr.

`SOLR_FIXTURE` fires up and tears down a Solr instance.
This fixture can be used to write unit tests for a Solr configuration.

Usually you need the `COLLECTIVE_SOLR_FIXTURE` which spins off a Solr instance and installs `collective.solr`.

A custom test layer based on this fixture looks like this

```python
class PlonetrainingSolrExampleLayer(PloneSandboxLayer):

    defaultBases = (COLLECTIVE_SOLR_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plonetraining.solr_example)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetraining.solr_example:default')
```

A test for our suggest method in our fancy search looks like this

```python
# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plonetraining.solr_example.browser.views import FancySearchView
from plonetraining.solr_example.testing import PLONETRAINING_SOLR_EXAMPLE_FUNCTIONAL_TESTING  # noqa
from collective.solr.testing import activateAndReindex
import unittest


class TestSearchView(unittest.TestCase):
    """Test that plonetraining.solr_example is properly installed."""

    layer = PLONETRAINING_SOLR_EXAMPLE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ('Manager', ))
        api.content.create(self.portal, 'Document', title='Lorem Ipsum')
        activateAndReindex(self.portal)

    def test_suggest(self):
        """Test if plonetraining.solr_example is installed."""
        request = self.layer['request']
        view = FancySearchView(self.portal, request)
        request.form['SearchableText'] = 'lore'
        self.assertEqual(
            view.suggest(),
            {'url': 'http://nohost?term=lore&SearchableText=lorem', 'word': u'lorem'}
        )
```

Note the **activateAndReindex** method.

It is a nice testing helper to cleat the Solr index and reindex all objects again.
If testing Solr it is advisable to call it at the test setup.
Otherwise the documents created during the tests would pile up in the index.

## Exercise

Write a custom test for a Solr feature used in Plone.
