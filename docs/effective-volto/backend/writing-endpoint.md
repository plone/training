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
