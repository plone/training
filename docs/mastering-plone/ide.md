---
myst:
  html_meta:
    "description": "Development support by editors and IDE's"
    "property=og:description": "Development support by editors and IDE's"
    "property=og:title": "Development environments and editors"
    "keywords": "Plone, Volto, editor, linter"
---

% ide-label:

# IDE's and editors

In this part you will:

- learn about editors

Topics covered:

- editor features and extensions

Plone consists of more than 20.000 files! You need a tool to manage that. No development environment is complete without a good editor.

Here are some of the most used editors in the Plone community.
Pick your favorite!

- [VSCode](https://code.visualstudio.com/)
- [Sublime](https://www.sublimetext.com/)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Wing IDE](http://wingide.com/)
- [Vim](https://www.vim.org/)
- [Emacs](https://www.gnu.org/software/emacs/)

Some features that most editors have in one form or another are essential when developing with Plone.

- **Find in project** (VSCode: {kbd}`cmd-shift-f`)
- **Find files in Project** (VSCode: {kbd}`cmd-p`)
- **Find methods and classes in Project** (VSCode: {kbd}`cmd-shift-o`)
- **Goto Definition** (VSCode Mac: {kbd}`F12`)
- **Powerful search & replace**
- **Git Diff** (VSCode: sidebar tab 'source control')
- **File Diff** (VSCode: select via sidebar tab 'explorer')

The capability of performing a _full text search_ through the complete Plone code is invaluable. Thanks to omelette, an SSD and plenty of RAM you can search through the complete Plone code base in quickly.

Some editors and IDEs have to be extended to be fully featured. Here are some packages we recommend if using VSCode:

- Bracket Highlighter: Decorates text inbetween symbols
- Easy Snippet: Turn your selection into a snippet

Editor support for `ReactJS` development is explained in {doc}`Effective Volto training: VSCode extensions and helpers<../effective-volto/development/vscode>`.

A must to be mentioned is `ESLint`, which helps correcting and enhancing `Javascript` code.

