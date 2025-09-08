---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(configuring-customizing-label)=

# Configuring and Customizing Plone "Through The Web"

```{eval-rst}
..  todo::

    * Update for Plone 6!
    * Add Volto screenshots for control panels


 .. sectionauthor:: Philip Bauer <bauer@starzel.de>
```

(customizing-controlpanel-label)=

## The Control Panel

The most important parts of Plone can be configured in the control panel.

- Click on the portrait/username in the toolbar
- Click {guilabel}`Site Setup`

```{figure} _static/features_control_panel.png
:alt: Site Setup

Site Setup
```

We'll explain every page and mention some of the actions you can perform here.

```{note}
Not all control panels are available in Volto.
Some are not useful in Volto, e.g. TinyMCE since that editor is not used here.
Other control panels, e.g. Content Rules still need to be implemented.
```

### General

1. Add-ons
1. Database
1. Date and Time
1. Language
1. Mail
1. Navigation
1. Search
1. Site
1. Social Media
1. Undo
1. URL Management
1. Volto Settings

The following control panels are so far only available in the backend:

1. Actions
1. Discussion
1. Syndication
1. Theming
1. TinyMCE

### Content

1. Content Types
1. Editing
1. Image Handling
1. Markup
1. Moderate Comments

The following control panels are so far only available in the backend:

1. Content Settings

### Users

1. Editing users

### Security

1. Security

The following control panels are so far only available in the backend:

1. Errors
2. HTML Filtering

### Advanced

The following control panels are so far only available in the backend:

1. Caching
2. Configuration Registry
3. Maintenance
4. Management Interface
5. Resource Registries

Below the links you will find information on your Plone, Zope and Python Versions and an indicator as to whether you're running in production or development mode.

#### Change the logo

```{note}
This only changes the logo used in Plone Classic (the backend) and does not change the logo in Volto.
The Logo in Volto is changed in next chapter {doc}`volto_overrides`.
```

Let's change the logo.

- Download a logo: <https://www.starzel.de/plone-tutorial/logo.png>
- Go to <http://localhost:8080/Plone/@@site-controlpanel>
- Upload the Logo.

```{figure} _static/configuring_customizing_logo.png
:alt: The view of the homepage with the customized logo.

The view of the homepage with the customized logo.
```

```{seealso}
<https://5.docs.plone.org/adapt-and-extend/change-the-logo.html>
```

(customizing-portlets-label)=

## Portlets

```{note}
Portlets only exist in the classic frontend. Volto has no equivalent so far.
The discussion about this is ongoing :)
```

In the toolbar under the {guilabel}`Portlets` section, you can open the configuration for the different places where you can have portlets.

- UI fit for smart content editors
- Various types
- Portlet configuration is inherited
- Managing
- Ordering/weighting
- The future: may be replaced by tiles
- `@@manage-portlets`

Example:

- Go to <http://localhost:8080/Plone/@@manage-portlets>

- Add a static portlet "Sponsors" on the right side.

- Remove the news portlet and add a new one on the left side.

- Go to the training folder: <http://localhost:8080/Plone/training> and click {guilabel}`Manage portlets`

- Add a static portlet. "Featured training: Become a Plone-Rockstar at Mastering Plone!"

- Use the toolbar to configure the portlets of the footer:

  - Hide the portlets "Footer" and "Colophon".
  - Add a {guilabel}`Static text portlet` and enter "Copyright 2019 by Plone Community".
  - Use {menuselection}`Insert --> Special Character` to add a real © sign.
  - You could turn that into a link to a copyright page later.

(customizing-viewlets-label)=

## Viewlets

```{note}
Viewlets only exist in the classic frontend.
In Volto they are replaced by react components and have no user-interface to move or show/hide them.
How to customize these elements in Volto is discussed in next chapter {doc}`volto_overrides`.
```

Portlets save data, Viewlets usually don't. Viewlets are often used for UI-Elements and have no nice UI to customize them.

- `@@manage-viewlets`
- Viewlets have no nice UI
- Not aimed at content editors
- Not locally addable, no configurable inheritance.
- Usually global (depends on code)
- Will be replaced by tiles?
- The code is much simpler (we'll create one tomorrow).
- Live in viewlet managers, can be nested (by adding a viewlet that contains a viewlet manager).
- TTW reordering only within the same viewlet manager.
- The code decides when it is shown and what it shows.

(customizing-zmi-label)=

## ZMI (Zope Management Interface)

Go to <http://localhost:8080/Plone/manage>

Zope is the foundation of Plone. Here you can access the inner workings of Zope and Plone alike.

```{note}
Here you can easily break your site so you should know what you are doing!
```

```{only} not presentation
We only cover three parts of customization in the ZMI now.
Later on when we added our own code we'll come back to the ZMI and will look for it.

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

### portal_view_customizations

```{note}
This feature has no effect for Volto since it allows customzing server-side rendered templates.
How to customize the equivalent views in Volto is discussed in next chapter {doc}`volto_overrides`.
```

#### Change the footer

- Go to `portal_view_customizations`

- Search `plone.footer`, click and customize

- Replace the content with the following

  ```html
  <div i18n:domain="plone"
       id="portal-footer">
     <p>&copy; 2019 by me! |
       <a href="mailto:info@ploneconf.org">
        Contact us
       </a>
     </p>
  </div>
  ```

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
The most important options are accessible in the [Plone control panel](http://localhost:8080/Plone/@@overview-controlpanel) but some are hidden away in the [ZMI](http://localhost:8080/Plone/manage).
The amount and presentation of information may be overwhelming and the differences between the Volto frontend and the Classic Plone frontend adds even more complexity.
Don't worry, you'll get the hang of it through practice.
