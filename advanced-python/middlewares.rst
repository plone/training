Middlewares
===========

A middleware is an object that wrapps the original application,
hence the name.
A middle is called between the application and the server.
It can modify the response or the environment or route requests to
different application objects.

  .. image:: ./_static/middlewares2.png
    :scale: 90%

Middlewares and apps are agnostic to each other,
so we can plumb any WSGI app to our middleware,
and our middleware to any WSGI app. Middleware can be chained,
allowing our response or request to go through mulitple
phases of processing.

Here is for example how the Django web framework chains multiple middlewares
before calling the application:

.. code:: shell

        $ django-admin startproject example
        $ grep -c2 -ni  middleware example/example/settings.py
        grep  -i middleware example/example/settings.py
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',

Django imports these middlewares from the their
specified module and plumbs them one after another. Let's see how
we can do that too.

Other frameworks use ``extentions`` sometimes also called ``plugins`` or
``includes``. For example, the Flask framework really wraps the
``Application`` instance:

.. code:: python

        """
        Example how flask uses 3 middlewares each wrapping around the
        application
        """
        from flask import Flask
        from flask.ext.sqlalchemy import SQLAlchemy
        from flask.ext.bcrypt import Bcrypt
        from flask.ext.login import LoginManager

        app = Flask(__name__)
        bcrypt = Bcrypt(app)
        login_manager = LoginManager()
        login_manager.init_app(app)
        db = SQLAlchemy(app)

``Bottle.py`` has a similar approach:

.. code:: python

        import bottle
        from bottle.ext import sqlite
        app = bottle.Bottle()
        plugin = sqlite.Plugin(dbfile='/tmp/test.db')
        app.install(plugin)

        @app.route('/show/:item')
        def show(item, db):
            row = db.execute('SELECT * from items where name=?', item).fetchone()
            if row:
               return template('showitem', page=row)
            return HTTPError(404, "Page not found")

Bottle hides the fact the the ``app.install`` command is wrapping your
application with a call plugin which takes place before your application
and after your application login. These action could be for example opening
and closing connections to the database before and after the request if
needed.

A Simple WSGI Middleware
------------------------

As an example we show a simple WSGI middle which logs the
environment dictionary to the console:

.. code-block:: python

    def log_environ(handler):
        """print the envrionment dictionary to the console"""
        from pprint import pprint
        def _inner(environ, start_function):
            pprint(environ)
            return handler(environ, start_function)

        return _inner

        # this will show "Hello World!" in your browser,
        # and the environment in the console
        app = log_environ(hello_world_app)

Excercise 2
+++++++++++

Implement your own middleware which capitalizes the response you original
application return.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python

       def capitalize_response(handler):
           """dumb middleware the assumes response is a list of
              strings which can be capitlized"""

           def _inner(environ, start_response):
               response = handler(environ, start_response)
               return [line.decode().upper().encode() for line in response]

           return _inner

       def handler(environ, start_function):
           start_function('200 OK', [('Content-Type', 'text/plain')])
           return [b"Hello World!\n"]

       # this will return HELLO WORLD
       app = capitalize_response(handler)


Excercise 3
+++++++++++

Implement your own middleware which reverses the response. Upon calling this
middleware twice you should see the original response, e.g.:

.. code:: python

   def reverser(wsgiapp):
       ...
       ...

   app = reverser(reverser(app)) # should return Hello WSGI!

..  admonition:: Solution
    :class: toggle

    .. code-block:: python

        def reverser(handler):

            def _inner(environ, start_response):
                response = handler(environ, start_response)
                new_response = [x[::-1] for x in response]
                print(new_response)
                return new_response

            return _inner

        def app(environ, start_function):
            start_function('200 OK', [('Content-Type', 'text/plain')])
            return [b"Hello World!\n"]

        # this will return Hello World
        app = reverser(reverser(app))

