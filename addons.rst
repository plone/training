Extend Plone with Add-ons
=========================

There are more than a thousand addons for Plone. We will cover only a handful today.

How to find addons
------------------

* https://pypi.python.org/pypi - use the search form!
* http://plone.org/products
* https://github.com/collective >1000 repos
* https://github.com/plone >240 repos
* http://news.gmane.org/gmane.comp.web.zope.plone.user
* Addon shortlist (will come 2014)
* google
* ask


Installing Addons
-----------------

Installation is a two-step process.

First, we must make the addons code available to Zope. This means, that Zope can import the code. buildout is responsible for this.

Use ``vagrant ssh`` to ssh to your vagrant, and change the buildout.cfg file in /vagrant/training.

In the section ``[instance]`` there is a variable called ``eggs``, which has multiple *eggs* as a value. Add the following eggs:

* ``Products.PloneFormGen``
* ``Products.LinguaPlone``
* ``collective.plonetruegallery``
* ``plone.app.themeeditor``


Usually, one enters the eggs by adding one more line per egg into the configuration.
You must write the egg name indented, this way Buildout understands that the current line is part of the last variable and not a new variable.

.. sourcecode:: bash

    $ bin/buildout
    $ bin/instance fg

Now the code is importable from within Plone and everything got registered via ZCML.
But your Plone-site has not yet been told to use this. For this, you have to install the addons in your Plone Site.

In your browser, go the control panel ``@@plone_control_panel``, and open the ``Addons`` Panel. You will see that you can install all three packages there.

Install them now.

This is what happens: The GenericSetup profile of the product gets loaded. This does things like:

* configuring new actions,
* registering new content types or
* creating some content/configuration objects in your Plone site.

Let' have a look at what we just installed.


PloneFormGen
------------

Creating forms in Plone:

* pure: html and python in a view
* framework: z3c.form, formlib, deform
* ttw: Products.PloneFormGen

Registration-form:

* Add a object of the new type 'Form Folder' in the site-root. Call it "Registration"
* Save and view the result
* Click in QuickEdit
* Remove field "Subject"
* Add fields for food-preference and shirt-size
* Add a DataSave Adapter


Internationalisation
--------------------

We're not doing this with the demo-site.

We would use http://pypi.python.org/pypi/plone.app.multilingual since we use Dexterity for our Content Types.

* Install
* ``/@@language-controlpanel``
* ``/@@language-setup-folders``
* best practices



Add 'bling' with collective.plonetruegallery
--------------------------------------------

collective.plonetruegallery is a role model on how to write a Plone Extension.

Instead of creating custom content types for Galleries, it integrates with the Plone functionality to choose different views for folderish content types.

https://pypi.python.org/pypi/collective.plonetruegallery


Customizing the design with plone.app.themeeditor
-------------------------------------------------

* Installation
* explain UI
* change Logo (download http://www.sixfeetup.com/blog/2011PloneConfLogo.gif - the brazil-logo is to big)
* change Footer (footer.pt):

  .. code-block:: html

      <p>&copy; 2013 by me! |
         Phone: +31 26 44 22 700 |
        <a href="mailto:info@ploneconf.org">
         Contact us
        </a>
      </p>

* Look at ``ploneCustom.css``. Recognize the changes we did before?:
* Add some more css to make our site a little responsive

  .. code-block:: css

      @media only screen and (max-width: 980px) {
          #visual-portal-wrapper {
              position: relative;
              width: auto;
          }
      }

      @media only screen and (max-width: 768px) {
          #portal-columns > div {
              width: 97.75%;
              margin-left: -98.875%;
              clear: both;
          }

          .searchButton,
          .searchSection {
              display: none;
          }
      }



export customizations
---------------------

* export the customizations as an egg (``ploneconf.theme``)


inspect the package
--------------------

* what is where?
* jbot, static etc.


We are now able to change the design of our wesite. We can install extensions and create simple actions.

But:

* Can we submit talks now?
* Can we create lists with the most important properties of each tasks?
* Can we allow Visitors to vote on talks?

We often have to work with structured data. Up to a degree we can do all this TTW, but at some point we reach barriers. In the second part of our Training, we will teach you, how to break these barriers.
