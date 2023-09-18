---
myst:
  html_meta:
    "description": "Block field contribute to `searchableText`"
    "property=og:description": "Block field contribute to `searchableText`"
    "property=og:title": "Block field contribute to `searchableText`"
    "keywords": "Volto, Plone, Searchable Text, Indexing, Catalog"
---

# Block field contribute to `searchableText`

Sometimes we want the blocks to be "text searchable", to participate in the
SearchableText extracted for the document.

There are two solutions for this, the simple but inneficient, and the
efficient but more complicated.

## Client side solution
The block provides the data to be indexed in its `searchableText` attribute:

{
  "@type": "image",
  "align": "center",
  "alt": "Plone Conference 2021 logo",
  "searchableText": "Plone Conference 2021 logo",
  "size": "l",
  "url": "https://2021.ploneconf.org/images/logoandfamiliesalt.svg"
}

This is the easy solution. The downside is the extra bits that have to be
stored in the database and shuffled around in network communication from the
browser to the Plone backend.

## Server side solution

A better solution (which is not always practical) is to write an adapter for
each type of block that needs to expose its searchable text:

For example:

```python
@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class ImageSearchableText(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block_value):
        return block_value['alt_text']
```

See `plone.restapi.interfaces.IBlockSearchableText` for details. The `__call__` methods needs to return a string, for the text to be indexed.

This adapter needs to be registered as a named adapter, where the name is the same as the block type (its `@type` property from the block value):

```xml
<adapter name="image" factory=".indexers.ImageBlockSearchableText" />
```
