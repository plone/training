---
myst:
  html_meta:
    "description": "Plone development tools"
    "property=og:description": "Plone development tools"
    "property=og:title": "Development tools"
    "keywords": "Plone, Volto, development, React, Redux"
---

(volto-development-label)=

# Development tools


(editors)=

## Integrated development environment (IDE)

You are about to write code in Python and React / JavaScript.
An appropriate integrated development environment supports both writing code and accessing our coding base: Plone Python code and JavaScript / React code.

Some of the most used editors in the Plone community are listed here.

- [VSCode](https://code.visualstudio.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Sublime](https://www.sublimetext.com/)
- [Wing IDE](https://wingware.com/)

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

The capability of performing a _full text search_ through the complete Plone codebase is invaluable.

IDEs nowadays have plenty of features.
Beyond the existing features, many extensions offer multiple practical features.
Here are some extensions we recommend when using VSCode:

- `Easy Snippet`: Turn your selection into a snippet.
- `autoDocstring`: Generates python docstrings.
- JSON Crack: Seamlessly visualize JSON data instantly into graphs.
- MyST-Markdown: Official markdown syntax extension for MyST (Markedly Structured Text)
- Plone Snippets
- `EsLint`: Statically analyzes your code to find problems.

Editor support for `ReactJS` development is explained in {doc}`Effective Volto training: VSCode extensions and helpers <training2024:effective-volto/development/vscode>`.

Check VSCode documentation for topics like [code navigation](https://code.visualstudio.com/docs/editing/editingevolved), [Keyboard shortcuts and Multiple selections](https://code.visualstudio.com/docs/editing/codebasics) and many more that make your everyday work easier.


(volto-development-tools-label)=

## Browser development tools

Most browsers have built-in developer tools which can be used to:

- explore the document object model (DOM)
- debug JavaScript code
- inspect styles
- inspect network requests

The **React Developer Tools** add a tab to inspect React components: props, hierarchy, and a lot more.

- [React Developer Tools Chrome](https://chromewebstore.google.com/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi)
- [React Developer Tools Firefox](https://addons.mozilla.org/de/firefox/addon/react-devtools/)

The **Redux Developer Tools** add a tab to inspect the Redux store and actions.

- [Redux Developer Tools Chrome](https://chromewebstore.google.com/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd)
- [Redux Developer Tools Firefox](https://addons.mozilla.org/de/firefox/addon/reduxdevtools/)


## Postman

[Postman](https://www.postman.com/) is an app that lets you execute and save requests.
We will request REST API endpoints of the backend later with actions.


## Tips

**Debugging React**

A variables value can of course always be printed to the developer tools console with `console.debug("var_name", var_name)`.
But if you want to see values inside rendered components, than this can be done by including `{var_name}`.

If the value is an `Object`, than this is also possible by stringifying it:
Just include `{JSON.stringify(var_name_object)}` in your components `html` code.

**Troubleshooting "Python import cannot be resolved"**

```{figure} _static/couldnotberesolved.png
:alt: Python import cannot be resolved
```

Select the Python of your project `backend/venv/bin/python`.

In VSCode this can be done by opening the Python menu at the bottom of the IDE.
