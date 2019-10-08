Debugging Plone on WSGI
=======================

When debugging Plone behind a WSGI server, there are a couple of things to remember.
The ``wsgitraining.site`` package contained in our buildout comes with a debugging view that simply sets a breakpoint:

.. code-block:: python
    :emphasize-lines: 5

    class DebuggingView(BrowserView):

         def __call__(self):
             self.msg = _(u'A small message')
             import pdb; pdb.set_trace()
             return self.index()

It's available at `<http://localhost:8080/Plone/debugging-view>`_.

Debugging with waitress
-----------------------

Debugging with waitresss doesn't feel different from what you know from ZServer.
Limiting to one worker thread might make debugging easer for you.

pdbpp
Products.PdbDebugMode
plone.app.debugtoolbar
Products.enablesettrace

Debugging uWSGI
---------------

When trying to open the debugging view in uWSGI, you will see an error message in both console and the browser instead of the pdb prompt.

.. code-block:: bash

    > /home/thomas/devel/plone/wsgitraining_buildout/src/wsgitraining.site/src/wsgitraining/site/views/debugging_view.py(18)__call__()
    -> return self.index()
    (Pdb)
    ERROR:Zope.SiteErrorLog:1570455986.90912460.23307293753294422 http://localhost:8080/Plone/debugging-view
    Traceback (innermost last):
      Module ZPublisher.WSGIPublisher, line 155, in transaction_pubevents
      Module ZPublisher.WSGIPublisher, line 337, in publish_module
      Module ZPublisher.WSGIPublisher, line 255, in publish
      Module ZPublisher.mapply, line 85, in mapply
      Module ZPublisher.WSGIPublisher, line 61, in call_object
      Module wsgitraining.site.views.debugging_view, line 18, in __call__
      Module wsgitraining.site.views.debugging_view, line 18, in __call__
      Module bdb, line 88, in trace_dispatch
      Module bdb, line 113, in dispatch_line
    bdb.BdbQuit

To make uWSGI stop at the ``pdb.set_trace()`` you need to start it with the ``honour-stdin`` flag set to ``true``.
`This flag <https://uwsgi-docs.readthedocs.io/en/latest/Options.html#honour-stdin>`_ will prevent uWSGI from redirecting ``stdin`` to ``/dev/null``, which is the default behaviour.
You can do so by modifying the inline template in the ``[uwsgiini]`` part and rerun buildout.

.. code-block:: ini
    :emphasize-lines: 11,14

    ...
    [uwsgiini]
    recipe = collective.recipe.template
    input = inline:
        [uwsgi]
        http-socket = 0.0.0.0:8080
        socket = 127.0.0.1:8081
        chdir  = ${buildout:directory}/bin
        module = wsgi:application
        master = false
        honour-stdin = true
        enable-threads = true
        processes = 1
        threads = 1
    output = ${buildout:directory}/etc/uwsgi.ini
    ...

After running buildout and starting your instance with ``bin/uwsgi-instance`` you will see an interactive console and uWSGI will not serve any requests at first (the browser will hang forever instead of showing a page).

.. code-block:: bash

    *** Operational MODE: single process ***
    Class Products.CMFFormController.ControllerPythonScript.ControllerPythonScript has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    Class Products.CMFFormController.ControllerValidator.ControllerValidator has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
    /home/thomas/.buildout/eggs/cp37m/pyScss-1.3.5-py3.7-linux-x86_64.egg/scss/selector.py:54: FutureWarning: Possible nested set at position 329
      ''', re.VERBOSE | re.MULTILINE)
    WARNING:plone.behavior:Specifying 'for' in behavior 'Tiles' if no 'factory' is given has no effect and is superfluous.
    >>>

Simply press ``Ctrl+D`` to continue the instance startup:

.. code-block:: bash

    >>>
    now exiting InteractiveConsole...
    WSGI app 0 (mountpoint='') ready in 52 seconds on interpreter 0x55fe3f766d30 pid: 7018 (default app)
    *** uWSGI is running in multiple interpreter mode ***
    spawned uWSGI worker 1 (and the only) (pid: 7018, cores: 1)
    ...

Now if you open the ``debugging-view`` again you will see the ``pdb`` prompt.
All looks fine now, however you will not be able to terminate the instance with ``Ctrl+C``.
However you can press ``Ctrl+Z`` to send the instance to the background and then kill it with ``kill %1`` (or whatever job number you're seeing on the console).
This behaviour is the reason why we don't put ``honour-stdin`` in the ``.ini`` template by default.

werkzeug debugging
------------------

XXX tbd.
