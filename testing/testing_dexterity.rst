Testing a Dexterity content-type
================================

The most common thing that we could develop in Plone are content-types.
Let's see how to test if a new content-type works like expected.

Create a new content-type
-------------------------

With plonecli we could add features on our package through command-line.

For example, let's create a new ``TestingItem`` content-type:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add content_type



With this command, plonecli will ask you some questions and will register new content-type in our package.

.. note::

    To follow this training, you need to ask questions like this:
    - Content type name (Allowed: _ a-z A-Z and whitespace) [Todo Task]: TestingItem

    - Content type description:

    - Use XML Model [y]: n

    - Dexterity base class (Container/Item) [Container]: Item

    - Should the content type globally addable? [y]: y

    - Create a content type class [y]: y

    - Activate default behaviors? [y]: y


Test the content-type
---------------------

If we now try to re-run tests, we could see that the tests number has increased.
This is because plonecli also creates a basic test for this new content-type in ``tests/test_ct_testing_item.py`` file:

.. code-block:: python
    
    ...

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
                container=self.portal,
                type='TestingItem',
                id='testing_item',
            )
            parent = obj.__parent__
            self.assertIn('testing_item', parent.objectIds())

            # check that deleting the object works too
            api.content.delete(obj=obj)
            self.assertNotIn('testing_item', parent.objectIds())

We can see some interesting things:

- We are using ``PLONETRAINING_TESTING_INTEGRATION_TESTING`` layer, because we don't need to write functional tests
- We are using ``setUp`` method to set some variables and add some roles to the testing user.


In these tests, we are testing some very basic stuffs for our content-type like for example if it's correctly registered in FTI, if we can create it
and if an user with a specific role (Contributor) can add it.

.. note::

    plone.app.testing gives us a default user for tests. We could import its username in a variable called ``TEST_USER_ID`` and set different roles when needed.

    By default each test is run with that user as logged-in user. If we want to run tests as anonymous users or with a different user, we need to logout/login.


Excercise 1
+++++++++++

- Change the permissions for our newly content-type and only allow Manager to add it.
- Fix old tests.
- Create a new one to test that Contributor can't add these types. 

..  admonition:: Solution
    :class: toggle

    In ``rolemap.xml``:

    .. code-block:: xml

        <permission name="plonetraining.testing: Add TestingItem" acquire="True">
            <role name="Manager"/>
        </permission>

    In test case file:

    .. code-block:: python

        from AccessControl.unauthorized import Unauthorized
        ...

        def test_ct_testing_item_adding_contributor_cant(self):
            setRoles(self.portal, TEST_USER_ID, ['Contributor'])
            with self.assertRaises(Unauthorized):
                api.content.create(
                    container=self.portal, type='TestingItem', id='testing_item'
                )

Functional test
---------------

Until now we wrote only ``ìntegration`` tests because we didn't needed to test browser integration or commit some transactions.

As previously said, if we don't need to create a functional test, it's better to avoid them because they are slower than integration ones.

.. note::

    It's always better avoiding transactions in tests because they invalidate the isolation between tests in the same test case.
    
    If we commit a transaction in one test, we persist that write into our testing database, and our changes are visible also in following tests in the same test case.

We could try to create a ``functional`` test just to see how they works and to test how our content-type creation works on browser.

Let's create a new test case in the same file like this:

.. code-block:: python

    from plone.testing.z2 import Browser
    from from plonetraining.testing.testing import PLONETRAINING_TESTING_FUNCTIONAL_TESTING
    from plone.app.testing import SITE_OWNER_NAME
    from plone.app.testing import SITE_OWNER_PASSWORD
    ...

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
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
            )

        def test_add_testing_item(self):
            self.browser.open(self.portal_url + '/++add++TestingItem')
            self.browser.getControl(name="form.widgets.IBasic.title").value = "Foo"
            self.browser.getControl("Save").click()
            self.assertIn(
                '<h1 class="documentFirstHeading">Foo</h1>',
                self.browser.contents
            )

            self.assertEqual("Foo", self.portal['foo'].title)

        def test_view_testing_item(self):
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            api.content.create(
                type="TestingItem",
                title="Bar",
                description="This is a description",
                container=self.portal,
            )

            import transaction

            transaction.commit()

            self.browser.open(self.portal_url + '/bar')

            self.assertTrue('Bar' in self.browser.contents)
            self.assertIn('This is a description', self.browser.contents)


The first thing that we can see, is the new layer used: ``PLONETRAINING_TESTING_FUNCTIONAL_TESTING``.

In ``setUp`` we configure the test case to use the Zope web browser and we login as site owner.

In ``test_add_testing_item`` we simulate user interaction on creating a new content from the browser:

- We open the url for adding a new TestingItem content
- We found the title field and compile it
- We click to Save button
- We check that after saving it, we can see its title.

In ``test_view_testing_item`` we check that accessing directly to a content with his url, we can see some informations.

.. note::

    self.browser.contents shows the html of the last visited page.


Excercise
+++++++++

Try to add a behavior (for example a rich text field) to our content-type and check that the field is showed up in edit form and in the view.

..  admonition:: Solution
    :class: toggle

    In ``TestingItem.xml`` uncomment ``plone.richtext`` behavior.

    In test case file:

    .. code-block:: python

        def test_rich_text_field(self):
            self.browser.open(self.portal_url + '/++add++TestingItem')
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
