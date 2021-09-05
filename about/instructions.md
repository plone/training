---
html_meta:
  "description": "directives and other examples in markdown / mySt"
  "keywords": "Sphinx, MyST, markdown"
---

# Guide for Authors

We use [MyST, or Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/) as the syntax for authoring training documentation.

meta data
:     ---
      html_meta:
            "description": "directives and other examples in markdown / mySt"
            "keywords": "Sphinx, MyST, markdown"
      ---

cross reference: chapter
:     We created an add-on in the last chapter {doc}`volto_custom_addon`.

cross reference: section
: **Using headers as anchors**

  If you have a page at myfolder/mypage.md (relative to your documentation root) with the following structure:

      # Title

      ## My Subtitle

  Then the autosectionlabel feature will allow you to reference the section headers like so:

      {ref}`path/to/file_1:My Subtitle`

: **Create explicit anchor**

  create anchor
  ```
  (volto-custom-addon-final-label)=
  ```
  create link
  ```
  Switch to section [Release a Volto add-on](/mastering-plone/volto_custom_addon.html#volto-custom-addon-final-label).
  ```
  ```
  Switch to section {ref}`Release a Volto add-on <volto-custom-addon-final-label>`.
  ```

image
:     ![Volto add-on volto-accordion-block](_static/volto_addon_accordion_display.png)
: with zoom

      ```{image} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block
      :width: 100%
      ```

code block
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

code snippet expandable
: Be aware of the nested directives! Increase back ticks!

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

  To reference terms in your glossary, use the {term} role.
  
  For example, ``{term}`ReactJS` `` becomes a reference to term {term}`ReactJS`.

: Add glossary term

  Add your term to `/about/glossary.md`


Solutions of Exercises
: Collapsed Solutions

      ````{admonition} Complete code of the component
      :class: toggle

      ```{code-block} jsx
      :linenos:
      :emphasize-lines: 2,4

      import React from 'react';
      import { defineMessages, injectIntl } from 'react-intl';
      import { v4 as uuid } from 'uuid';
      import { omit, without } from 'lodash';
      ```
      ````

````{admonition} Complete code of the component
:class: toggle

```{code-block} jsx
:linenos:
:emphasize-lines: 2,4

import React from 'react';
import { defineMessages, injectIntl } from 'react-intl';
import { v4 as uuid } from 'uuid';
import { omit, without } from 'lodash';
```
````


