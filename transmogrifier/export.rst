===================================
Exporting Your Current Site Content
===================================

Your current site might be Plone, Wordpress, or some other :term:`CMS`.
Some CMSs have a built-in export, an add-on for exporting content, or you may need to write your own.
While this is the first step in the process of moving your content, you will likely need to export several times throughout the process.
This will be the case if your current site is still edited regularly, or if you are writing your own custom export.

Export from Plone
-----------------

While you could possibly migrate your Plone site in-place by updating the version number and running buildout, there are occasionally reasons to start fresh.
You'll want to use `collective.jsonify <https://pypi.org/project/collective.jsonify>` for the export.
It walks through your entire Plone site, creating one JSON file for each object in the site.
It does this using an External Method, and has been tested back to Plone 2.1.
There is a way to limit what gets exported,
but you may find it better to export everything, and do the limiting on the import side.

.. todo::

    add steps for external method


Export from Wordpress
---------------------

* Tools > export - exports content as a single XML
* suggestions for add-ons to export as json
  * https://wordpress.org/plugins/search/json+export
  * https://wordpress.org/plugins/all-in-one-wp-migration

Write Your Own Export
---------------------

Consistency is key.
Check out a sample jsonify export to model.
You can also export to CSV.

.. todo::

    attach a sample jsonify export