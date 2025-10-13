---
myst:
  html_meta:
    "description": "Migrating from third party systems to Plone"
    "property=og:description": "Migrating from third party systems to Plone"
    "property=og:title": "Migrating from third party systems to Plone"
    "keywords": "Migrating, import, JSON, Plone"
---

(migrate-to-plone-label)=

# Migrating from third party systems to Plone

For many systems, it should be possible to generate data in the format required by `@@import_content`.

The minimal data required is:

`@id`
: The URL of the item.

`@type`
: A content type that exists in Plone.

`id`
: The ID (the last part of `@id`).

`@parent["@id"]`
: The URL of the container, usually the items `@id` without the last part.

Here is a minimal example for a JSON file that could be imported:

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

For all other imports, the forms where you can upload JSON files contain examples for expected JSON data.
