---
myst:
  html_meta:
    "description": "Migrating from 3rd party systems to Plone"
    "property=og:description": "Migrating from 3rd party systems to Plone"
    "property=og:title": "Migrating from 3rd party systems to Plone"
    "keywords": "Migrating, import, json"
---

(migrate-to-plone-label)=

# Migrating from 3rd party systems to Plone

For many systems it should be possible to generate data in the format required by `@@import_content`.

The minimal data required is:

`@id`
: The url of the item

`@type`
: A content-type that exists in Plone

`id`
: The id (the last part of `@id`)

`@parent["@id"]`
: The url of the container, usually the items `@id` without the last part.


Here is a minmal example for a json-file that could be imported:

```json
[{
    "@id": "http://localhost:8080/Plone/folder",
    "@type": "Folder",
    "id": "folder",
    "parent": {
        "@id": "http://localhost:8080/Plone"
    }
}]
```

A full example (as exported from Plone) for a document inside that folder:

```json
[{
    "@id": "http://localhost:8080/Plone/folder/document",
    "@type": "Document",
    "UID": "6552ee34f0e848a59ab66126d752e9df",
    "allow_discussion": false,
    "changeNote": "",
    "contributors": [],
    "created": "2022-10-05T14:39:33+00:00",
    "creators": [
        "admin"
    ],
    "description": "A test document",
    "effective": "2022-10-05T16:39:35",
    "exclude_from_nav": false,
    "expires": null,
    "id": "document",
    "is_folderish": false,
    "language": "de",
    "layout": "document_view",
    "lock": {
        "locked": false,
        "stealable": true
    },
    "modified": "2022-10-05T14:39:35+00:00",
    "parent": {
        "@id": "http://localhost:8080/Plone/folder",
        "@type": "Folder",
        "UID": "4302981ed51a4328b42a58f64ad6c0ff",
        "description": "",
        "review_state": "published",
        "title": "Folder"
    },
    "review_state": "published",
    "rights": null,
    "subjects": [
        "White noise"
    ],
    "table_of_contents": false,
    "text": {
        "content-type": "text/html",
        "data": "<p>Some <strong>text</strong> here</p>",
        "encoding": "utf-8"
    },
    "title": "Document",
    "version": "current",
    "versioning_enabled": true,
    "workflow_history": {
        "simple_publication_workflow": [
            {
                "action": null,
                "actor": "admin",
                "comments": "",
                "review_state": "private",
                "time": "2022-10-05T14:39:33+00:00"
            },
            {
                "action": "publish",
                "actor": "admin",
                "comments": "",
                "review_state": "published",
                "time": "2022-10-05T14:39:35+00:00"
            }
        ]
    }
}]
```

For all other imports the forms where you can upload json-files contain examples for expected json-data.
