
11. Views II: A default view for "talk" (45min) (Patrick)
=========================================================

 * zcml
 * grok
 * View-Classes
 * Python-Klasse mit Grok dazu (Patrick)

Der View ist eine Zope Toolkit Komponente. Er besteht aus einer Klasse, in die wir View Logik packen, und meistens einem Template, welches Daten anzeigt. Klassischer Weise hat man den View mit ZCML registriert, wir haben heutzutage aber auch Grok zur Verfügung, was uns die Arbeit erleichert. Traditionell legt man einen Ordner browser an, in den man die Views packt. View anlegen.


View Classes
------------

Views are Multi Adapters! Thats all there is to know.
Yesterday we created a view, lets have a look at it again!

* ZCML
* python
* page template

The template does a lot of things. We are going to ignore some of them.

For a normal browser view, you don't really need allowed_interface, you don't need the implements statement in code and you don't need the translation features provided by the _ method.

There is something else, much much more important. You can see the __init__ method, don't do anything fancy in there.

The way zope looks for the right view, your __init__ code block gets executed, before any permission checks have been applied. Also, because of the history of zope, a number of exceptions that you can trigger in your browser view, will result in the error message 404, page not found, without any way of giving you a traceback to tell you, what might have gone wrong.

This code has some property getters. Everybody knows what that means?

Property getters have a small problem, I avoid them nowadays. They provide shitty tracebacks because a traceback in the getter is hidden.

The init method gets two objects. That is always the case with a browser view. Did I mention that views are multiadapters? Adapters and multiadapters get always called with the objects, in case of a view, it always adapts a browser request and a content object, so this if why you get them here.

The request can be used to change the content type, if you return files. We are not going to do this here or today.

The context gives you access to the current object. If you modify objects, you always do this in the browser view. The context is also used to get tools, like the catalog.

If you have a special view that modifies content, you can do that in the __call__ method. I suggest you try to get information from the request about the data that has been submitted, and based on that you dispatch different methods you create. These methods would then handle the data manipulation.

Be aware that the __call__ method is special. Whatever the call method returns, gets displayed. The default implementation will render the associated page template. So to make sure that some html gets rendered, always call super(self, XXX).__call__(self) and return that value.

I mentioned yesterday, what zcml is and that there is an alternative way to create browser views.

Lets do this now, lets create a second and a third view as a grok view.
blablabla
So, when to use grok and when to use zcml?
You add a dependency with grok, so it is uncommon to use grok in reusable components yet.

