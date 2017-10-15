The Web and Python
==================
In the days before the popularity of frameworks like Django, Flask
and other frameworks soared, development with Python for the web was
a bit harder for comers.

Python applications were often designed for only one of CGI,
FastCGI, mod_python or some other custom API of a specific web server.
This wide variety of choices can be a problem for new Python users,because
generally speaking, their choice of web framework limited
their choice of usable web servers, and vice versa.


WSGI
----

WSGI was created as a low-level interface between web servers and
web applications or  frameworks to promote a common ground for
portable web application development. This is similar to Java's
"servlet" API makes it possible for applications written with any
Java web application framework to run in any web server that
supports the servlet API. [pep-333]

  .. image:: ./_static/wsgi-servers.png
    :scale: 50%

As stated above, WSGI was created to ease the development of Python
web applications. The handling of the requests from browser is done
by a normal HTTP server, which routes the request to the WSGI container,
which in turn runs the WSGI application.

The following ilustration demonstartes this setup:

  .. image:: ./_static/http-server-app.png
    :scale: 50%

This setup promotes scalability and flexibility.
As a result you can mix and match any of the above mentioned servers,
with any of the WSGI framework, below. In fact, if you desire to, you
build a web application mixing parts from different WSGI frameworks.

  .. image:: ./_static/wsgi-fw.png
    :scale: 50%
