---
html_meta:
  "description": "Authors guide to Sphinx, MyST and markdown"
  "keywords": "Sphinx, MyST, markdown"
---

# Guide for Authors

## MyST markdown, Sphinx

We use [MyST, or Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/), a rich and extensible flavor of Markdown, for authoring training documentation.

Meta Data
: SEO info

      ---
      html_meta:
            "description": "directives and other examples in markdown / mySt"
            "keywords": "Sphinx, MyST, markdown"
      ---

Cross Reference: chapter
:     We created an add-on in the last chapter {doc}`volto_custom_addon`.

Cross Reference: section

: create anchor
  ```
  (volto-custom-addon-final-label)=
  ```
  create link
  ```
  Switch to section [Release a Volto add-on](/mastering-plone/volto_custom_addon.html#volto-custom-addon-final-label).
  ```
  or

  ```
  Switch to section {ref}`Release a Volto add-on <volto-custom-addon-final-label>`.
  ```

Image
:     ```{figure} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block
      ```

: with caption

      ```{figure} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block

      Accordion Block
      ```

: with zoom

      ```{figure} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block
      :width: 100%
      ```

Code Block
: example code python

      ```{code-block} python
      :lineno-start: 10
      :emphasize-lines: 1, 3

      a = 2
      print('my 1st line')
      print(f'my {a}nd line')
      ```

: is rendered as:

```{code-block} python
:lineno-start: 10
:emphasize-lines: 1, 3

a = 2
print('my 1st line')
print(f'my {a}nd line')
```

Code Snippet Expandable
: Solutions of Exercises

  Be aware of the nested directives! Increase outer back ticks!

      ````{admonition} Complete code for ReactJS component
      :class: toggle

      Here's my code snippet

      Maecenas sed diam eget risus varius blandit sit amet non magna. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Nullam quis risus eget urna mollis ornare vel eu leo. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Etiam porta sem malesuada magna mollis euismod. Nulla vitae elit libero, a pharetra augue.


      ```{code-block} jsx
      :linenos: true

      import React, { useState } from 'react';
      ```
      ````

````{admonition} Complete code for ReactJS component
:class: toggle

Here's my code snippet

Maecenas sed diam eget risus varius blandit sit amet non magna. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Nullam quis risus eget urna mollis ornare vel eu leo. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Etiam porta sem malesuada magna mollis euismod. Nulla vitae elit libero, a pharetra augue.


```{code-block} jsx
:linenos: true

import React, { useState } from 'react';
```
````

Glossary
: Reference glossary terms

  To reference terms in your glossary, use the `{term} role`.    
  For example, ``{term}`ReactJS` `` becomes a reference to term {term}`ReactJS`.

: Add glossary term

  Add your term to `/glossary.md`
