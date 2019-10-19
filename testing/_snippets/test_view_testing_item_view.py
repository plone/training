# -*- coding: utf-8 -*-
from plonetraining.testing.testing import (
    PLONETRAINING_TESTING_FUNCTIONAL_TESTING,
)
from plonetraining.testing.testing import (
    PLONETRAINING_TESTING_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')
        api.content.create(self.portal, 'TestingItem', 'foo')

    def test_testing_item_view_is_registered(self):
        # original
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='testing-item-view'
        )
        # excercise 1
        view = getMultiAdapter(
            (self.portal['foo'], self.portal.REQUEST), name='testing-item-view'
        )
        self.assertTrue(view.__name__ == 'testing-item-view')
        # self.assertTrue(
        #     'Sample View' in view(),
        #     'Sample View is not found in testing-item-view'
        # )

    def test_testing_item_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='testing-item-view',
            )
            # exercise 1
            getMultiAdapter(
                (self.portal['other-folder'], self.portal.REQUEST),
                name='testing-item-view',
            )

    def test_testing_item_view_show_text(self):
        view = api.content.get_view(
            name='testing-item-view',
            context=self.portal['foo'],
            request=self.request,
        )
        self.assertIn('A small message', view())

    def test_testing_custom_msg_without_parameter(self):
        view = api.content.get_view(
            name='testing-item-view',
            context=self.portal['foo'],
            request=self.request,
        )
        self.assertEqual('', view.custom_msg())

    def test_testing_custom_msg_with_parameter(self):
        view = api.content.get_view(
            name='testing-item-view',
            context=self.portal['foo'],
            request=self.request,
        )
        self.request.form['message'] = 'hello'
        self.assertEqual('hello', view.custom_msg())


from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from transaction import commit


class ViewsFunctionalTest(unittest.TestCase):

    layer = PLONETRAINING_TESTING_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'TestingItem', 'foo')
        # needed to "see" this content in the browser
        commit()

        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {username}:{password}'.format(
                username=SITE_OWNER_NAME,
                password=SITE_OWNER_PASSWORD),
        )

    def test_view_without_parameter(self):
        self.browser.open(self.portal_url + '/foo')
        self.assertNotIn(
            '<p>This is the default message: A small message</p>',
            self.browser.contents,
        )
        # because it's not the default view
        self.browser.open(self.portal_url + '/foo/testing-item-view')
        self.assertIn(
            '<p>This is the default message: A small message</p>',
            self.browser.contents,
        )
        self.assertNotIn(
            'This is the custom message',
            self.browser.contents,
        )

    def test_view_with_parameter(self):
        self.browser.open(self.portal_url + '/foo?message=hello')
        self.assertNotIn(
            '<p>This is the default message: A small message</p>',
            self.browser.contents,
        )
        self.assertNotIn(
            'This is the custom message',
            self.browser.contents,
        )
        # because it's not the default view
        self.browser.open(self.portal_url + '/foo/testing-item-view?message=hello')
        self.assertIn(
            '<p>This is the default message: A small message</p>',
            self.browser.contents,
        )
        self.assertIn(
            '<p>This is the custom message: hello</p>',
            self.browser.contents,
        )
