Testing a Dexterity content-type
================================

The most common thing that we could develop in Plone are content-types.
Let's see how to test if a new content-type works like expected.

Create a new content-type
-------------------------

With plonecli we could add features on our package through command-line:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add content_type

With this command, a new content-type will be automatically registered in our package and we don't need to to think about it.

Test the content-type
---------------------

If we now try to re-run tests, we could see that the tests number has increased. This is because plonecli also creates a basic test for this new content-type in ``test_ct_your_ct_name.py`` file.

Inspecting this file, we could see some interesting things:

.. code-block:: python

    from plone.app.testing import TEST_USER_ID
    from plone.app.testing import setRoles
    ...

    def test_ct_test_type_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal, type='TestType', id='test_type'
        )

        self.assertTrue(
            ITestType.providedBy(obj),
            u'ITestType not provided by {0}!'.format(obj.id),
        )

        # check that deleting the object works too
        self.assertIn('test_type', self.portal.objectIds())
        api.content.delete(obj=obj)
        self.assertNotIn('test_type', self.portal.objectIds())

In this test, for example, we are testing that a contributor can add and delete our content-type.

.. note::

    plone.app.testing gives us a default user for tests. We could import its username in a variable called ``TEST_USER_ID`` and set different roles when needed.

    By default each test is run with that user as logged-in user. If we want to run tests as anonymous users or with a different user, we need to logout/login.


Excercise
+++++++++

Try to change the permissions for our content-type and set that only Manager can add it.
Then fix the test for contributor role and create a new test for the Manager.

..  admonition:: Solution
    :class: toggle

    In ``rolemap.xml``:

    .. code-block:: xml

        <permission name="plonetraining.testing: Add TestType" acquire="True">
            <role name="Manager"/>
        </permission>

    In test case file:

    .. code-block:: python

        from AccessControl.unauthorized import Unauthorized
        ...

        def test_ct_test_type_adding(self):
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            ...

        def test_ct_test_type_adding_contributor(self):
            setRoles(self.portal, TEST_USER_ID, ['Contributor'])
            self.assertRaises(
                Unauthorized,
                api.content.create,
                container=self.portal,
                type='TestType',
                id='test_type',
            )


These are ``integration`` tests because we are not testing the browser integration.

We could try to create a ``functional`` test to test how our content-type creation works on browser.

Let's create a new test class in the same file like this:

.. code-block:: python

    from plone.testing.z2 import Browser
    from from plonetraining.testing.testing import PLONETRAINING_TESTING_FUNCTIONAL_TESTING
    ...

    class TestTypeFunctionalTest(unittest.TestCase):

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
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

        def test_add_test_type(self):
            self.browser.open(self.portal_url + '/++add++TestType')
            self.browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = "Example content"
            self.browser.getControl("Save").click()

            self.assertEqual(
                "Example content", self.portal['example-content'].title
            )

        def test_view_test_type(self):
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            self.portal.invokeFactory(
                "TestType",
                id="example-content",
                title="Example content",
                description="This is a description",
            )

            import transaction

            transaction.commit()

            self.browser.open(self.portal_url + '/example-content')

            self.assertTrue('Example content' in self.browser.contents)
            self.assertIn('This is a description', self.browser.contents)

.. note::

    self.browser.contents shows the html of the last visited page.


Excercise
+++++++++

Try to add a behavior (for example a rich text field) to our content-type and check that the field is showed up in edit form and in the view.

..  admonition:: Solution
    :class: toggle

    In ``TestType.xml`` uncomment ``plone.richtext`` behavior.

    In test case file:

    .. code-block:: python

        def test_rich_text_field(self):
            self.browser.open(self.portal_url + '/++add++TestType')
            self.assertIn(
                'form.widgets.IRichTextBehavior.text', self.browser.contents
            )
            self.browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = "A content with text"
            self.browser.getControl(
                name="form.widgets.IRichTextBehavior.text"
            ).value = "Some text"
            self.browser.getControl("Save").click()
            self.assertIn(
                'Some text', self.browser.contents
            )
