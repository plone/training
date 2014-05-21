More complex behaviors
======================

We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations and need to understand the implications.

Annotations in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without coliding.

So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so must be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisisons.

The attribute where we store our data will be declared as a schema field. We mark the field as an ommitted field, because we are not going to create z3c.form widgets for displaying them. We do provide a schema, because many other packages use the schema information to get knowledge of the relevant fields.
For example, when files have been migrated to blobs, new objects had to be created and every schema field was copied. The code can't know about our field, except if we provide schema information.

To start, we create a directory :file:`behavior`
