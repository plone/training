---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Create a theme based on Barceloneta

We’re going to create a theme for Plone 6 Classic UI that is based on the default theme plonetheme.barceloneta. This package will allow you to change and extend the look of Plone to your needs. You will develop on the filesystem. You can add your package to any code repository e.g. GitHub and re-use it on different Plone sites.

## Use Case
- Your own theme package based on Plone Classic Theming
- You want to have control over all styles
- You want to build on existing Plone Core or Addon Templates and Markup

## What you will learn
- How to prepare your development setup
- How to create your theme package
- What are the important parts of your theme
- How to add and compile your styles

## Preparation
- Install npm
- Install plonecli

## Create a theme package
- Create addon package with plonecli
- Change into package
- Add theme
- Run buildout
- Explain theme structure
- Start Plone
- Install Theme

## Adding styles and compile
- Package.json explain dependencies and scripts
- npm run watch
- As a start add your logo through control panel
- Now you have some colors that you will use throughout your theme
- Explain Styles/Variables/..
- Bootstrap has a lot of variables to change almost everything that defines your theme - look at https://github.com/twbs/bootstrap/blob/main/scss/_variables.scss
- To make variables work they have to be defined before barceloneta/bootstap is imported
- Color variables
- Map variables for primary secondary…
- Properties “rounded”
- Add more rounding 1rem

## Fonts
Add fonts (link vs import)
Show index.html (preconnect)
Set font-family
Set font-sizes
Styles
Fix Search Button Styling
Navbar / Breadcrumbs
Add container to index.html
Add more styles
Custom CSS


