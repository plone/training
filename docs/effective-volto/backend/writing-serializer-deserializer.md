# Writing a serializer or a deserializer

In plone.restapi we have an hierarchy, several levels deep, of serializers and
deserializers adapters. Keep in mind that "serializing" is the operation where
we transform Python objects to a representation (JSON) and deserializing is
when we take that representation (JSON coming from the browser POST, for
example) and convert it to live Python objects.

- content based, where the class of the context item is used as discriminator
  in the adaptor to `plone.restapi.interfaces.ISerializeToJson` (and the
  counterpart `IDeserializeToJson`.
- field based, used when processing DX Content, where each field/property is
  adapted for endpoint serialization with the `IFieldSerializer`
  / `IFieldDeserializer`
- block based, where we take the JSON data bits that represent a Volto block
  data and transform it (see the [writing block transformers](./writing-block-transformers) page).
- value based, where each Python basic data value needs to be transformed into
  a JSON-compatible representation, with the `IJsonCompatible` adaptor (use
  `json_compatible()` helper for this
