---
myst:
  html_meta:
    'description': 'Learn How to customize the Footer of the page'
    'property=og:description': 'Learn How to customize the Footer of the page'
    'property=og:title': 'Footer customization'
    'keywords': 'Plone, Volto, Training, Theme, Footer'
---

# Creating New Project

First you have to  install the cookieplone
```
pipx install cookieplone

```

After that you have to run it to create the project.

```
pipx run cookieplone
```

It is going to ask you multiple question. If you happy with default keep pressing enter. Otherwise overwrite this according to your needs.


```
 [1/17] Project Title (Project Title): my-vlt-project
  [2/17] Project Description (A new project using Plone 6.): My Project
  [3/17] Project Slug (Used for repository id) (my-vlt-project): my-project
  [4/17] Project URL (without protocol) (my-project.example.com): my-project.example.com
  [5/17] Author (Plone Foundation): <your name>
  [6/17] Author E-mail (collective@plone.org):
  [7/17] Should we use prerelease versions? (No):
  [8/17] Plone Version (6.0.13):
  [9/17] Volto Version (18.0.0):
  [10/17] Python Package Name (my.project):
  [11/17] Volto Addon Name (volto-my-project):
```

After creating project you have to build the volto project.

Run
```
make install
``

This will install all your backend as well as frontend project.

For running backend you have to run

```
make backend-start

```

For running frontend

```
make frontend-start

```

Please commit your inital commit by running

```
git add .
git commit -m 'initial-commit' --no-verify
```
Walk throught the boiler plate and explain them.
