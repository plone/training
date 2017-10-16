Routing
=======

Routing is the mechanism which allows our application to call different
parts according to the requested URL.
Until now only saw applications that always give the same response to any
requested URL.

Using ``PATH_INFO``
-------------------
The requested URL contains a ``PATH_INFO`` which is passed to our WSGI
application via the ``environment`` dictionary.
We can write our application as a giant case switch to match a specific
``PATH_INFO`` to a specific behavior:


.. code:: python

    def giant_wsgi_case_app(environ, start_response):
        status = '200 OK'  # HTTP Status
        # HTTP Headers
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        # The returned object is going to be printed
        if environ['PATH_INFO'] == '/hello':
            return [b"Hello World"]
        elif environ['PATH_INFO'] == '/bye':
            return [b"Good bye"]
        elif ...
             ...
        else:
            start_response('404 Not Found', headers)
            return [b"Not found"]

This would be very un-pythonic and cumbersome to extend. Essentianly, this
problem is solved by all web framework with some kind of a routing
middleware. But before we examine how it is done by some of the most famous
WSGI frameworks, we implement a primitive routing middleware on our own.

Exercise 4
++++++++++
A small improvement would be to replace the giant ``if ... elif ... else``
with a dictionary and map a ``PATH_INFO`` to a callable. The middleware should use this mapping to call the correct WSGI callable.

..  admonition:: Solution
    :class: toggle

    .. code:: python

        def not_found(environ, start_response):
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'404 Not Found']

        def hello_world(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b"Hello World!\n"]

        def greet_user(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/plain')])
            user = environ.get('USER')
            return ["Welcome {}!\n".format(user).encode()] # response must contain bytes

        URLS = {
            "/": hello_world,
            "/greeter": greet_user,
        }

        def app(environ, start_response):
            handler = URLS.get(environ.get('PATH_INFO')) or not_found
            return handler(environ, start_response)


While this solution is pretty primitive it is understand and extend.
Essententialy, many WSGI framework have some kind of a ``Mapping``
class which is responsible for this mechanism.
For example, in Djanog one defines in ``urls.py`` a list of patters,
which are a regular expression and callable ``view``. Here is an
example from the most venerable Django polls tutorial:

.. code:: python

    from django.conf.urls import url

    from . import views

    app_name = 'polls'
    urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
        ...
        ]

The ``url`` items are then matched by django.urls.resolvers.ResolverMatch_
A similar approach is also taken by the more modern ``aiohttp`` (an
honorable reference, even though it's not a WSGI framework):

.. code:: python

    from aiohttp import web

    ...
    app = web.Application()
    app.router.add_get('/', handle)

Pyramid does this too:

.. code:: python

    with Configurator() as config:
         config.add_route('hello', '/hello/{name}')
         config.add_view(hello_world, route_name='hello')
         app = config.make_wsgi_app()

Here ``add_route`` creates an association between a ``route_name`` and
a pattern. ``add_view`` connects the callable ``hello_world`` with the route
just created.

``Flask`` and ``Bottle`` have an implicit way of adding ``route`` items to
the ``Mapping``:

.. code:: python

    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

``app.route`` adds the wrapped callable to the internal mapping inside the
``Flask`` instance. In a later part of this course, we will examine later
how this decorator works.

Working with URL parameters
---------------------------

So far, we have a simple routing middleware. But it can't work with
parameters, as seen in the Django and Pyramid examples above.
A middleware can modify the response or the environment. Modifying the latter,
we can pass new objects via the environment dictionary to the callable.

Exercise 5
++++++++++

Modify the main app matching mechanism to use regular expression groups,
to match certain URL parts as groups. These groups are the URL args,
the application can make use of. For example, calling ``/hello/`` should return
``hello wolrd!``. Calling ``/hello/frank`` should return ``/hello/frank!``.

.. code:: python

   def hello(environ, start_response):
       """Like the example above, but it uses the name specified in the URL."""
       # get the name from the url if it was specified there.
       args = environ['myapp.url_args']
       if args:
           subject = escape(args[0])
       else:
           subject = 'World'

       start_response('200 OK', [('Content-Type', 'text/html')])
       return ['''Hello {}!'''.format(subject).encode()]


..  admonition:: Solution
    :class: toggle

    .. code:: python

        urls = [
            (r'^$', index),
            (r'hello/?$', hello),
            (r'hello/(.+)/$', hello),
        ]

        def application(environ, start_response):
            path = environ.get('PATH_INFO', '').lstrip('/')
            for regex, callback in urls:
                match = re.search(regex, path)
                if match:
                    environ['myapp.url_args'] = match.groups()
                    return callback(environ, start_response)

            return not_found(environ, start_response)

.. _django.urls.resolvers.ResolverMatch: https://github.com/django/django/blob/f0ffa3f4ea277f9814285085fde20baff60fc386/django/urls/resolvers.py#L29
