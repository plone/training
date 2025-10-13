---
myst:
  html_meta:
    "description": "Prepare data with collective.transmute for import with plone.exportimport"
    "property=og:description": "Prepare data with collective.transmute for import with plone.exportimport"
    "property=og:title": "Prepare data with collective.transmute for import with plone.exportimport"
    "keywords": "export, import, transmute"
---

(transmute-label)=

# Prepare data with `collective.transmute` for import with `plone.exportimport`

Instead of using collective.exportimport for the import of exported data you can also use [`collective.transmute`](https://github.com/collective/collective.transmute)

`collective.transmute` transforms data extracted by `collective.exportimport` into data to be importable by `plone.exportimport`.

```{important}
A requirement for `collective.transmute` to work properly is to export each item as a separate file on the server and include the blob-data as base64 in the json-files.
That means calling the `export_content` view with the arguments `include_blobs=1` and `download_to_server=2`.
```

Here is an example for a `export_all` view that does that:

```python
# -*- coding: UTF-8 -*-
from contentexport.interfaces import IContentexportLayer
from plone import api
from Products.Five import BrowserView
from zope.interface import alsoProvides

import logging

logger = logging.getLogger(__name__)

TYPES_TO_EXPORT = []


class ExportAll(BrowserView):

    def __call__(self):
        request = self.request
        if not request.form.get("form.submitted", False):
            return self.index()

        qi = api.portal.get_tool("portal_quickinstaller")
        if not qi.isProductInstalled("contentimport"):
            qi.installProducts(["contentimport"])
            alsoProvides(request, IContentexportLayer)

        portal = api.portal.get()

        export_name = "export_content"
        logger.info("Start {}".format(export_name))
        view = api.content.get_view(export_name, portal, request)
        exported_types = TYPES_TO_EXPORT
        request.form["form.submitted"] = True
        view(
            portal_type=exported_types,
            include_blobs=1,  # base64
            download_to_server=2, # each item as a separate file
            migration=True,
        )
        logger.info("Finished {}".format(export_name))

        other_exports = [
            "export_relations",
            "export_members",
            "export_translations",
            "export_localroles",
            "export_ordering",
            "export_defaultpages",
            "export_discussion",
            "export_portlets",
            "export_redirects",
        ]
        for export_name in other_exports:
            export_view = api.content.get_view(export_name, portal, request)
            request.form["form.submitted"] = True
            # store each result in var/instance/export_xxx.json
            export_view(download_to_server=True)

        logger.info("Finished export_all")
        # Important! Redirect to prevent infinite export loop :)
        return self.request.response.redirect(self.context.absolute_url())
```

With `collective.transmute` you can first create a report about the exported data regarding content types, views, review states and creators.

With `collective.transmute` you need to an configure a migration-pipeline of steps that are applied to each item. A step is basically the same as a `item_hook` in `collective.exportimport`.

There are some steps that come with `collective.transmute` that help to migrate to Volto (e.g. transform html to Volto-blocks, integrate default-pages and transform collections to listing blocks).

`collective.transmute` does not do the import (thats delegated to `plone.exportimport`), so there are no `obj_hooks` like in `plone.exportimport`, you would need to add them to `plone.exportimport` if required.

Since `collective.transmute` is still in alpha and is undergoing development we will refer to the documentation:

```{seealso}
https://collective.github.io/collective.transmute
```
