Summary
=======

The amalgamation of the ideas we showed here can be demonstrated by the
nano-framework ``Chick``:

.. code:: python

    class Chick:

        """
        A WSGI Application framework with API inspired by Bottle and Flask.

        There is No HTTPRequest Object and No HTTPResponse object.

        Just barebone routing ...
        """

        routes = {}

        def __call__(self, environ, start_response):
            try:
                callback, method = self.routes.get(environ.get('PATH_INFO'))
            except TypeError:
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return [b'404 Not Found']

            if method != environ.get('REQUEST_METHOD'):
                start_response('405 Method Not Allowed',
                               [('Content-Type', 'text/plain')])
                return [b'404 Method Not Allowed']

            start_response('200 OK', [('Content-Type', 'text/plain')])
            return callback(environ)

        def add_route(self, path, wrapped, method):
            self.routes[path] = (wrapped, method)

        def get(self, path):
            def decorator(wrapped):
                self.add_route(path, wrapped, 'GET')
                return wrapped

            return decorator

        def post(self, path):
            def decorator(wrapped):
                self.add_route(path, wrapped, 'POST')
                return wrapped

            return decorator


    class CapitalizeResponse(object):

        def __init__(self, app):
            self.app = app
            self.visits = 0  # state keeping made easier

        def __call__(self, environ, start_response, *args, **kw):
            self.visits += 1
            response = self.app(environ, start_response)
            response.append(("You visited " + str(self.visits) +
                             " times").encode())
            return [line.decode().upper().encode()
                    for line in response]


    chick = Chick()


    @chick.get("/")
    def index(environ):
        return [b"Hello World!\n"]


    @chick.post("/input/")
    def test_post(environ):

        r = ''.join(('{} {}\n'. format(k, v) for k, v
                     in environ.items())).encode()
       return [r]


    capital_chick = CapitalizeResponse(chick)

    if __name__ == "__main__":
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8000, capital_chick)
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
