---
html_meta:
  "description": "Guide to Sphinx, MyST, and Markdown"
  "keywords": "Sphinx, MyST, Markdown"
---

# Guide for Authors

## MyST, Markdown, Sphinx

We use [MyST, or Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/), a rich and extensible flavor of Markdown, for authoring training documentation.

Meta Tags
: You can improve the findability of a chapter in search engines by adding meta tags.

      ---
      html_meta:
            "description": "directives and other examples in markdown / MySt"
            "keywords": "Sphinx, MyST, markdown"
      ---

Cross Reference: chapter
: Link to another chapter.
:     We created an add-on in the last chapter {doc}`volto_custom_addon`.

Cross Reference: section
: Link to a section of a chapter

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

: with caption:

      ```{figure} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block

      Accordion Block
      ```

: with zoom:

      ```{figure} _static/volto_addon_accordion_display.png
      :alt: Volto add-on volto-accordion-block
      :width: 100%
      ```

Code Block
: example code `Python`

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

The lexers check the syntax. Be sure to provide valid code for a correct highlighting.

jsx does not allow a tick `'` in nodes.

```jsx
import React from 'react';

const TalkView = props => {
  return <div>I'm the TalkView component!</div>;
};

export default TalkView;
```

```jsx
import React from 'react';

const TalkView = props => {
  return <div>I am the TalkView component!</div>;
};

export default TalkView;
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

Notes and other highlighted blocks
: To highlight a block you can use the directives `note`, `warning`, `attention`, `caution`, `danger`, `error`, `hint`, `important`, `tip` 

      ```{tip}
      You can find the list with the global Semantic UI variables available in `omelette/theme/themes/default/globals/site.variables`.
      ```


```{tip}
You can find the list with the global Semantic UI variables available in `omelette/theme/themes/default/globals/site.variables`.
```

Glossary
: Reference glossary terms

  To reference terms in your glossary, use the `{term} role`.    
  For example, ``{term}`ReactJS` `` becomes a reference to term {term}`ReactJS`.

: Add glossary term

  Add your term to `/glossary.md`

Modes
: The training is rendered using Sphinx and builds in two flavors:

  default
  : The verbose version used for the online documentation and for the trainer.
  : Build it in Sphinx with `make html` or use the online version [training.plone.org](https://training.plone.org). See {doc}`/contributing/setup-author`.

  presentation
  : An abbreviated version used for the projector during a training.
  : It should use more bullet points than verbose text.
  : Build it in Sphinx with `make presentation`.

  With directive `{only} not presentation` you can control
  that a block is used for the presentation version only.

      ```{only} not presentation
      You can extend the functionality of your Dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

      But if you want to use this adapter, you must somehow know that an object implements that.
      Also, adding more fields to an object would not be easy with such an approach.
      ```

  To hide a block from the presentation version use `{only} not presentation`.

      ```{only} presentation
      You can extend the functionality of your Dexterity object by writing an adapter that adapts your dexterity object to add another feature or aspect.

      But if you want to use this adapter, you must somehow know that an object implements that.
      Also, adding more fields to an object would not be easy with such an approach.
      ```

  Content without a directive will be included in both versions.

