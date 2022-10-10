---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(code-walkthrough-label)=

# Code Walkthrough

Volto is based on React, Redux and React-Router.
All the code is located in the `src` folder.
Inside the `src` folder we used the default Redux folder structure.

## Actions

`actions` contains all the redux actions for fetching all backend data like content, users and so on.

## Components

`components` contains all the views.
This includes views for the manage interface and the theme.

## Config

In this folder all configuration is stored.
All configuration can be overridden in your theme package.

## Constants

The constants contain all constants including the action types.

## Helpers

`helpers` contains helper methods like for example url helpers.

## Icons

All the Pastanaga icons are located in this folder.

## Middleware

The API middleware is located in this folder which takes care of the communication with the backend.

## Reducers

All the reducers are located here.

## Theme

The `theme` folder contains the Pastanaga theme which is used for the styling.
The `theme.config` can be used to set the theme settings.
