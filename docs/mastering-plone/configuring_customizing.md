---
myst:
  html_meta:
    "description": "What you can do through the web without touching the code"
    "property=og:description": "What you can do through the web without touching the code"
    "property=og:title": "Configure Plone 'through the web'"
    "keywords": "Plone, configuration"
---

(configuring-customizing-label)=

# Configure Plone "through the web"

(customizing-controlpanel-label)=

## Site Setup

Important parts of Plone can be configured in the Site Setup area, often still called the "control panel".

As an admin user, open the menu at the bottom left of your site and choose {guilabel}`Site Setup`.

```{figure} _static/features_control_panel.png
:alt: Site Setup

Site Setup
```

We'll explain every page and mention some of the actions you can perform here.

```{note}
A few control panels are not available in Volto yet.
Switch to the backend if you need to configure your site: http://localhost:8080/Plone/@@overview-controlpanel.
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
1. URL Management
1. Undo
1. Volto Settings

The following control panels are so far only available in the backend:

1. Actions
1. Discussion
1. Syndication

### Content

1. Block Types
1. Content Rules
1. Content Types
1. Editing
1. Image Handling
1. Relations

The following control panels are so far only available in the backend:

1. Content Settings

### Users

1. Groups
1. User Group Membership
1. User and Group Settings
1. Users

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

## Zope Management Interface (ZMI)

Zope is the foundation of Plone.
Here you can access the inner workings of Zope and Plone alike.

Go to <http://localhost:8080/Plone/manage>

```{warning}
You can easily break your site here. So you should know what you are doing!
Back up your site, just to be sure.
```

Examples of what can be configured in the `ZMI` are:

* {guilabel}`portal_workflow` where you can inspect and manage existing and applied workflows, their states and transitions.

* {guilabel}`portal_catalog` where you can inspect existing indices.


## Summary

You can configure and customize a lot in Plone through the web.
The most important options are accessible in the [Plone control panel](http://localhost:3000/controlpanel) but some are hidden away in the [ZMI](http://localhost:8080/Plone/manage).
The amount and presentation of information may be overwhelming and the differences between the Volto frontend and the Classic Plone frontend add even more complexity.
Don't worry, you'll get the hang of it through practice.
