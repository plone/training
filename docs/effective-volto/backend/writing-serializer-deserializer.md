---
myst:
  html_meta:
    "description": "Writing a serializer or a deserializer"
    "property=og:description": "Writing a serializer or a deserializer"
    "property=og:title": "Writing a serializer or a deserializer"
    "keywords": "Volto, Plone, REST API, plone.restapi, serializer, deserializer"
---

# Writing a serializer or a deserializer

In plone.restapi we have an hierarchy, several levels deep, of serializers and
deserializers adapters. Keep in mind that "serializing" is the operation where
we transform Python objects to a representation (JSON) and deserializing is
when we take that representation (JSON coming from the browser POST, for
example) and convert it to live Python objects. The (de)serializers, with the
type-based lookups are a great example of ZCML use, as they're all implemented
as adapters for the content+request => ISomeSerializationInferface.

1.  content based, where the class of the context item is used as discriminator in the adaptor to `plone.restapi.interfaces.ISerializeToJson` (and the counterpart `IDeserializeToJson`.
    See the [DX Content serializer][1].
2.  field based, used when processing DX Content, where each field/property is adapted for endpoint serialization with the `IFieldSerializer` / `IFieldDeserializer`.
    See the [DX Field serializers][2].
3.  block based, where we take the JSON data bits that represent a Volto block data and transform it (see the {doc}`writing-block-transforms` chapter).
4.  value based, where each Python basic data value needs to be transformed into a JSON-compatible representation, with the `IJsonCompatible` adaptor (use `json_compatible()` helper for this.
    See the [converters.py module][3] with these basic serializers.

Here's how the Folder serializer looks like:

```python
@implementer(ISerializeToJson)
@adapter(IDexterityContainer, Interface)
class SerializeFolderToJson(SerializeToJson):
    def _build_query(self):
        path = "/".join(self.context.getPhysicalPath())
        query = {
            "path": {"depth": 1, "query": path},
            "sort_on": "getObjPositionInParent",
        }
        return query

    def __call__(self, version=None, include_items=True):
        folder_metadata = super().__call__(version=version)

        folder_metadata.update({"is_folderish": True})
        result = folder_metadata

        include_items = self.request.form.get("include_items", include_items)
        include_items = boolean_value(include_items)
        if include_items:
            query = self._build_query()

            catalog = getToolByName(self.context, "portal_catalog")
            brains = catalog(query)

            batch = HypermediaBatch(self.request, brains)

            result["items_total"] = batch.items_total
            if batch.links:
                result["batching"] = batch.links

            if "fullobjects" in list(self.request.form):
                result["items"] = getMultiAdapter(
                    (brains, self.request), ISerializeToJson
                )(fullobjects=True)["items"]
            else:
                result["items"] = [
                    getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
                    for brain in batch
                ]
        return result
```

[1]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/dxcontent.py
[2]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/dxfields.py
[3]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/converters.py
