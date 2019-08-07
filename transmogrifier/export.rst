===================================
Exporting Your Current Site Content
===================================

For the sake of this training, a sample export is provided.
`Download the export <../_static/sample_export.zip>`.
The original content came from a Plone 4 site,
and was exported with collective.jsonify.

If you are using the sample export, continue with the training: `<basics>`.
Otherwise, if you need to build an export from your existing site, continue reading.
Keep in mind that this training is currently only written for handling a jsonify export.

Your current site might be Plone, Wordpress, or some other :term:`CMS`.
Some CMSs have a built-in export, an add-on for exporting content, or you may need to write your own.
While this is the first step in the process of moving your content, you will likely need to export several times throughout the process.
This will be the case if your current site is still edited regularly, or if you are writing your own custom export.

Whatever the case, it's a good idea to export your current site's full content as-is.
Then as you determine what pieces are not going to be imported, handle that with Transmogrifier.
You'll find it's better to export everything and have the information,
than to have to go back and export more.

Export from Plone
-----------------

While you could possibly migrate your Plone site in-place by updating the version number and running buildout,
there are occasionally reasons to start fresh.
This might be the case if:

* You are currently on a very old version of Plone
* Your site has been around for a while and has a bit of cruft code (makes for a fresh start)
* You are looking to drastically update your site, but need to keep a few items

You'll want to use `collective.jsonify <https://pypi.org/project/collective.jsonify>`_ for the export.
It walks through your entire Plone site, creating one JSON file for each object in the site.
It does this using an External Method, and has been tested back to Plone 2.1.
There is a way to limit what gets exported,
but you may find it better to export everything, and do the limiting on the import side.

1. Install ``collective.jsonify`` into the buildout
2. Add an `External Method <http://old.zope.org/Documentation/How-To/ExternalMethods>`_ at the root of the Management Interface (``http://[your site]/manage``) with the following properties:

   * id: ``export_content``
   * module name: ``collective.jsonify.json_methods``
   * function name: ``export_content``

3. Go to ``http://[your site]/export_content``
4. See the instance log output for where the export throws the content (it may go into /tmp)
5. Copy the numbered folders from the export into the new buildout,
   into a folder at the root called content-import and add this to your ``.gitignore``.


Export from Wordpress
---------------------

* Tools > export - exports content as a single XML
* suggestions for add-ons to export as json

  * https://wordpress.org/plugins/search/json+export
  * https://wordpress.org/plugins/all-in-one-wp-migration


Write Your Own Export
---------------------

Consistency is key.
Check out a sample ``collective.jsonify`` export to model.
You can also export to CSV.
