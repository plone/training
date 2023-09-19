---
myst:
  html_meta:
    "description": "Writing a content expansion endpoint"
    "property=og:description": "Writing a content expansion endpoint"
    "property=og:title": "Writing a content expansion endpoint"
    "keywords": "Volto, Plone, REST API, plone.restapi, Serialization, Content Expanders"
---

# Writing a content expansion endpoint

By default Volto fetches content using a single call to the
[unnamed (content) endpoint](https://github.com/plone/plone.restapi/blob/afde2a940d2518e061eb3fe30093093af55e3a50/src/plone/restapi/services/content/configure.zcml#L15-L20).

plone.restapi provides a mechanism to piggy-back on this network call to load
additional information, the so-called Content Expanders which are adaptors
for `plone.restapi.interfaces.IExpandableElement`.

For example, here's the registration for the breadcrumbs content expander:

```
<adapter
  factory=".get.Breadcrumbs"
  name="breadcrumbs"
  />
```

To activate the content expander, add its name to the `?expand` query parameter
of the main JSON endpoint call:

```bash
curl -i -X GET 'http://nohost/plone/front-page?expand=breadcrumbs,navigation' -H "Accept: application/json" --user admin:secret
```

These adaptors will typically include the same information that would be returned by calling
separately the service, in this case the `@breadcrumbs` service:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "@components": {
        "actions": {
            "@id": "http://localhost:55001/plone/front-page/@actions"
        },
        "aliases": {
            "@id": "http://localhost:55001/plone/front-page/@aliases"
        },
        "breadcrumbs": {
            "@id": "http://localhost:55001/plone/front-page/@breadcrumbs",
            "items": [
                {
                    "@id": "http://localhost:55001/plone/front-page",
                    "title": "Welcome to Plone"
                }
            ],
            "root": "http://localhost:55001/plone"
        },
        "contextnavigation": {
            "@id": "http://localhost:55001/plone/front-page/@contextnavigation"
        },
        "navigation": {
            "@id": "http://localhost:55001/plone/front-page/@navigation"
        },
        "types": {
            "@id": "http://localhost:55001/plone/front-page/@types"
        },
        "workflow": {
            "@id": "http://localhost:55001/plone/front-page/@workflow"
        }
    },
    "@id": "http://localhost:55001/plone/front-page",
    "@type": "Document",
    "UID": "SomeUUID000000000000000000000001",
    "allow_discussion": false,
    "changeNote": "",
    "contributors": [],
    "created": "1995-07-31T13:45:00",
    "creators": [
        "test_user_1_"
    ],
    "description": "Congratulations! You have successfully installed Plone.",
    "effective": null,
    "exclude_from_nav": false,
    "expires": null,
    "id": "front-page",
    "is_folderish": false,
    "language": "",
    "layout": "document_view",
    "lock": {
        "locked": false,
        "stealable": true
    },
    "modified": "1995-07-31T17:30:00",
    "next_item": {},
    "parent": {
        "@id": "http://localhost:55001/plone",
        "@type": "Plone Site",
        "description": "",
        "title": "Plone site"
    },
    "previous_item": {},
    "relatedItems": [],
    "review_state": "private",
    "rights": "",
    "subjects": [],
    "table_of_contents": null,
    "text": {
        "content-type": "text/plain",
        "data": "<p>If you&#x27;re seeing this instead of the web site you were expecting, the owner of this web site has just installed Plone. Do not contact the Plone Team or the Plone mailing lists about this.</p>",
        "encoding": "utf-8"
    },
    "title": "Welcome to Plone",
    "version": "current",
    "versioning_enabled": true,
    "working_copy": null,
    "working_copy_of": null
}
```

## Make Volto aware of it

Volto has a configuration point where you can instruct the automatic inclusion
of an api expander, on a particular route match for a particular Redux action.

For example:

```
import { GET_CONTENT } from '@plone/volto/constants/ActionTypes';

export default function applyConfig (config) {
  config.settings.apiExpanders = [
      ...config.settings.apiExpanders,
      {
        match: '',
        GET_CONTENT: ['mycustomexpander'],
      },
      {
        match: '/de',
        GET_CONTENT: ['myothercustomexpander'],
      }
  ];
  return config;
}
```

Notice that the api expanders are a feature of plone.restapi **content**
serialization, so they'll be included on endpoints where content is serialized.
