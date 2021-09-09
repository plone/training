# -*- coding: utf-8 -*-
from AccessControl.unauthorized import Unauthorized
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from plonetraining.testing.testing import PLONETRAINING_TESTING_FUNCTIONAL_TESTING
from plonetraining.testing.testing import PLONETRAINING_TESTING_INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class TestingItemIntegrationTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_testing_item_schema(self):
        fti = queryUtility(IDexterityFTI, name='TestingItem')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('TestingItem')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_testing_item_fti(self):
        fti = queryUtility(IDexterityFTI, name='TestingItem')
        self.assertTrue(fti)

    def test_ct_testing_item_factory(self):
        fti = queryUtility(IDexterityFTI, name='TestingItem')
        factory = fti.factory
        obj = createObject(factory)

    def test_ct_testing_item_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal, type='TestingItem', id='testing_item',
        )

        parent = obj.__parent__
        self.assertIn('testing_item', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('testing_item', parent.objectIds())

    def test_ct_testing_item_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='TestingItem')
        self.assertTrue(
            fti.global_allow, u'{0} is not globally addable!'.format(fti.id),
        )

    def test_ct_testing_item_contributor_cant_add(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        with self.assertRaises(Unauthorized):
            api.content.create(
                container=self.portal, type='TestingItem', id='testing_item',
            )


class TestingItemFunctionalTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {username}:{password}'.format(
                username=SITE_OWNER_NAME,
                password=SITE_OWNER_PASSWORD),
        )

    def test_add_testing_item(self):
        self.browser.open(self.portal_url + '/++add++TestingItem')
        self.browser.getControl(name='form.widgets.IBasic.title').value = 'Foo'
        self.browser.getControl('Save').click()
        self.assertTrue(
            '<h1 class="documentFirstHeading">Foo</h1>'
            in self.browser.contents
        )

        self.assertEqual('Foo', self.portal['foo'].title)

    def test_view_testing_item(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(
            type='TestingItem',
            title='Bar',
            description='This is a description',
            container=self.portal,
        )

        import transaction

        transaction.commit()

        self.browser.open(self.portal_url + '/bar')

        self.assertTrue('Bar' in self.browser.contents)
        self.assertIn('This is a description', self.browser.contents)

    def test_rich_text_field(self):
        self.browser.open(self.portal_url + '/++add++TestingItem')
        self.assertIn(
            'form.widgets.IRichTextBehavior.text', self.browser.contents,
        )
        self.browser.getControl(
            name='form.widgets.IBasic.title'
        ).value = 'A content with text'
        self.browser.getControl(
            name='form.widgets.IRichTextBehavior.text'
        ).value = 'Some text'
        self.browser.getControl('Save').click()
        self.assertIn('Some text', self.browser.contents)
