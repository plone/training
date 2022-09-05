---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Exporting Your Current Site Content

For the sake of this training, a sample export is provided.
Download the {download}`sample_export.zip <../_static/sample_export.zip>`.
The original content came from a Plone 4 site,
and was exported with collective.jsonify.

If you are using the sample export, continue with the training: {doc}`basics`.
Otherwise, if you need to build an export from your existing site, continue reading.
Keep in mind that this training is currently only written for handling a jsonify export.

Your current site might be Plone, Wordpress, or some other {term}`CMS`.
Some CMSs have a built-in export, an add-on for exporting content, or you may need to write your own.
While this is the first step in the process of moving your content, you will likely need to export several times throughout the process.
This will be the case if your current site is still edited regularly, or if you are writing your own custom export.

Whatever the case, it's a good idea to export your current site's full content as-is.
Then as you determine what pieces are not going to be imported, handle that with Transmogrifier.
You'll find it's better to export everything and have the information,
than to have to go back and export more.

## Export from Plone

While you could possibly migrate your Plone site in-place by updating the version number and running buildout,
there are occasionally reasons to start fresh.
This might be the case if:

- You are migrating from Python 2 to Python 3 (Plone 5.2+)
- You are currently on a very old version of Plone
- Your site has been around for a while and has a bit of cruft code (makes for a fresh start)
- You are looking to drastically update your site, but need to keep a few items

You'll want to use [collective.jsonify](https://pypi.org/project/collective.jsonify) for the export.
It walks through your entire Plone site, creating one JSON file for each object in the site.
It does this using an External Method, and has been tested back to Plone 2.1.
There is a way to limit what gets exported,
but you may find it better to export everything, and do the limiting on the import side.

1. Install `collective.jsonify` into the buildout

2. Add an [External Method](https://old.zope.dev/Documentation/How-To/ExternalMethods) at the root of the Management Interface (`http://[your site]/manage`) with the following properties:

   - id: `export_content`
   - module name: `collective.jsonify.json_methods`
   - function name: `export_content`

3. Go to `http://[your site]/export_content`

4. See the instance log output for where the export throws the content (it may go into /tmp)

5. Copy the numbered folders from the export into the new buildout,
   into a folder at the root called content-import and add this to your `.gitignore`.

## Export from Wordpress

There is currently not an easy way to migrate Wordpress data in to Plone,
but here are some starting points:

- {menuselection}`Tools > export` - exports content as a single XML

- suggestions for add-ons to export as json

  - <https://wordpress.org/plugins/search/json+export>
  - <https://wordpress.org/plugins/all-in-one-wp-migration>

## Write Your Own Export

Consistency is key. Determine what data and metadata is needed to be kept in the new site,
and include that in your export. Here is a simple example:

```json
{
    "_type": "Document",
    "title": "Award Survey",
    "text": "<h1>Quoniam, si dis placet, ab Epicuro loqui discimus.</h1>\n\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; An hoc usque quaque, aliter in vita? Id enim natura desiderat. Tamen a proposito, inquam, aberramus. Ne discipulum abducam, times."
    "modified": "2018/10/02 11:03:43.251170 GMT-4",
    "_path": "/mysite/award",
    "_id": "Award"
}
```

And here is a sample JSON export from a Plone site.
It contains lots of information,
and you can determine in the import what should be kept.

```json
{
    "contributors": [],
    "_content_type_text": "text/html",
    "text": "<h1>Quoniam, si dis placet, ab Epicuro loqui discimus.</h1>\n\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ille enim occurrentia nescio quae comminiscebatur; An hoc usque quaque, aliter in vita? Id enim natura desiderat. Tamen a proposito, inquam, aberramus. Ne discipulum abducam, times. Quis istum dolorem timet? </p>\n\n<pre>\nMe ipsum esse dicerem, inquam, nisi mihi viderer habere bene\ncognitam voluptatem et satis firme conceptam animo atque\ncomprehensam.\n\nQuid affers, cur Thorius, cur Caius Postumius, cur omnium\nhorum magister, Orata, non iucundissime vixerit?\n</pre>\n\n\n<h2>Duo Reges: constructio interrete.</h2>\n\n<p>Sic enim censent, oportunitatis esse beate vivere. Nihil illinc huc pervenit. <code>At miser, si in flagitiosa et vitiosa vita afflueret voluptatibus.</code> Inde igitur, inquit, ordiendum est. </p>\n\n<ol>\n\t<li>Sed finge non solum callidum eum, qui aliquid improbe faciat, verum etiam praepotentem, ut M.</li>\n\t<li>Quam tu ponis in verbis, ego positam in re putabam.</li>\n\t<li>Potius inflammat, ut coercendi magis quam dedocendi esse videantur.</li>\n\t<li>Conferam tecum, quam cuique verso rem subicias;</li>\n\t<li>Sed nimis multa.</li>\n</ol>\n\n\n<ul>\n\t<li>Zenonis est, inquam, hoc Stoici.</li>\n\t<li>Sed emolumenta communia esse dicuntur, recte autem facta et peccata non habentur communia.</li>\n\t<li>Aliud est enim po\u00ebtarum more verba fundere, aliud ea, quae dicas, ratione et arte distinguere.</li>\n\t<li>Te enim iudicem aequum puto, modo quae dicat ille bene noris.</li>\n\t<li>Comprehensum, quod cognitum non habet?</li>\n</ul>\n\n\n<p><code>Idemne, quod iucunde?</code> Que Manilium, ab iisque M. Si quidem, inquit, tollerem, sed relinquo. Iam enim adesse poterit. Ratio quidem vestra sic cogit. Quis est tam dissimile homini. <a href='http://loripsum.net/' target='_blank'>Quonam modo?</a> Tamen a proposito, inquam, aberramus. </p>\n\n<dl>\n\t<dt><dfn>Haec dicuntur fortasse ieiunius;</dfn></dt>\n\t<dd>Ita fit ut, quanta differentia est in principiis naturalibus, tanta sit in finibus bonorum malorumque dissimilitudo.</dd>\n\t<dt><dfn>Itaque fecimus.</dfn></dt>\n\t<dd>Sin te auctoritas commovebat, nobisne omnibus et Platoni ipsi nescio quem illum anteponebas?</dd>\n</dl>\n\n\n",
    "creation_date": "2018/10/26 13:44:45.371553 GMT-4",
    "imageCaption": "Porta vitae quis pharetra dui felis eni class pretium.",
    "expirationDate": "None",
    "_content_type_id": "text/plain",
    "id": "purus-felis-aliquam-egestas-lectus-ante-velit-laoreet.",
    "subject": [],
    "modification_date": "2018/10/26 13:44:45.796026 GMT-4",
    "title": "Purus felis aliquam egestas lectus ante velit laoreet.",
    "_ac_local_roles": {
        "admin": [
            "Owner"
        ]
    },
    "_content_type_language": "text/plain",
    "_defaultpage": "",
    "location": "Netus dolor.",
    "_content_type_title": "text/plain",
    "excludeFromNav": true,
    "_atbrefs": {},
    "_content_type_imageCaption": "text/plain",
    "_type": "News Item",
    "description": "Morbi magna augue mauris pellentesque sodales eleifend in suspendisse quam orci lacus mattis. Magna netus sem velit tempus in tortor nunc suspendisse laoreet nec. Vitae fusce lectus condimentum. Lacus justo vel imperdiet. Magna porta. Porta dolor hac amet dictum placerat facilisis faucibus ut. Felis donec quisque quis odio venenatis proin morbi. Fusce lacus sociis lorem adipiscing aliquet odio. Nulla curae fermentum sem. Dolor morbi.",
    "_atrefs": {},
    "_layout": "newsitem_view",
    "_workflow_history": {
        "simple_publication_workflow": [
            {
                "action": null,
                "review_state": "private",
                "actor": "admin",
                "comments": "",
                "time": "2018/10/26 13:44:45.374644 GMT-4"
            },
            {
                "action": "publish",
                "review_state": "published",
                "actor": "admin",
                "comments": "",
                "time": "2018/10/26 13:44:45.791654 GMT-4"
            }
        ]
    },
    "_content_type_rights": "text/plain",
    "_directly_provided": [],
    "_classname": "ATNewsItem",
    "_datafield_image": {
        "encoding": "base64",
        "filename": "",
        "data": "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",
        "content_type": "image/jpeg",
        "size": 5764
    },
    "_userdefined_roles": [],
    "_content_type": "text/html",
    "_id": "purus-felis-aliquam-egestas-lectus-ante-velit-laoreet.",
    "effectiveDate": "None",
    "language": "en",
    "rights": "Risus ipsum. Purus fames eget mattis integer quam ut consectetuer urna lacus tincidunt quam sit. Magna risus. Lorem felis. Massa etiam velit cursus vestibulum morbi diam. Metus lorem pede varius quisque posuere taciti neque eu porttitor id et cursus augue. Vitae purus eni netus lorem non nisi sit nunc ultrices tincidunt. Class neque scelerisque id congue mi turpis donec tortor sapien purus ac. Donec morbi cras laoreet. Donec massa proin metus per odio tincidunt magnis interdum. Neque curae duis. Metus proin molestie donec.",
    "_content_type_description": "text/plain",
    "_uid": "4acf06985b74439b91e502301a7455fa",
    "_owner": "admin",
    "_content_type_location": "text/plain",
    "_permissions": {
        "Modify portal content": {
            "acquire": false,
            "roles": [
                "Editor",
                "Manager",
                "Owner",
                "Site Administrator"
            ]
        },
        "Access contents information": {
            "acquire": false,
            "roles": [
                "Anonymous"
            ]
        },
        "View": {
            "acquire": false,
            "roles": [
                "Anonymous"
            ]
        }
    },
    "_properties": [
        [
            "title",
            "Purus felis aliquam egestas lectus ante velit laoreet.",
            "string"
        ]
    ],
    "allowDiscussion": false,
    "_gopip": 106,
    "creators": [
        "admin"
    ],
    "_path": "/Plone/news/purus-felis-aliquam-egestas-lectus-ante-velit-laoreet."
}
```
