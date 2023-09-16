---
myst:
  html_meta:
    "description": "Plone development tools"
    "property=og:description": "Plone development tools"
    "property=og:title": "Plone development"
    "keywords": "Plone, Volto, development, React, Redux"
---

(volto-development-label)=

# Develop


(editors)=

## IDE – Integrated developement environment

You are about to write code in Python and React / Javascript.
An appropriate integrated development environment supports both writing code and accessing our coding base: Plone Python code and Javascript / React code.

Some of the most used editors in the Plone community are listed here.

- [VSCode](https://code.visualstudio.com/)
- [Sublime](https://www.sublimetext.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Wing IDE](http://wingide.com/)

Some features that most editors have in one form or another, are essential when developing with Plone.

| Task | VSCode |
| --- | --- |
| find in project | {kbd}`cmd shift f` |
| find files in a project | {kbd}`cmd p` |
| find symbols (methods, classes, …) in a project | {kbd}`cmd shift o` |
| go to definition | {kbd}`F12` |
| powerful search & replace | |
| git diff | sidebar tab 'source control' |
| file diff | select via sidebar tab 'explorer' |

The capability of performing a _full text search_ through the complete Plone frontend code is invaluable.
Thanks to `omelette` mapping the Volto code in your project, you can search through the complete Plone frontend code base quickly.

IDE's nowadays have plenty of features.
Beyond the existing features, many extensions offer multiple practical features.
Here are some extensions we recommend when using VSCode:

- Easy Snippet: Turn your selection into a snippet.
- autoDocstring: Generates python docstrings.
- JSON Crack: Seamlessly visualize JSON data instantly into graphs.
- MyST-Markdown:Oofficial markdown syntax extension for MyST (Markedly Structured Text)
- Plone Snippets
- EsLint: Statically analyzes your code to quickly find problems.

Editor support for `ReactJS` development is explained in {doc}`Effective Volto training: VSCode extensions and helpers<../effective-volto/development/vscode>`.

Checkout VSCode documentation for topics like [code navigation](https://code.visualstudio.com/docs/editor/editingevolved), [Keyboard shortcuts and Multiple selections](https://code.visualstudio.com/docs/editor/codebasics) and many more that makes your everday work easier.


(volto-development-tools-label)=

## Tools

### Browser Development Tools

React components can be inspected with `React Developer Tools`: props, hierarchy, and a lot more.

- [React Developer Tools Chrome](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [React Developer Tools Firefox](https://addons.mozilla.org/de/firefox/addon/react-devtools/)

The Redux store and actions can be inspected with `Redux Developer Tools`.

- [Redux Developer Tools Chrome](https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd)
- [Redux Developer Tools Firefox](https://addons.mozilla.org/de/firefox/addon/reduxdevtools/)


### Postman

[Postman](https://www.postman.com/) is an app that lets you execute and save requests.
We will request REST API endpoints of the backend later with actions.


## Tips

**Debugging React**

A variables value can of course always be printed to the developer tools console with `console.debug("var_name", var_name)`.
But if you want to see values inside rendered components, than this can be done by including `{var_name}`.

If the value is an `Object`, than this is also possible by stringifiying it:
Just include `{JSON.stringify(var_name_object)}` in your components `html` code.

**Troubleshooting "Python import cannot be resolved"**

```{image} _static/couldnotberesolved.png
:alt: Python import cannot be resolved
```

Select the Python of your project `backend/venv/bin/python`.

In VSCode this can be done by following the menu on selecting the current Python in the bottom of the IDE.

