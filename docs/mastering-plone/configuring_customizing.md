---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": "Configuring and Customizing Plone 'Through The Web'"
    "keywords": "Plone, configuration"
---

(configuring-customizing-label)=

# Configuring and Customizing Plone "Through The Web"

% TODO Update for Plone 6!
% TODO Add Volto screenshots for control panels

(customizing-controlpanel-label)=

## The site setup

Important parts of Plone can be configured in the site setup, often still called `control panel`.

Follow the menu in the left bottom of your site via {guilabel}`Site Setup`

```{figure} _static/features_control_panel.png
:alt: Site Setup

Site Setup
```

We'll explain every page and mention some of the actions you can perform here.

```{note}
Not all control panels known from Plone Classic are available in Volto yet.
Switch to the backend if you need to configure your site: `http://localhost:8080/Plone/@@overview-controlpanel`.
```

### General

1. Add-ons
1. Database
1. Date and time
1. Language
1. Mail
1. Navigation
1. Search
1. Site
1. Social Media
1. Undo
1. URL management
1. Volto settings

The following control panels are so far only available in the backend:

1. Actions
1. Discussion
1. Syndication

### Content

1. Content rules
1. Content types
1. Editing
1. Image handling
1. Markup
1. Moderate comments
1. Relations

The following control panels are so far only available in the backend:

1. Content Settings

### Users

1. Editing users
1. Editing groups
1. Editing group memberships

### Security

1. Security

The following control panels are so far only available in the backend:

1. Errors
1. HTML Filtering

### Advanced

The following control panels are so far only available in the backend:

1. Caching
1. Configuration Registry
1. Maintenance
1. Resource registries

### Add-ons

More control panels appear for installed add-ons.

Below the links to panels you will find information on your Plone, Zope and Python versions and an indicator as to whether you're running in production or development mode.


(customizing-zmi-label)=

## ZMI (Zope management interface)

Go to <http://localhost:8080/Plone/manage>

Zope is the foundation of Plone. Here you can access the inner workings of Zope and Plone alike.

```{warning}
Here you can easily break your site so you should know what you are doing!
Back up your site, just to be sure.
```

```{only} not presentation
We only cover three parts of customization in the ZMI now.
Later on when we will have added our own code we'll come back to the ZMI and will look for it.

At some point you'll have to learn what all those objects are about. But not today.
```

### Actions (portal_actions)

- Actions are mostly links. But **really flexible** links.
- Actions are configurable TTW (Through-The-Web) and through code.
- These actions are usually iterated over in viewlets and displayed.

Examples:

- Links in the Footer (`site_actions`)
- Actions Dropdown (`object_buttons`)

Actions have properties like:

- description
- url
- i18n-domain
- condition
- permissions

#### `site_actions`

These are the links at the bottom of the page:

- {guilabel}`Site Map`
- {guilabel}`Accessibility`
- {guilabel}`Contact`
- {guilabel}`Site Setup`

We want a new link to legal information, called "Imprint".

- Go to `site_actions` (we know that because we checked in `@@manage-viewlets`)
- Add a CMF Action `imprint`
- Set URL to `string:${portal_url}/imprint`
- Leave *condition* empty
- Set permission to `View`
- Save

```{only} not presentation
explain
```

- Check if the link is on the page
- Create new Document "Imprint" and publish

```{seealso}
<https://5.docs.plone.org/develop/plone/functionality/actions.html>
```

#### Global navigation

- The horizontal navigation is called `portal_tabs`
- Go to {menuselection}`portal_actions --> portal_tabs` [Link](http://localhost:8080/Plone/portal_actions/portal_tabs/manage_main)
- Edit `index_html`

Where is the navigation?

The navigation shows content-objects, which are in Plone's root. Plus all actions in `portal_tabs`.

Explain & edit `index_html`

Configuring the navigation itself is done elsewhere: <http://localhost:8080/Plone/@@navigation-controlpanel>

If time explain:

- user > login/logout


### Further tools in the ZMI

There are many more notable items in the ZMI. We'll visit some of them later.

- {guilabel}`acl_users`
- {guilabel}`error_log`
- {guilabel}`portal_setup`
- {guilabel}`portal_workflow`
- {guilabel}`portal_catalog`

(customizing-summary-label)=

## Summary

You can configure and customize a lot in Plone through the web.
The most important options are accessible in the [Plone control panel](http://localhost:3000/controlpanel) but some are hidden away in the [ZMI](http://localhost:8080/Plone/manage).
The amount and presentation of information may be overwhelming and the differences between the Volto frontend and the Classic Plone frontend adds even more complexity.
Don't worry, you'll get the hang of it through practice.
