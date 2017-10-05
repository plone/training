Dynamic Roles
=============

Plone core's ``borg.localrole`` package allows you to hook into role-resolving code and add roles dynamically. I.e. the role on the user depends on HTTP request / environment conditions and is not something set in the site database.


Using Dynamic Roles
-------------------

To start utilizing dynamic roles in Plone, you will need to create an Zope 3 Adapter for ``ILocalRoleProvider`` in your custom product that contains the code to return the correct roles for a user in a specific context.

* getAllRoles() is overridden to return a custom role which is not available
  through normal security machinery. This is required because Plone/Zope
  builds look-up tables based on the result of getAllRoles() and
  all possible roles must appear there

* getRoles() is overridden to call custom getDummyRolesOnContext()
  which has the actual logic to resolve the roles

* An example code checks whether the context object implements
  a marker interface and gives the user a role based on that

**Note:** getRoles() function is called several times per request so you might want to cache the result.

Example ``localroles.py``

.. code:: python

    from zope.interface import Interface, implements
    from zope.component import adapts
    from borg.localrole.interfaces import ILocalRoleProvider

    class DummyLocalRoleAdapter(object):
        """ Give additional Member roles based on context and DummyUser type.

        This enables giving View permission on items higher in the
        traversign path than the user folder itself.
        """
        implements(ILocalRoleProvider)
        adapts(Interface)

        def __init__(self, context):
            self.context = context


        def getEditorRolesOnContext(self, context, principal_id):
            """ Calculate magical Dummy roles based on the user object.

            Note: This function is *heavy* since it wakes lots of objects along the acquisition chain.
            """

            # Filter out bogus look-ups - Plone calls this function
            # for every possible role look up out there, but
            # we are interested only these two cases
            if IDummyMarkerInterface.providedBy(context):
                    return ["Editor"]

            # No match
            return []

        def getRoles(self, principal_id):
            """Returns the roles for the given principal in context.

            This function is additional besides other ILocalRoleProvider plug-ins.

            @param context: Any Plone object
            @param principal_id: User login id
            """
            return self.getDummyRolesOnContext(self.context, principal_id)

        def getAllRoles(self):
            """Returns all the local roles assigned in this context:
            (principal_id, [role1, role2])"""
            return [ ("dummy_id", ["Editor"]) ]

Custom local role implementation is made effective using :term:`ZCML` adapter directive in your add-ons ``configure.zcml``

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:zcml="http://namespaces.zope.org/zcml">

      <adapter
          factory=".localroles.DummyLocalRoleAdapter"
          name="dummy_local_role"
          />

    </configure>
