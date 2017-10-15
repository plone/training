Hello WSGI
==========

A WSGI application is just a callable object the responds to requests
by taking two arguments. The first one is the WSGI ``environment``
and the second is the ``start_response``.
The ``environment`` is a Python dictionary containing information about
the CGI environment.
``start_response`` is a callback which takes two inputs the response
``status`` and ``headers``. The status is astring representation like
``200 OK`` or any other HTTP status code followed by a word.
``headers`` is a list of two values tuples or possible HTTP headers.
The return value of ``start`` response is another callable which when
invoked return the body of the response.

It is the responsiblity of the WSGI server to implement this callback.
That is, the Python web application or the framework simply recieve it.

The WSGI application is invoked with the ``environment`` and
``start_response``, it may or may not use information from the
``environment``, when done it should return an iterable yielding zero
or more strings which then become the body of the response.
It may also manipulate the headers passed on to ``start_response``
before invoking it.

The following is a complete valid WSGI application:

  .. code:: python

    def hello_world_app(environ, start_response):
        status = '200 OK'  # HTTP Status
        # HTTP Headers
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)

        # The returned object is going to be printed
        return [b"Hello World"]


Running a WSGI application
--------------------------

To actually make use of the above example, you need to invoke it
with a valid WSGI server. Luckily, we don't need to fully setup a HTTP
server, because the Python standard library already has already s simple
HTTP server which implements the WSGI protocal which we can use to
test our app. To make use of it you can do:

  .. code:: python

    from wsgiref.simple_server import make_server

    def hello_world_app(environ, start_response):
        status = '200 OK'  # HTTP Status
        # HTTP Headers
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)

        # The returned object is going to be printed
        return [b"Hello World"]

    httpd = make_server('', 8000, app)
    print("Serving on port 8000...")
    # Serve until process is killed
    httpd.serve_forever()


 .. note::
   In reality, a WSGI server is usually depoloyed behing a
   full blown HTTP server, which serves as a reverse proxy for the
   WSGI server. That is, the HTTP server (for example NGinx) listen to
   HTTP or HTTPS requests on port 80 or 443 and then redirects them to
   the appropriate socket to which the WSGI server is bound to.

Excercise 1
+++++++++++

 Write your own callable class which is a valid WSGI application.

..  admonition:: Solution
    :class: toggle

    .. code-block:: python

       class HelloWSGI:

            def __call__(self, environ, start_response):
                self.start_response('200 OK', [('Content-Type', 'text/plain')])
                yield b"Hello World!\n"
