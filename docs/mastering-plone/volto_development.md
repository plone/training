---
myst:
  html_meta:
    "description": "Tools for developing in Volto"
    "property=og:description": "Tools for developing in Volto"
    "property=og:title": "Volto development"
    "keywords": "Volto, development, React, Redux"
---

(volto-development-label)=

# Volto App Development

## Editor

The variety of editors is big.
Try `VSCode` if you do not already use it and don't have a strong alternative preference.
`VSCode` comes with a good support for programming React apps and development in general.

`VSCode` extensions:

- "Add jsdoc comments" 
  
  Adds simple jsdoc comments for the parameters of a selected function signature.
- "Better Comments"
  
  Improve your code commenting by annotating with alert, informational, TODOs, …
- "Babel JavaScript"
  
  Syntax highlighting for Javascript and React
- "Easy Snippet"
  
  Turn your selection into a snippet.


(volto-development-tools-label)=

## Tools

### Browser Development Tools

React components can be inspected with `React Developer Tools`: props, hierarchy, and a lot more.

- [Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [Firefox](https://addons.mozilla.org/de/firefox/addon/react-devtools/)

The Redux store and actions can be inspected with `Redux Developer Tools`.

- [Chrome](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd)
- [Firefox](https://addons.mozilla.org/de/firefox/addon/reduxdevtools/)


### Postman

Postman is an app that lets you execute and save requests.
We will request REST API endpoints of the backend later with actions.

[Download Postman](https://www.postman.com/downloads/)


## Tips

A variables value can of course always printed to the developer tools console with `console.debug("var_name", var_name)`.
But if you want to see values inside rendered components and the value is an Object, than this is also possible.
Just include `{JSON.stringify(var_name_object)}` in your components `html` code.
