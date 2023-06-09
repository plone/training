---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Debugging Plone on WSGI

When debugging Plone behind a WSGI server, there are a couple of things to remember.
The `wsgitraining.site` package contained in our buildout comes with a debugging view that sets a breakpoint:

```{code-block} python
:emphasize-lines: 5

class DebuggingView(BrowserView):

     def __call__(self):
         self.msg = _(u'A small message')
         import pdb; pdb.set_trace()
         return self.index()
```

It is available at [http://localhost:8080/Plone/debugging-view](http://localhost:8080/Plone/debugging-view).

It also provides a very basic view that raises an `AttributeError` available at [http://localhost:8080/Plone/attribute-error-view](http://localhost:8080/Plone/attribute-error-view).

## Debugging with waitress

Debugging with waitresss doesn't feel different from what you know from ZServer.
Limiting to one worker thread might make debugging easer for you.

The widely used `pdbpp`, `Products.PdbDebugMode`, `plone.app.debugtoolbar` and `Products.enablesettrace` add-ons also work as expected.

## werkzeug debugging

````{sidebar} Build now
Run buildout for this section:

```shell
buildout -c werkzeugdebugger.cfg
```
````

The werkzeug WSGI server provides an additional [debugging WSGI middleware](https://werkzeug.palletsprojects.com/en/latest/debug/) that renders tracebacks and also provides an interactive debug console.
To quote from this [blog post](https://labs.detectify.com/2015/10/02/how-patreon-got-hacked-publicly-exposed-werkzeug-debugger/) this is basically remote remote code execution by design, so never use the werkzeug debugger in production (although the original vulnerability has been mitigated by introducing a debugger PIN).

To get this working for Plone we first have to disable our standard exception views.
We can do this by means of an additional option in the `[instance]` buildout part:

```{code-block} ini
:emphasize-lines: 9

...
[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
zeo-client = on
zeo-address = 8100
shared-blob = on
blob-storage = ${buildout:directory}/var/blobstorage
debug-exceptions = on
eggs =
    Plone
    Pillow
    wsgitraining.site
    dataflake.wsgi.werkzeug
wsgi-ini-template = ${buildout:directory}/templates/werkzeugdebugger.ini.in
```

We also have to specify the correct entry point in the `ini` template to use the werkzeug debugger:

```{code-block} ini
:emphasize-lines: 2

[server:main]
use = egg:dataflake.wsgi.werkzeug#debugger
hostname = 127.0.0.1
port = 8080
...
```

Start the instance with `bin/instance fg`.
Use the `attribute-error-view` from the training add-on to see a traceback rendered by werkzeug debugger.
If you move the mouse to the right of a stack frame, you will see a symbol of a terminal.
Click on it.
You will be prompted for a PIN once.
Enter the PIN provided on the console where you started the instance.
You will see an interactive console in the browser where you can enter arbitrary Python code.

## Debugging uWSGI

When trying to open the debugging view in uWSGI, you will see an error message in both console and the browser instead of the pdb prompt.

```shell
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
```

To make uWSGI stop at the `pdb.set_trace()` you need to start it with the `honour-stdin` flag set to `true`.
[This flag](https://uwsgi-docs.readthedocs.io/en/latest/Options.html#honour-stdin) will prevent uWSGI from redirecting `stdin` to `/dev/null`, which is the default behaviour.
You can do so by modifying the inline template in the `[uwsgiini]` part and rerun buildout.

```{code-block} ini
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
```

After running buildout and starting your instance with `bin/uwsgi-instance` you will see an interactive console and uWSGI will not serve any requests at first (the browser will hang forever instead of showing a page).

```console
*** Operational MODE: single process ***
Class Products.CMFFormController.ControllerPythonScript.ControllerPythonScript has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
Class Products.CMFFormController.ControllerValidator.ControllerValidator has a security declaration for nonexistent method 'ZPythonScriptHTML_changePrefs'
/home/thomas/.buildout/eggs/cp37m/pyScss-1.3.5-py3.7-linux-x86_64.egg/scss/selector.py:54: FutureWarning: Possible nested set at position 329
  ''', re.VERBOSE | re.MULTILINE)
WARNING:plone.behavior:Specifying 'for' in behavior 'Tiles' if no 'factory' is given has no effect and is superfluous.
>>>
```

Press `Ctrl+D` to continue the instance startup:

```console
>>>
now exiting InteractiveConsole...
WSGI app 0 (mountpoint='') ready in 52 seconds on interpreter 0x55fe3f766d30 pid: 7018 (default app)
*** uWSGI is running in multiple interpreter mode ***
spawned uWSGI worker 1 (and the only) (pid: 7018, cores: 1)
...
```

Now if you open the `debugging-view` again you will see the `pdb` prompt.
All looks fine now, however you will not be able to terminate the instance with `Ctrl+C`.
Instead you can press `Ctrl+Z` to send the instance to the background and then kill it with `kill %1` (or whatever job number you're seeing on the console).
This behaviour is the reason why we don't put `honour-stdin` in the `.ini` template by default.
