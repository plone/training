.. _behaviors2-label:

More Complex Behaviors
======================

In this part you will:

* Write an annotation

Topics covered:

* Annotation Marker Interfaces

.. _behaviors2-annotations-label:

Using Annotations
-----------------
.. only:: not presentation

    We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations and need to understand the implications.

    `Annotations`_ in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without colliding.

    So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so it has to be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisions.

.. only:: presentation

 * What are annotations
 * When to use them

.. _Annotations: https://pypi.python.org/pypi/zope.annotation/4.2.0

.. _behaviors2-schema-label:

Using Schema
------------

.. only:: not presentation

    The attribute where we store our data will be declared as a schema field. We mark the field as an omitted field (using schema directive similar to ``read_permission`` or ``widget``), because we are not going to create z3c.form widgets for entering or displaying them. We do provide a schema, because many other packages use the schema information to get knowledge of the relevant fields.

    For example, when files were migrated to blobs, new objects had to be created and every schema field was copied. The code can't know about our field, except if we provide schema information.

.. only:: presentation

 * Why to use schemas always

.. _behaviors2-code-label:

Writing Code
------------

To start, we create a directory :file:`behavior` with an empty :file:`behavior/__init__.py` file.

Next we must, as always, register our zcml.

First, add the information that there will be another zcml file in :file:`configure.zcml`


.. code-block:: xml
    :linenos:

    <configure
          ...>

      ...
      <include package=".behavior" />
      ...

    </configure>

Next, create :file:`behavior/configure.zcml`

.. code-block:: xml
    :linenos:

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone">

      <plone:behavior
          title="Voting"
          description="Allow voting for an item"
          provides="starzel.votable_behavior.interfaces.IVoting"
          factory=".voting.Vote"
          marker="starzel.votable_behavior.interfaces.IVotable"
          />

    </configure>

There are some important differences to our first behavior:

  * There is a marker interface
  * There is a factory

.. only:: not presentation

    The factory is a class that provides the behavior logic and gives access to the attributes we provide.
    Factories in Plone/Zope land are retrieved by adapting an object to an interface.
    If you want your behavior, you would write :samp:`IVoting(object)`

    But in order for this to work, your object may *not* be implementing the IVoting interface, because if it did, :samp:`IVoting(object)` would return the object itself!
    If I need a marker interface for objects providing my behavior, I must provide one, for this we use the marker attribute. My object implements :samp:`IVotable` and because of this, we can write views and viewlets just for this content type.

The interfaces need to be written, in our case into a file :file:`interfaces.py`:

.. code-block:: python
    :linenos:

    # encoding=utf-8
    from plone import api
    from plone.autoform import directives
    from plone.autoform.interfaces import IFormFieldProvider
    from plone.supermodel import model
    from plone.supermodel.directives import fieldset
    from zope import schema
    from zope.interface import alsoProvides
    from zope.interface import Interface

    class IVotableLayer(Interface):
        """Marker interface for the Browserlayer
        """

    # Ivotable is the marker interface for contenttypes who support this behavior
    class IVotable(Interface):
        pass

    # This is the behaviors interface. When doing IVoting(object), you receive an
    # adapter
    class IVoting(model.Schema):
        if not api.env.debug_mode():
            directives.omitted("votes")
            directives.omitted("voted")

        fieldset(
            'debug',
            label=u'debug',
            fields=('votes', 'voted'),
        )

        votes = schema.Dict(title=u"Vote info",
                            key_type=schema.TextLine(title=u"Voted number"),
                            value_type=schema.Int(title=u"Voted so often"),
                            required=False)
        voted = schema.List(title=u"Vote hashes",
                            value_type=schema.TextLine(),
                            required=False)

        def vote(request):
            """
            Store the vote information, store the request hash to ensure
            that the user does not vote twice
            """

        def average_vote():
            """
            Return the average voting for an item
            """

        def has_votes():
            """
            Return whether anybody ever voted for this item
            """

        def already_voted(request):
            """
            Return the information wether a person already voted.
            This is not very high level and can be tricked out easily
            """

        def clear():
            """
            Clear the votes. Should only be called by admins
            """

    alsoProvides(IVoting, IFormFieldProvider)


.. only:: not presentation

    This is a lot of code. The IVotableLayer we will need later for viewlets and browser views. Let's add it right here.
    The IVotable interface is the simple marker interface. It will only be used to bind browser views and viewlets to contenttypes that provide our behavior, so no code needed.

    The IVoting class is more complex, as you can see. While IVoting is just an interface, we use :samp:`plone.supermodel.model.Schema` for advanced dexterity features.
    Zope.schema provides no means for hiding fields. The directives :samp:`form.omitted` from :samp:`plone.autoform` allow us to annotate this additional information so that the autoform renderers for forms can use the additional information.

    We make this omit conditional. If we run Plone in debug mode, we will be able to see the internal data in the edit form.

    We create minimal schema fields for our internal data structures. For a small test, I removed the form omitted directives and opened the edit view of a talk that uses the behavior. After seeing the ugliness, I decided that I should provide at least  minimum of information. Titles and required are purely optional, but very helpful if the fields won't be omitted, something that can be helpful when debugging the behavior.
    Later, when we implement the behavior, the :samp:`votes` and :samp:`voted` attributes are implemented in such a way that you can't just modify these fields, they are read only.

    Then we define the API that we are going to use in browser views and viewlets.

    The last line ensures that the schema fields are known to other packages. Whenever some code wants all schemas from an object, it receives the schema defined directly on the object and the additional schemata. Additional schemata are compiled by looking for behaviors and whether they provide the :samp:`IFormFieldProvider` functionality. Only then the fields are known as schema fields.

Now the only thing that is missing is the behavior, which we must put into :file:`behavior/voting.py`

.. code-block:: python
    :linenos:

    # encoding=utf-8
    from hashlib import md5
    from persistent.dict import PersistentDict
    from persistent.list import PersistentList
    from zope.annotation.interfaces import IAnnotations

    KEY = "starzel.votable_behavior.behavior.voting.Vote"


    class Vote(object):
        def __init__(self, context):
            self.context = context
            annotations = IAnnotations(context)
            if KEY not in annotations.keys():
                annotations[KEY] = PersistentDict({
                    "voted": PersistentList(),
                    'votes': PersistentDict()
                    })
            self.annotations = annotations[KEY]

        @property
        def votes(self):
            return self.annotations['votes']

        @property
        def voted(self):
            return self.annotations['voted']

.. only:: not presentation

    In our :samp:`__init__` method we get *annotations* from the object.
    We look for data with a specific key.

    The key in this example is the same as what I would get with :samp:`__name__+Vote.__name__`. But we won't create a dynamic name, this would be very clever and clever is bad.

    By declaring a static name, we won't run into problems if we restructure the code.

    You can see that we initialize the data if it doesn't exist. We work with PersistentDict and PersistentList. To understand why we do this, it is important to understand how the ZODB works.

    .. seealso::

        The ZODB can store objects. It has a special root object that you will never touch. Whatever you store there, will be part of the root object, except if it is an object subclassing :samp:`persistent.Persistent` Then it will be stored independently.

        Zope/ZODB Persistent objects note when you change an attribute on it and mark itself as changed. Changed objects will be saved to the database. This happens automatically. Each request begins a transaction and after our code runs and the Zope Server is preparing to send back the response we generated, the transaction will be committed and everything we changed will be saved.

        Now, if have a normal dictionary on a persistent object, and you will only change the dictionary, the persistent object has no way to know if the dictionary has been changed. This `happens`_ from time to time.

        So one solution is to change the special attribute :samp:`_p_changed` to :samp:`True` on the persistent object, or to use a PersistentDict. That is what we are doing here.

        You can find more information in the documentation of the ZODB, in particular `Rules for Persistent Classes <http://www.zodb.org/en/latest/documentation/guide/prog-zodb.html#rules-for-writing-persistent-classes>`_


    Next we provide the internal fields via properties. Using this form of property makes them read only properties, as we did not define write handlers. We don't need them so we won't add them.

    As you have seen in the Schema declaration, if you run your site in debug mode, you will see an edit field for these fields. But trying to change these fields will throw an exception.

    .. _happens: https://github.com/plone/Products.CMFEditions/commit/5c07c72bc8701cf28c9cc68ad940186b9e296ddf

.. only:: presentation

 * Explain ZODB and Persistent Classes

Let's continue with this file:

.. code-block:: python
    :linenos:

        def _hash(self, request):
            """
            This hash can be tricked out by changing IP addresses and might allow
            only a single person of a big company to vote
            """
            hash_ = md5()
            hash_.update(request.getClientAddr())
            for key in ["User-Agent", "Accept-Language",
                        "Accept-Encoding"]:
                hash_.update(request.getHeader(key))
            return hash_.hexdigest()

        def vote(self, vote, request):
            if self.already_voted(request):
                raise KeyError("You may not vote twice")
            vote = int(vote)
            self.annotations['voted'].append(self._hash(request))
            votes = self.annotations['votes']
            if vote not in votes:
                votes[vote] = 1
            else:
                votes[vote] += 1

        def average_vote(self):
            if not has_votes(self):
                return 0
            total_votes = sum(self.annotations['votes'].values())
            total_points = sum([vote * count for (vote, count) in
                                self.annotations['votes'].items()])
            return float(total_points) / total_votes

        def has_votes(self):
            return len(self.annotations.get('votes', [])) != 0

        def already_voted(self, request):
            return self._hash(request) in self.annotations['voted']

        def clear(self):
            annotations = IAnnotations(self.context)
            annotations[KEY] = PersistentDict({'voted': PersistentList(),
                                               'votes': PersistentDict()})
            self.annotations = annotations[KEY]

.. only:: not presentation

    We start with a little helper method which is not exposed via the interface. We don't want people to vote twice. There are many ways to ensure this and each one has flaws.

    We chose this way to show you how to access information from the request the browser of the user sent to us. First, we get the ip of the user, then we access a small set of headers from the user's browser and generate an md5 checksum of this.

    The vote method wants a vote and a request. We check the preconditions, then we convert the vote to an integer, store the request to :samp:`voted` and the votes into the :samp:`votes` dictionary. We just count there how often any vote has been given.

    Everything else is just python.
