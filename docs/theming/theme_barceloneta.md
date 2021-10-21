---
html_meta:
  "description": ""
  "property=og:description": ""
  "property=og:title": ""
  "keywords": ""
---

# Create a theme based on Barceloneta

We’re going to create a theme for Plone 6 Classic UI that is based on the default theme plonetheme.barceloneta.

This package will allow you to change and extend the look of Plone to your needs. You will develop on the filesystem. You can add your package to any code repository e.g. GitHub and re-use it on different Plone sites.

**Use Case**
- Your own theme package based on Plone Classic Theming
- You want to have control over all styles
- You want to build on existing Plone Core or Addon Templates and Markup

**What you will learn**
- How to prepare your development setup
- How to create your theme package
- What are the important parts of your theme
- How to add and compile your styles


## Creating a theme package

To create a filesystem based theme, we first create a new addon package for Plone type:

```{code-block} shell
$ plonecli create addon myaddon.name
```

Answer some questions about the package:

```
--> Author's name [Your Name]:

--> Author's email [yourname@example.com]:

--> Author's GitHub username: your_name_gitbhub

--> Package description [An add-on for Plone]:

--> Do you want me to initialize a GIT repository in your new package?

--> Plone version [6.0]:

--> Python version for virtualenv [python3]:

--> Do you want me to activate VS Code support? (y/n) [y]:

Generated file structure at ... ./myaddon.name
```

Change into your package:

```{code-block} shell
$ cd myaddon.name
```

To create a theme based on Plones default theme Barceloneta, add `theme_barceloneta` from the list of templates.

```{code-block} shell
$ plonecli add theme_barceloneta
```

You will be asked for to name your theme (This will be the name that is displayed in the theming control panel and can but does not have to be the package name):

```{code-block} shell
--> Theme name [My Theme]:

Generated file structure at ... ./myaddon.name
```

All theme related files have now been added to `./myaddon.name/src/youraddon/name/theme/`



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


