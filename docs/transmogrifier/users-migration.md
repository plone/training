---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Users & Groups Migration

Export using a script:

```python
""" To run this file:
    $ bin/instance run export_users.py
"""

import os
import json

site = app.Plone

os.mkdir('99')
counter = 99000

uf = site.acl_users
users = uf.source_users.getUsers()

exported_users = {"_acl_users": dict()}

for user in users:
    user_data = {
        'email': user.getProperty('email'),
        'roles': user.getRoles(),
    }
    exported_users['_acl_users'][user._id] = user_data

f = open(os.path.join('99', str(counter) + '.json'), 'wb')
json.dump(exported_users, f, indent=4)
counter += 1
f.close()

groups = dict(uf.source_groups._groups)
exported_groups = {"_acl_groups": dict()}
for group in groups:
    # Loop over each group grabbing members
    members = uf.source_groups._group_principal_map[group].keys()
    roles = uf.getGroupByName(group)._roles
    group_info = {
        'title': groups[group]['title'],
        'description': groups[group]['description'],
        'members': members,
        'roles': roles,
    }
    exported_groups['_acl_groups'][group] = group_info

f = open(os.path.join('99', str(counter) + '.json'), 'wb')
json.dump(exported_groups, f, indent=4)
counter += 1
f.close()
```

The import can be done as blueprints, which is the code below.
But it would be better off as an upgrade step.

```python
@provider(ISectionBlueprint)
@implementer(ISection)
class ImportUsers(object):
    """ Import users that had been exported
        with the custom export script
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            if '_acl_users' not in item:
                yield item
                continue

            for person in item['_acl_users']:
                user = api.user.get(username=person)
                data = item['_acl_users'][person]
                roles = data['roles']
                # remove these roles, they cannot be granted
                if 'Authenticated' in data['roles']:
                    roles.remove('Authenticated')
                if 'Anonymous' in data['roles']:
                    roles.remove('Anonymous')
                if not data['email']:
                    data['email'] = 'user@site.com'

                if user:
                    api.user.grant_roles(username=person, roles=roles)
                    continue
                try:
                    user = api.user.create(username=person,
                                           email=data['email'])
                    api.user.grant_roles(username=person, roles=roles)
                except ValueError as e:
                    logger.warn("Import User '{0}' threw an error: {1}".format(
                        person, e))
            yield item

@provider(ISectionBlueprint)
@implementer(ISection)
class Groups(object):
    """ Import groups that had been exported
        with the custom export script
    """

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context

        if 'acl_groups-key' in options:
            groupskeys = options['acl_groups-key'].splitlines()
        else:
            groupskeys = defaultKeys(
                options['blueprint'], name, 'acl_groups')
        self.groupskey = Matcher(*groupskeys)

    def __iter__(self):
        for item in self.previous:
            groupskey = self.groupskey(*item.keys())[0]

            if not groupskey:
                yield item
                continue

            group_tool = api.portal.get_tool(name='portal_groups')
            if '_acl_groups' not in item:
                yield item
                continue
            for group in item['_acl_groups']:
                acl_group = api.group.get(groupname=group)
                props = item['_acl_groups'][group]
                if not acl_group:
                    acl_group = api.group.create(
                        groupname=group,
                        title=props['title'],
                        description=props['description'],
                        roles=props['roles'],
                    )
                else:
                    group_tool.editGroup(
                        group,
                        roles=props['roles'],
                        title=props['title'],
                        description=props['description'],
                    )
                for member in props['members']:
                    acl_group.addMember(member)

            yield item
```
