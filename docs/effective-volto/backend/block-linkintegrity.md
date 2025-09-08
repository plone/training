---
myst:
  html_meta:
    "description": "Link integrity for blocks"
    "property=og:description": "Link integrity for blocks"
    "property=og:title": "Link integrity for blocks"
    "keywords": "Volto, Plone, Link integrity"
---

# Link integrity for blocks

Using the latest plone.restapi, Volto blocks also provide Link Integrity
protection (if you have references to other internal content, removing the
destination object triggers a validation rule).

By default the `href` and `url` fields of any block data is used to establish
the link integraty protection. You can define additional fields, or other
extraction methods, by writing a subscriber for `plone.restapi.interfaces.IBlockFieldLinkIntegrityRetriever`.

For example:

```python
@adapter(IBlocks, IBrowserRequest)
@implementer(IBlockFieldLinkIntegrityRetriever)
class GenericBlockLinksRetriever(object):
    order = 1
    block_type = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block):
        """
        Returns a list of internal links
        """
        links = []
        for field in ["url", "href"]:
            value = block.get(field, "")
            if value and "resolveuid" in value:
                links.append(value)
        return links
```

```xml
  <subscriber
      factory=".blocks_linkintegrity.GenericBlockLinksRetriever"
      provides="plone.restapi.interfaces.IBlockFieldLinkIntegrityRetriever"
      />
```
