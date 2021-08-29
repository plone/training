# Instructions for contributors: markdown

cross reference chapter
:     Let's start with our fresh add-on we created in the last chapter {doc}`volto_custom_addon`.

cross reference anchor
: create anchor
  ```
  (volto-custom-addon-final-label)=
  ```
: create link
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

code snippet expandable
: Be aware of the nested directives. Increase back ticks.

      ````{admonition} Complete code for ReactJS component
      :class: dropdown

      Here's my code snippet

      Maecenas sed diam eget risus varius blandit sit amet non magna. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Nullam quis risus eget urna mollis ornare vel eu leo. Duis mollis, est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Etiam porta sem malesuada magna mollis euismod. Nulla vitae elit libero, a pharetra augue.


      ```{code-block} jsx
      :linenos: true

      import React, { useState } from 'react';
      ```
      ````
