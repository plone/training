# Writing a serializer or a deserializer

In plone.restapi we have an hierarchy, several levels deep, of serializers and
deserializers adapters. Keep in mind that "serializing" is the operation where
we transform Python objects to a representation (JSON) and deserializing is
when we take that representation (JSON coming from the browser POST, for
example) and convert it to live Python objects.

1. content based, where the class of the context item is used as discriminator
  in the adaptor to `plone.restapi.interfaces.ISerializeToJson` (and the
  counterpart `IDeserializeToJson`. See the [DX Content serializer][1]
2. field based, used when processing DX Content, where each field/property is
  adapted for endpoint serialization with the `IFieldSerializer`
  / `IFieldDeserializer`. See the [DX Field serializers][2]
3. block based, where we take the JSON data bits that represent a Volto block
  data and transform it (see the [writing block transformers](./writing-block-transformers) page).
4. value based, where each Python basic data value needs to be transformed into
  a JSON-compatible representation, with the `IJsonCompatible` adaptor (use
  `json_compatible()` helper for this. See the [converters.py module][3] with
  these basic serializers.


[1]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/dxcontent.py
[2]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/dxfields.py
[3]: https://github.com/plone/plone.restapi/blob/f5758140d49abdb602cbd3198626fd66871e9b1a/src/plone/restapi/serializer/converters.py
