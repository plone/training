Exploiting Python's data model
==============================

To make our session store easy to as if it was a dictionary, we implement
out middleware by crafting a class which behaves like that. For that purpose,
we are taking a small diversion from WSGI to Python's Data Model. We enter
the realm of so called **magic methods** also known as ``__dunder__``
(which stands of duble underscore).

The first thing to know about special methods is that they are meant to be
called by the Python interpreter, and not by you. [Fluent Python, pg. 8].

Our goal is to build the following elements of a WSGI framework.

A Dictionary like Session storage
+++++++++++++++++++++++++++++++++

Using a Python session like storage we should be able to check membership
use `in`, e.g.::

    >>> 'a72e7a6b4fcf8ae611953' in session_storage

We shoud also be able to retrieve items as if was a dictionary::

    >>> session_storage['a72e7a6b4fcf8ae611953']
    {'login-date': '2017-11-09 17:13:25'}

Our goal is to create a middleware that stores information in some kind of
a persistant storage. For simplicity we start by writing this infromation
to a file on a disk, but this can easily be extended to a Redis storgae,
MongoDB or any database of your liking.
Let's assume though that session data is unstructured might look like
a dictionary of session ID as keys, with values which are another dictionary:

.. code:: python

   sessions = {
        "id1": {'data': {'k1': 'v1', 'k2': 'v2', ..., 'kn': 'vn'}},
        "id2": {'data': {'ka1': 'va1', 'ka2': 'va2', ..., 'kan': 'van'}},
        ...
       }


Requests read only attributes
+++++++++++++++++++++++++++++

A Request object is a wrapper around the environment. Some frameworks, like
Bottle, Flask and WebOb, make the attribute of a Request object read only.

The most obvious way is to use ``@property``, but this creates a very
verbose code, here is an example from `web.request.Request` (which is almost
1000 lines of code long!):

.. code:: python

    class BaseRequest(object):

         ...

         @property
         def host_url(self):
             """
             The URL through the host (no path)
             """
             e = self.environ
             scheme = e.get('wsgi.url_scheme')
             url = scheme + '://'
             host = e.get('HTTP_HOST')
             if host is not None:
                 if ':' in host and host[-1] != ']':
                     host, port = host.rsplit(':', 1)
                 else:
                     port = None
             else:
                 host = e.get('SERVER_NAME')
                 port = e.get('SERVER_PORT')
             if scheme == 'https':
                 if port == '443':
                     port = None
             elif scheme == 'http':
                 if port == '80':
                     port = None
             url += host
             if port:
                 url += ':%s' % port
             return url

We can do much better than creating methods and decorating them with
properties. Instead we craft a special container class which wrapps
the environment and allows us to access keys as if they where attributes.


     >>> req = Request(environment)
     >>> req.request_method  REQUEST_METHOD
     'GET'

Ouick access to properties
++++++++++++++++++++++++++

Sometimes accessing a property can be expensive! As can be seen in the
example above, building the host URL, we make 4 dictionary lookups, which
isn't taking much, but if we pass our Request object through 4 middlewares
each asking for this property, we already make 16 lookups. This could be
improved by calculating such properties and save the result, by using a
specially crafted decorator:

.. code:: python

   @cached_property
   def host_url(self):
       """
       This will be calucalated only once
       """
       ...
       ...
       return url

Abitility to extened
++++++++++++++++++++

If we want our framework to be public it might be a good idea to have some
kind of a plugin system. But even if our framework is intended for a use
of a small team of developers, it might be a good idea to supply some
base classes and maybe meta-classes to make sure development and extension
are easy enough, but also safe to use.
For example, suppose we want to replace our dictionary based session with
a Redis cache, but we don't want to break the API. We do this with caution,
and we think, we might want to replace Redis in some other Key-Value
storage. We domenstrate, how the use of meta classes can enforce programmers,
to obay some certain structure, with out throwing a ``RuntimeError`` or an
``AttributeError``, which in some cases might be too late.


.. code:: python

   >>> class RedisSession(BaseSession):
   ...     pass
   ...
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 7, in __new__
   ValueError: RedisSession must define a method called __setitem__

