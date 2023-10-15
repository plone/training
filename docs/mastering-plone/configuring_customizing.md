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

1. Date and time
1. Language
1. Mail
1. Navigation
1. Search
1. Site
1. Social Media
1. Volto settings
1. Add-ons
1. Database
1. Undo
1. URL management

The following control panels are so far only available in the backend:

1. Actions
1. Discussion
1. Syndication

### Content

1. Content types
1. Editing
1. Image handling
1. Content rules
1. Relations
1. Moderate comments

The following control panels are so far only available in the backend:

1. Content Settings

### Users

1. User and group settings
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

Zope is the foundation of Plone.
Here you can access the inner workings of Zope and Plone alike.

Go to <http://localhost:8080/Plone/manage>

```{warning}
You can easily break your site here. So you should know what you are doing!
Back up your site, just to be sure.
```

Examples of what can be configured in the `ZMI` are

{guilabel}`portal_workflow` where you can inspect and manage existing and applied workflows, their states and transitions.

{guilabel}`portal_catalog` where you can inspect existing indices.


## Summary

You can configure and customize a lot in Plone through the web.
The most important options are accessible in the [Plone control panel](http://localhost:3000/controlpanel) but some are hidden away in the [ZMI](http://localhost:8080/Plone/manage).
The amount and presentation of information may be overwhelming and the differences between the Volto frontend and the Classic Plone frontend adds even more complexity.
Don't worry, you'll get the hang of it through practice.
