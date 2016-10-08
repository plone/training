Through-The-Web development
===========================

It is possible to include Javascript functionality without the need to know about any of the tools involved.
This is not reccommended for when you need to do a complex and modular implementation.


portal_javascript & portal_css
++++++++++++++++++++++++++++++

These two portal tools are no longer used in Plone 5.
They are still present, but nothing should be included in them.


Resource Registries
+++++++++++++++++++

This is the new tool included in Plone 5.
From here we will manage everything related to Javascript and CSS resources.
It can be found right at the bottom of Plone's Control Panel, in the :guilabel:`Advanced` section.

.. figure:: _static/resource_registry.png
   :align: center


Add files
---------

We are going to include 2 new resources, a Javascript file, and a LESS file.

The Javascript will look like this:

.. code-block:: js

    $( document ).ready(function() {
        var links = $('a');
        links.addClass('custom-background');
    });

The LESS will look like this:

.. code-block:: css

    a.custom-background{
        background-color: #F7E1CF;
        color: black;
    }


* Go to the :guilabel:`Overrides` tab
* Click the :guilabel:`Add file` button
* Name the new file :file:`++plone++static/custom-links.js`
* Paste the contents of the Javascript section into the textarea
* Click :guilabel:`Save`
* Click the :guilabel:`Add file` button again
* Name the new file :file:`++plone++static/custom-links.less`
* Paste the contents of the CSS section into the textarea
* Click :guilabel:`Save`


Create the resource
-------------------

* Go to the :guilabel:`Registry` tab
* Click the :guilabel:`Add resource` button
* Name it ``training-custom-links``
* Under ``JS`` enter ``++plone++static/custom-links.js``
* For the :guilabel:`CSS/LESS` section, click :guilabel:`Add`
* Enter :file:`++plone++static/custom-links.less`

It should look somthing like this:

.. figure:: _static/add_resource.png
   :align: center

* Click :guilabel:`Save`


Create the bundle and wire everything up
----------------------------------------

* Go to the :guilabel:`Registry` tab
* Click the :guilabel:`Add bundle` button
* Name it ``training-custom-bundle``
* Under :guilabel:`Resources` enter ``training-custom-links``
* For the :guilabel:`Depends` section, we'll use ``plone``
* Make sure :guilabel:`Enabled` is checked

It should look somthing like this:

.. figure:: _static/add_bundle.png
   :align: center

* Click :guilabel:`Save`


Build the bundle
----------------

In order for changes to be included, you need to build your bundle.
For doing this, you just need to click the :guilabel:`Build` under the bundle you want to build.
