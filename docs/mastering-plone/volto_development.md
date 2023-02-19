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


(editors)=

## IDE's and editors

The variety of editors is big.
Try `VSCode` if you do not already use it and don't have a strong alternative preference.
`VSCode` comes with a good support for programming React apps and development in general.

Plone consists of more than 20.000 files!
You need a tool to manage that.
No development environment is complete without a good editor.

Here are some of the most used editors in the Plone community.
Pick your favorite!

- [VSCode](https://code.visualstudio.com/)
- [Sublime](https://www.sublimetext.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Wing IDE](http://wingide.com/)

Some features that most editors have in one form or another, are essential when developing with Plone.

| Task | VSCode |
| --- | --- |
| Find in project | {kbd}`cmd-shift-f` |
| Find files in Project | {kbd}`cmd-p` |
| Find methods and classes in Project | {kbd}`cmd-shift-o` |
| Goto Definition | {kbd}`F12` |
| Powerful search & replace | |
| Git Diff | sidebar tab 'source control' |
| File Diff | select via sidebar tab 'explorer' |

The capability of performing a _full text search_ through the complete Plone code is invaluable.
Thanks to `omelette` mapping the Volto code in your project, an SSD and plenty of RAM you can search through the complete Plone code base quickly.

Editors and IDE's nowadays have plenty of features.
Beyond the existing features, many extensions offer multiple practival features.
Here are some packages we recommend when using VSCode:

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

A variables value can of course always printed to the developer tools console with `console.debug("var_name", var_name)`.
But if you want to see values inside rendered components, than this can be done by including {var_name}.
If the value is an Object, than this is also possible by stringifiying it:
Just include `{JSON.stringify(var_name_object)}` in your components `html` code.
