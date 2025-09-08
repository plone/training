---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Basic Roles and Permissions

Roles, groups, permissions, workflows, states, transitions are all a part of Plone's robust security model.
But you don't have to be a guru to understand the basic Plone permissions you will encounter on a daily basis.

## Definitions

Let's start off with some basic terminology.
Permissions are individual rights that give the user the ability to perform an action.
Roles are a combination of permissions.
Both users and groups can be assigned roles.

### Roles

Roles are a combination of permissions that you will assign to your users.
Plone comes with a basic set of roles, each of which already has certain permissions assigned.
Below you will learn a little bit about the defaults for each role.

Most of your site users have the "Member" role.
By default, a Member can see anything that is published, see the contents of a folder, see a list of other portal members and groups, and see portlets.
Depending on how your site is customized, Members may not have access to certain portlets or specific parts of the site.
I keep track of what a Member has access to by reminding myself that a Member cannot change content and can only see what has been published.
You will want to assign the Member role to your every day, normal users who will not be changing content.

Everyone who joins your site should be assigned this role.

#### Reader

The Reader role may be almost the opposite from the Member role.
Readers can view content items that are in the private state, but cannot make any changes.
You should assign people the Reader role when you want them to review a piece of content that is not yet published.

The Reader role is great for when you want only certain people to see a piece of content.
You can also use the Reader role as part of a document review cycle for users who would like to review your document
but not make changes to the document.

#### Contributor

A user with a Contributor role can do all the things a member can, plus add content, use version control, and view content that is not in the published state.
A contributor cannot modify (edit) another user's content.
The Contributor role should be given to users who will create content but not edit another person's content.

#### Owner

The owner role is inherited when a user adds a piece of content.
You have to have another role, like Contributor, that has the ability to add content.
Once you add a piece of content, you are automatically assigned the Owner role over this content.
When you are the Owner of a piece of content, you can modify that piece of content whenever you wish, no matter what state the content is in.

#### Editor

A user with the Editor role by default does not have the ability to add content, but can modify(edit) content and use version control.
An Editor can also manage properties of content and can submit content for publication.
The Editor role should be used when a Contributor is sending a piece of content for review.

The Editor will review, and change, the content and then submit it for publication.

#### Reviewer

A Reviewer role picks up where the Editor leaves off.
While a Reviewer does not have as many rights as the Editor, the Reviewer can publish content that has been sent to the submit
for publication state or send it back to the owner.
The Reviewer also has a special portlet just for content that needs to be reviewed.

Once an Editor has submitted content for publication, the Reviewer will review the content and then has the option to Publish
or send back the content for the Contributor to review.

The Reviewer has the final say if something gets published or not.

#### Site Administrator

The Site Administrator role is very similar to the Manager role described below, but with a few exceptions.
The Site Administrator has full access to manage all of the content in the portal, and can perform certain actions from the
site setup such as adding and removing users.

They do not have access to the ZMI or to actions such as activating Plone add-ons, configuring caching or discussion settings.

#### Manager

The Manager role is the role that can do everything.
A user with the Manager role is a Site Administrator.
Manager privileges are not given out lightly as this role can add, delete, and make changes to any thing in the site.

While more than one person should have this role, it definitely should not be handed out to large numbers of people.
Your site Manger has access to the control panel, where many site wide settings can be changed and updated.

The Manager can also manage things via the {term}`ZMI` (Zope Management Interface).

## Giving Out Permissions

The easiest way to hand out permissions is to assign roles to groups.
You can create a group and assign that group a role.

Then, whenever you want to give someone certain permissions, you can add that user to that group.
Assigning roles on a group level allows you to more easily manage large numbers of users.

## Permissions

Plone's security system is based on the concept of *permissions* protecting *operations*
(like accessing a view, viewing a field, modifying a field, or adding a type of content) that are granted to *roles*,
which in turn are granted to *users* and/or *groups*.

In the context of developing content types, permissions are typically used in three different ways:

- A content type or group of related content types often has a custom
  *add permission* which controls who can add this type of content.
- Views (including forms) are sometimes protected by custom
  permissions.
- Individual fields are sometimes protected by permissions,
  so that some users can view and edit fields that others can't see.

It is not hard to create new permissions.

Be aware that it is considered good practice to use the standard permissions wherever possible and use *workflow*
to control which roles are granted these permissions on a per-instance basis.

### Standard Permissions

Many of the standard permissions can be found in `Product.CMFCore`'s `permissions.zcml` (`parts/omelette/Products/CMFCore/permissions.zcml`).

Here, you will find a short `id` (also known as the *Zope 3 permission id*) and a longer `title` (also known as the *Zope 2 permission title*).

For historical reasons, some areas in Plone use the id, whilst others use the title.

As a rule of thumb:

- Browser views defined in ZCML use the Zope 3 permission id.
- Security checks using `zope.security.checkPermission()` use the Zope
  3 permission id
- Dexterity's `add_permission` FTI variable uses the Zope 3 permission
  id.
- The `rolemap.xml` GenericSetup handler and workflows use the Zope 2
  permission title.
- Security checks using `AccessControl`’s
  `getSecurityManager().checkPermission()`, including the methods on
  the `portal_membership` tool, use the Zope 2 permission title.

The most commonly used permission are shown below.

The Zope 2 permission title is shown in parentheses.

`zope2.View` ({guilabel}`View`)

: used to control access to the standard view of a content item;

`zope2.DeleteObjects` ({guilabel}`Delete objects`)

: used to control the ability to delete child objects in a container;

`cmf.ModifyPortalContent` ({guilabel}`Modify portal content`)

: used to control write access to content items;

`cmf.ManagePortal` ({guilabel}`Manage portal`)

: used to control access to management screens;

`cmf.AddPortalContent` ({guilabel}`Add portal content`)

: the standard add permission required to add content to a folder;

`cmf.SetOwnProperties` ({guilabel}`Set own properties`)

: used to allow users to set their own member properties'

`cmf.RequestReview` ({guilabel}`Request review`)

: typically used as a workflow transition guard
  to allow users to submit content for review;

`cmf.ReviewPortalContent` ({guilabel}`Review portal content`)

: usually granted to the `Reviewer` role,
  controlling the ability to publish or reject content.

`cmf.AddPortalMember` ({guilabel}`Add portal member`)

: usually granted to the `Site Administrator` and `Manager`  role,
  controlling the ability to add new users into the site. It is also
  granted to the `Anonymous` role if you have enabled self user registration.

Here is an example of how Permissions can be changed by event subscribers:

```python
>>> from plone import api
>>> api.portal.get_registry_record(name="plone.enable_self_reg")
False
>>> from AccessControl.SecurityManagement import noSecurityManager
>>> noSecurityManager() # Log out the Special System User
>>> api.user.get_current()
<SpecialUser 'Anonymous User'>
>>> api.user.has_permission("Add portal member")
False
>>> api.portal.set_registry_record(name="plone.enable_self_reg", value=True)
>>> api.user.has_permission("Add portal member")
True
```

Inside of `Products.CMFPlone` there is an event subscriber listening for
changes to specific registry keys and will alter the permissions in the site
based on the change in the setting.
