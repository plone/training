1. Introduction (10 Minutes)
============================

Who are we?
-----------

We introduce each other

* Patrick Gerken, do3cc, patrick@starzel.de
* Philip Bauer, pbauer, bauer@starzel.de
* Starzel.de (http://www.starzel.de)
* Munich User Group

Who are you?
------------

Please introduce yourselves:

* name, company, country...
* What is your Plone experience?
* What is your web-development experience?
* What is your motivation to go to this tutorial?
* What are your expectations for this tutorial?
* Do you know the html of the output of this?::

    <div class="hiddenStructure"
         tal:repeat="num python:range(1, 10, 5)"
         tal:content="structure num"
         tal:omit-tag="">
      This is some weird sh*t!
    </div>

  The answer is::

    1 6

* Do you know what the following would return?::

    [(i.Title, i.getURL()) for i in context.getFolderContents()]

* What is your favorite editor?


What will we do?
----------------

Technologies and tools we use during the training

* git
* github
* virtualbox
* vagrant
* ubuntu linux
* TTW (a lot!)
* buildout
* TAL
* METAL
* zcml
* grok
* python
* dexterity
* viewlets
* jquery

What we will not do?
--------------------

We will not cover the following topics:

* archetypes (http://developer.plone.org/content/archetypes/index.html)
* portlets
* genericsetup
* z3c.form
* caching
* hosting
* Diazo
* Theming
* tests
* deco and tiles
* image-scales
* i18n and locales



What to expect
--------------

You won't be a plone-programmer after these 2 days. You will know some of the more powerfull features of Plone and should be able to construct a website on your own using these tools. You should also be able to find out where to look for instructions to do tasks we did not cover. You will know most of the core-technologies involved in plone-programming.

If you want to become a plone-developer or plone-integrator you should definitvely read Martins book and re-read it again. Most importantly you should practice your skills and not stop here but go forward!

If you want to stay on the ttw-side of things you could read "Practical Plone" (http://www.packtpub.com/practical-plone-3-beginners-guide-to-building-powerful-websites/book).


Other
-----

* Breaks
* Food, Restrooms
* Questions
* WIFI: fairtraderocks
