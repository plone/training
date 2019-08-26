Testing a view
==============

Now let's test a view.

Create a new view
-----------------

Create a new view:

.. code-block:: console

  $ cd plonetraining.testing
  $ plonecli add view

With this command, a new view will be automatically registered in our package and we don't need to to think about it.

Test the view
-------------

Like for dexterity types, also for views ``plonecli`` created some basic tests (in ``test_view_training_view.py`` file).


Inspecting this file, we could see some interesting things:

.. code-block:: python

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_training_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='training-view'
        )
        self.assertTrue(view.__name__ == 'training-view')

    def test_training_view_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='training-view'
            )

If we also see the view registration in ``views/configure.zcml`` we could see the it is registestered only for objects that implements ``IFolderish`` interface.
That's the reason why `test_training_view_not_matching_interface` tests that invoking that view on a Document, an Exception will be raised.

With a view we could test several things:

- If it is available only for a certain type of objects
- If it renders like we expected (calling the view in an Integration test, or using the browser in a Functional test)
- If its methods returns what we expects (calling methods directly from the view instance)

Excercise 1
+++++++++++

The view template prints a string that is returned from its class. Write a test that checks this thing.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python

        def test_training_view_print_message(self):
            view = getMultiAdapter(
                (self.portal['other-folder'], self.portal.REQUEST),
                name='training-view'
            )
            self.assertIn('A small message', view())

Excercise 2
+++++++++++

- Add a method in the view that checks a parameter from the request (message) and returns the union between the static message and the given message.
- Update the template to print the value from that method.
- Test that calling the method from the view, it returns what we expect
- Write a Functional test to test browser integration

..  admonition:: Solution
    :class: toggle

    First of all we need to implement that method in view:

    .. code-block:: python

        def print_msg(self):
            message = self.request.form.get('message', '')
            return '{}: {}'.format(self.msg, message)

    .. code-block:: python

        def test_training_view_print_message(self):
            view = getMultiAdapter(
                (self.portal['other-folder'], self.portal.REQUEST),
                name='training-view'
            )
            self.assertIn('A small message', view())
