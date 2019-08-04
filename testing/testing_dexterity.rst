Testing a Dexterity content-type
=================================

The most common thing that we could develop in Plone are content-types. Let's see how to test if a new content-type works like expected.

Create a new content-type
-------------------------

With plonecli we could add features on our package through command-line:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add content_type

With this command, a new content-type will be automatically registered in our package and we don't need to to think about it.

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

In this test for example, we are testing that a contributor can add and delete our content-type.

.. note::
    
    plone.app.testing gives us a default user for tests. We could import its username in a variable called ``TEST_USER_ID`` and set different roles when needed.
    
    By default each test is run with that user as logged-in user. If we want to run tests as anonymous users or with a different user, we need to logout/login.


Excercise
+++++++++

Try to change the permissions for our content-type and set that only Manager can add it. Then fix the test for contributor role and create a new test for the Manager.

.. note::

    If you are developing a test case, you can run only that test with `-t` option:
    
    .. code-block:: console

        $ bin/test -t test_method_name


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
