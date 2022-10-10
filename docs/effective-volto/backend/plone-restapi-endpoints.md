---
myst:
  html_meta:
    "description": "Plone REST API endpoints"
    "property=og:description": "Plone REST API endpoints"
    "property=og:title": "Plone RES TAPI endpoints"
    "keywords": "Volto, Plone, REST API, JSON, Backend"
---

# Plone REST API endpoints

Volto comunicates with the Plone backend via the so-called "endpoints", which
care REST API services exposed by plone.restapi. Some of these endpoints include:

You communicate with the REST API service using `application/json` ACCEPT header:

```bash
curl -H "Accept: application/json" http://localhost:8080/Plone/mycontent
```

The response from the server is typically JSON content (using the
[JSONSchema][1] format).

```
GET /plone/front-page HTTP/1.1
Accept: application/json
Authorization: Basic YWRtaW46c2VjcmV0

{
  "@id": "http://localhost:55001/plone/front-page",
  "@type": "Document",
  "@components": [
    {
      "@id": "http://localhost:55001/plone/front-page/@actions"
    },
    {
      "@id": "http://localhost:55001/plone/front-page/@breadcrumbs"
    },
    {
      "@id": "http://localhost:55001/plone/front-page/@navigation"
    },
    {
      "@id": "http://localhost:55001/plone/front-page/@types"
    },
    {
      "@id": "http://localhost:55001/plone/front-page/@workflow"
    },
    {
      "more components": "..."
    }
  ],
  "UID": "1f699ffa110e45afb1ba502f75f7ec33",
  "title": "Welcome to Plone",
  "more attributes": "..."
}
```

To access these endpoints, you can use a variety of HTTP verbs (and they are,
typically, semantically meaningful, following REST API conventions). For example,
the following verbs are used for content manipulation:

- `GET /folder` to fetch information
- `POST /folder/{document-id}` to create new content in a folder
- `PATCH /folder/{document-id}` to update a document
- `DELETE /folder/{document-id}` to remove a document

plone.restapi comes with many many endpoints, covering a lot of the Plone
backend functionality. By convention the endpoints are named with a single `@`
as prefix, to show similarity to the classic Browser Views. Some examples include:

- The **unnamed service**, which serves as the "content" endpoint, accessed by simply
  GETing a content URL with the `application/json` header
- the `@navigation` endpoints which returns a tree of global navigation items
- the `@breadcrumbs` which can be used to build a Breadcrumbs for any context
- the `@querystring-search` that can be used to create a listing, similar to
  the Collection listing

A complete listing of all the available endpoints is available in the
[plone.restapi endpoints documentation][2]

[1]: https://json-schema.org/
[2]: https://plonerestapi.readthedocs.io/en/latest/endpoints/
