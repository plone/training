Programming Plone
=================

memoize.ram:
brains = catalog(portal_type="talk")
return [brain.modified for brain in brains]


programming plone

plone.api
http://docs.plone.org/external/plone.api/docs/index.html

- content
- portal
- groups
- users
- environment

Examples
http://docs.plone.org/external/plone.api/docs/portal.html#send-e-mail

http://docs.plone.org/external/plone.api/docs/content.html#create-content

http://docs.plone.org/external/plone.api/docs/content.html#get-content-object

http://docs.plone.org/external/plone.api/docs/content.html#get-view

http://docs.plone.org/external/plone.api/docs/content.html#transition

http://docs.plone.org/external/plone.api/docs/user.html#get-user-roles

http://docs.plone.org/external/plone.api/docs/env.html#switch-roles-inside-a-block


methoden
- getToolByName > api.portal.get_tool
- getMultiAdapter > api.content.get_view

api of some tools
portal_catalog:
-searchResults
-uniqueValuesFor(index)

portal_setup:
-runAllImportStepsFromProfile

portal_quickinstaller
- installProducts

portal_properties


