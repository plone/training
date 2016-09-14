Solr Testing
------------------------------------------------------------------------------

collective.solr comes with a few test fixtures that make it easier to test Solr.

SOLR_FIXTURE fires up and tears down a Solr instance. This fixture can be used to write unit tests for a Solr configuration.

test_solr_unit.py::

    # -*- coding: utf-8 -*-
    from collective.solr.testing import SOLR_FIXTURE
    import unittest2 as unittest
    import json
    import requests

    SOLR_BASE_URL = 'http://localhost:8090/solr/collection1'


    class TestSuggesetSolrConfig(unittest.TestCase):

        layer = SOLR_FIXTURE

        def setUp(self):
            self.clear()

        def clear(self):
            headers = {'Content-type': 'text/xml', 'charset': 'utf-8'}
            requests.post(
                SOLR_BASE_URL + "/update",
                data="<delete><select>*:*</select></delete>",
                headers=headers)
            requests.post(
                "http://localhost:8090/solr/update",
                data="<commit/>",
                headers=headers)

        def add(self, payload):
            headers = {'Content-type': 'application/json'}
            request = requests.post(
                SOLR_BASE_URL + "/update/json?commit=true",
                data=json.dumps(payload),
                headers=headers
            )
            if request.status_code != 200:
                print "FAILURE"

        def select(self, select):
            return requests.get(
                SOLR_BASE_URL + '/select?wt=json&q=%s' % select)

        def test_suggest(self):
            self.add([{
                "UID": "1",
                "Title": "Krebs",
                "SearchableText": "Krebs",
            }])
            response = self.select("Krabs")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json()['spellcheck']['suggestions'][1]['numFound'],
                1,
                "Number of found suggestions should be 1."
            )
            self.assertEqual(
                response.json()['spellcheck']['suggestions'][1]
                ['suggestion'][0]['word'],
                u'Krebs'
            )

COLLECTIVE_SOLR_FIXTURE fires up and tears down a Solr instance. In addition it activates and configures the collective.solr connection.

test_solr_integration.py::

    # -*- coding: utf-8 -*-
    from collective.solr.browser.interfaces import IThemeSpecific
    from collective.solr.testing import COLLECTIVE_SOLR_INTEGRATION_TESTING
    from collective.solr.utils import activate
    from plone.app.testing import TEST_USER_ID
    from plone.app.testing import setRoles
    from zope.component import getMultiAdapter
    from zope.interface import directlyProvides

    import json
    import unittest


    class JsonSolrTests(unittest.TestCase):

        layer = COLLECTIVE_SOLR_INTEGRATION_TESTING

        def setUp(self):
            self.portal = self.layer['portal']
            self.request = self.layer['request']
            self.app = self.layer['app']
            self.portal.REQUEST.RESPONSE.write = lambda x: x    # ignore output
            self.maintenance = \
                self.portal.unrestrictedTraverse('@@solr-maintenance')
            activate()
            self.maintenance.clear()
            self.maintenance.reindex()
            directlyProvides(self.request, IThemeSpecific)
            setRoles(self.portal, TEST_USER_ID, ['Manager'])

        def tearDown(self):
            activate(active=False)

        def afterSetUp(self):
            self.maintenance = self.portal.unrestrictedTraverse('solr-maintenance')

        def beforeTearDown(self):
            pass

        def test_search_view_returns_plone_app_search_view(self):
            view = getMultiAdapter(
                (self.portal, self.request),
                name="search"
            )
            self.assertTrue(view)

        def test_search_view_with_json_accept_header(self):
            self.request.response.setHeader('Accept', 'application/json')
            view = getMultiAdapter(
                (self.portal, self.request),
                name="search"
            )
            view = view.__of__(self.portal)
            self.assertEqual(json.loads(view())['data'], [])
