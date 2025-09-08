---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Local Roles

## Local Roles On Folders

There may be some situations where you don't want your group to have a specific role across the entire site.
You can manage that too.

When setting up your group in the Site Setup, do not assign it a role.
Go to the folder where you want the group to have specific permissions and assign the group that role on the sharing tab for the folder.

You can assign individual users permissions at this level as well.
Add the user to the sharing tab and assign the permission to that user.
When you assign roles at an object level like this, you are assigning local roles.

Local roles give users (or groups) extra permissions in a very specific context.
For example, you may have two groups: pirates and ninjas.

The ninjas probably don't want the pirates mucking about with their content.
In this case, you could create a folder for the ninjas and assign their group to have a local role of Owner over the folder.
Uncheck the inherit permissions box and now your ninjas have their own folder where they can add content and the pirates cannot see or add anything to this folder.
Similarly, if only the pirate captain should have access to a folder,
add the pirate captain user to the sharing tab and select the correct permission.

Don't forget to uncheck the inherit permissions box, otherwise your folder will inherit permissions from the rest of the site.

## Local Roles On Groups

A state can also assign local roles to groups.
This is akin to assigning roles to groups on Plone's Sharing tab, but the mapping of roles to groups happens on each state change,
much like the mapping of roles to permissions.

Thus, you can say that in the pending_secondary state, members of the Secondary reviewers group has the `Reviewer` local role.
This is powerful stuff when combined with the more usual role-to-permission mapping.

### Additional Resources

- <https://5.docs.plone.org/working-with-content/collaboration-and-workflow/collaboration-through-sharing.html>
- <https://5.docs.plone.org/develop/plone/security/local_roles.html>
