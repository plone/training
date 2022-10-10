---
myst:
  html_meta:
    "description": "Volto add-ons development training module 9, Plone integration"
    "property=og:description": "Volto add-ons development training module 9"
    "property=og:title": "Volto add-ons development Plone integration"
    "keywords": "Volto"
---

# Plone integration with Volto blocks

When developing for Volto websites, don't neglect the server-side, Plone.
Beyond the regular endpoints and expanders that [plone.restapi] offers,
there's a few dedicated features that can improve the quality of Volto-powered
websites.

## Block transformations

The main feature that applies to Volto blocks is called the "blocks
transformers". They are adaptors that can be registered per block type.
They can alter the output on serialization (when the fetching information from Plone),
as well as on deserialization (when information arrives in Plone, from the client).

```python
@implementer(IBlockFieldDeserializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class DatabaseQueryDeserializeTransformer(object):
    order = 100
    block_type = 'database_listing'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        value["items"] = db.query(value)    # pseudo code
        return value
```

Then register it as a subscription adapter:

```xml
<subscriber factory=".blocks.DatabaseQueryDeserializeTransformer"
  provides="plone.restapi.interfaces.IBlockFieldDeserializationTransformer"/>
```

Note that you'll probably want to also register the reverse.

## Smart fields

It is possible to register a generic block transformer that applies to all
block types. By doing so we can process block information consistently for all
blocks, providing us with the "smart fields" concept.

A "smart field" is a convention: "all block fields named `url` will be
transformed on serialization/deserialization, to store them with a resolveuid".

## Searchable text from blocks

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

This adapter needs to be registered as a named adapter, where the name is the
same as the block type (its `@type` property from the block value).

```xml
<adapter name="image" factory=".indexers.ImageBlockSearchableText" />
```

Examples of potential smart fields:

- `_v_*` blocks, to provide volatile data from the backend
- `blob`, which would deserialize base64-encoded binary data to an attachment
  store, then serialize back as a simple download link

```{note}
These smart fields don't exist right now. But it would be great if
they did exist.
```

[plone.restapi]: https://github.com/plone/plone.restapi
