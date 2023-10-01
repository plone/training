---
myst:
  html_meta:
    "description": "Writing a block transform"
    "property=og:description": "Writing a block transform"
    "property=og:title": "Writing a block transform"
    "keywords": "Volto, Plone, REST API, plone.restapi, Volto blocks, Serialization, Block Transformers"
---

# Writing a block transform

Practical experience has shown that it is useful to transform, server-side, the value of block fields on inbound (deserialization, saving in the database) or outbound (serialization, exposing information to the browser) operations.
For example, HTML field values are cleaned up using `portal_transforms`.
Or paths in image blocks are transformed to use `resolveuid`.

It is possible to influence the transformation of block values per block type.
For example, to tweak the value stored in an `image` type block, we can create a new subscriber as follows:

```python
@implementer(IBlockFieldDeserializationTransformer)
@adapter(IBlocks, IBrowserRequest)
class ImageBlockDeserializeTransformer(object):
    order = 100
    block_type = 'image'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, value):
        portal = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state"
        ).portal()
        url = value.get('url', '')
        deserialized_url = path2uid(
            context=self.context, portal=portal,
            href=url
        )
        value["url"] = deserialized_url
        return value
```

Then register it as a subscription adapter:

```xml
<subscriber factory=".blocks.ImageBlockDeserializeTransformer"
  provides="plone.restapi.interfaces.IBlockFieldDeserializationTransformer"/>
```

This would replace the `url` value to use `resolveuid` instead of hard coding the image path.

The `block_type` attribute needs to match the `@type` field of the block value.
The `order` attribute is used in sorting the subscribers for the same field.
A lower number has higher precedence, that is, it is executed first.

On the serialization path, a block value can be tweaked with a similar transformer
For example, on an imaginary database listing block type:

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
        value["items"] = db.query(value)  # pseudocode
        return value
```

Then register it as a subscription adapter:

```xml
<subscriber factory=".blocks.DatabaseQueryDeserializeTransformer"
  provides="plone.restapi.interfaces.IBlockFieldDeserializationTransformer"/>
```

## Generic block transformers and smart fields

You can create a block transformer that applies to all blocks by using `None` as the value for `block_type`.
The `order` field still applies, though.
The generic block transformers enable us to create **smart block fields**, which are handled differently.
For example, any internal link stored as `url` or `href` in a block value is converted (and stored) as a `resolveuid`-based URL, then resolved back to a full URL on block serialization.
Any block field name can be a URL, if you make that value an object with `@type` and `value` keys, like below:

```JSON
{
  "@type": "headlineBlock",
  "preview_image": {
    "@type": "URL",
    "value": "../path/to/object"
  }
}
```

The same is valid for any of the following combination of values, even when
they are found in a list of objects that's set as the value of a block field:

```JSON
{
  "@type": "headlineBlock",
  "preview_images": [
    {
      "@id": "../path/to/object",
    },
    {
      "url": "../path/to/object",
    },
    {
      "href": "../path/to/object",
    },
    {
      "@type": "URL",
      "value": "../path/to/object"
    },
    {
      "@id": "../path/to/object",
      "@type": "URL",
      "value": "../path/to/object"
    }
  ]
}
```

Another **smart field** is the `searchableText` field in a block value.
It needs to be a plain text value, and it will be used in the `SearchableText` value for the context item.

If you need to store "subblocks" in a block value, you should use the `blocks` smart field (or `data.blocks`).
Doing so integrates those blocks with the transformers.
