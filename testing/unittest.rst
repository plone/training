Unit tests
==========

The first test types that we are going to see, are unit tests.

They are the quickiest to run and easiest to write because they don't need special environments/configuration to be executed.

We are going to use a python unit testing library called ``unittest``.

.. note::

    More detailed documentation could be found in `unittest <https://docs.python.org/2.7/library/unittest.html>`_ documentation.

Create our first test
---------------------

First of all we need to create a new file in ``tests`` folder.

Let's call it ``test_unit.py``:

.. code-block:: python

    import unittest

    class SomeTest(unittest.TestCase):

        def test_a_feature(self):
            self.assertTrue(1 == 1)
            self.assertEqual(1, 1)

Now we need to run it:

.. code-block:: console

    $ bin/test

If we are working on a single test and we don't want to run all, we could say the testrunner which test to run:

.. code-block:: console

    $ bin/test -t test_a_feature


Excercise 1
+++++++++++

Try to create a new test and play with assertions (try also to make them fails, to see what happens and see traceback informations for debug).

Excercise 2
+++++++++++

If in your package there are some helper methods that doesn't need some CMS/Zope/Plone features but they simply transform an input into an output, you could import them and test in an unittest.

Try to create a new file into our package with a method that takes a number and returns this number doubled, and then write an unittest for this.

..  admonition:: Solution
    :class: toggle

    File ``helper_functions.py``:

    .. code-block:: python

        def double_number(x):
            return x * 2

    In ``tests/test_unit.py``:

    .. code-block:: python

        from plonetraining.testing.helper_functions import double_number

        ...

        def test_double_number(self):
            self.assertEqual(double_number(1), 2)
            self.assertEqual(double_number(2), 4)
            self.assertNotEqual(double_number(2), 3)
