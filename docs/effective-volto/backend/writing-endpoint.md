---
myst:
  html_meta:
    "description": "Writing an endpoint"
    "property=og:description": "Writing an endpoint"
    "property=og:title": "Writing an endpoint"
    "keywords": "Volto, Plone, REST API, plone.restapi, Endpoint"
---

# Writing an endpoint

Endpoint services are registered with the `plone:service` ZCML tags:

```xml
<plone:service
  method="GET"
  factory=".get.BreadcrumbsGet"
  for="zope.interface.Interface"
  permission="zope2.View"
  name="@breadcrumbs"
  />
```

They are similar in registration with the more simple BrowserViews, except you
can also set the HTTP verb that they will be used for.

For the python implementation:

```python
from plone.restapi.services import Service

class BreadcrumbsGet(Service):
    def reply(self):
        # ... pseudocode
        return extract_something_from(self.context)
```

Make sure that the return value is compatible with JSON serialization. You may
need to convert the value. plone.restapi provides an extensible adapter-based
function for this, the `plone.restapi.serializer.converters.json_compatible`.

A common pattern is to reuse a content expander class in your service
implementation. You can do it like:

```python
from plone.restapi.services import Service
from plone.restapi.interfaces import IExpandableElement

class BreadcrumbsGet(Service):
    def reply(self):
        # ... pseudocode
        expander = getMultiAdapter((self.context, self.request), interface=IExpandableElement, name="breadcrumbs")
        return expander(expand=True)['breadcrumbs']
```
