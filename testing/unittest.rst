Unittest primer
===============


See https://docs.python.org/2.7/library/unittest.html

.. code-block:: python

    import unittest

    class SomeTest(unittest.TestCase):

        def test_a_feature(self):
            self.assertTrue(1 == 1)
            self.assertFalse(1 == 2)
            self.assertEqual(1, 1)
            self.assertNotEqual(1, 2)
            self.assertIn(1, [1])
            self.assertNotIn(1, [2])
            self.assertIn(obj.id.upper(), html_output, 'The id is not in the rendered page')


Test Classes
------------

.. code-block:: python

    class SomeTest(unittest.TestCase):

        def setUp(self):
            ...

        def tearDown(self):
            ...

        def test_something(self):
            ...


Assert Methods
--------------

msg!
    All the assert methods (except assertRaises(), assertRaisesRegexp()) accept a msg argument that, if specified, is used as the error message on failure. Use it!


assertEqual(a, b)
    a == b


assertNotEqual(a, b)
    a != b


assertTrue(x)
    bool(x) is True


assertFalse(x)
    bool(x) is False


assertIs(a, b)
    a is b


assertIsNot(a, b)
    a is not b


assertIsNone(x)
    x is None


assertIsNotNone(x)
    x is not None


assertIn(a, b)
    a in b


assertNotIn(a, b)
    a not in b


assertIsInstance(a, b)
    isinstance(a, b)


assertNotIsInstance(a, b)
    not isinstance(a, b)


assertRaises(exc, fun, *args, **kwds)
    fun(*args, **kwds) raises exc


assertRaisesRegexp(exc, r, fun, *args, **kwds)
    fun(*args, **kwds) raises exc and the message matches regex r


assertAlmostEqual(a, b)
    round(a-b, 7) == 0


assertNotAlmostEqual(a, b)
    round(a-b, 7) != 0


assertGreater(a, b)
    a > b


assertGreaterEqual(a, b)
    a >= b


assertLess(a, b)
    a < b


assertLessEqual(a, b)
    a <= b


assertRegexpMatches(s, r)
    r.search(s)


assertNotRegexpMatches(s, r)
    not r.search(s)


assertItemsEqual(a, b)
    sorted(a) == sorted(b) and works with unhashable objs


assertDictContainsSubset(a, b)
    all the key/value pairs in a exist in b



Skipping tests
--------------

@unittest.skip(reason)
    Unconditionally skip the decorated test. reason should describe why the test is being skipped.


@unittest.skipIf(condition, reason)
    Skip the decorated test if condition is true.


@unittest.skipUnless(condition, reason)
    Skip the decorated test unless condition is true.


@unittest.expectedFailure()
    Mark the test as an expected failure. If the test fails when run, the test is not counted as a failure.

