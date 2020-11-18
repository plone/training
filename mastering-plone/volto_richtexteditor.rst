.. _volto_richtexteditor-label:

Rich Text Editor Settings
=========================

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about customizing the rich text editor.


  .. topic:: Description

      Add a button / feature to the rich text editor.


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout


The rich text editor lets editors make text bold, italic and more. This chapter is about adding an additional button to the editor toolbar to make text lighter.

To be solved task in this part:

* Enrich text editor

In this part you will:

* Learn about configuration of your Volto app in general.

Topics covered:

* Configuration of a Volto app
* Rich text editor DraftJS

.. figure:: _static/volto_richtexteditor_edit.jpg
   :alt: mark text as discreet / mark text with a style via css class name

.. figure:: _static/volto_richtexteditor.jpg
   :alt: text marked as discreet

The `settings` in :file:`/src/config.js` is the place to modify the general configuration of your Volto app. Here we add info about the additional button, what to display in the editor bar and what to do when the button is clicked.

:file:`/src/config.js`

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 3,4,8

    export const settings = {
      ...defaultSettings,
      richTextEditorInlineToolbarButtons: newbuttonset,
      ToHTMLRenderers: {
        ...defaultSettings.ToHTMLRenderers,
        inline: {
          ...defaultSettings.ToHTMLRenderers.inline,
          ...customInline,
        },
      },
    };

You see that two attributes of the overall `settings`, `richTextEditorInlineToolbarButtons` and `ToHTMLRenderers`, are overwritten. We define these attributes to show a button which lets the editor add a CSS class *discreet* to a selected phrase.

:file:`/src/config.js`

.. code-block:: jsx
    :linenos:

    import React from 'react';
    import createInlineStyleButton from 'draft-js-buttons/lib/utils/createInlineStyleButton';
    import Icon from '@plone/volto/components/theme/Icon/Icon';
    import radiodisabledSVG from '@plone/volto/icons/radio-disabled.svg';

    // Button
    const DiscreetButton = createInlineStyleButton({
      style: 'DISCREET',
      children: <Icon name={radiodisabledSVG} size="24px" />,
    });
    let newbuttonset = defaultSettings.richTextEditorInlineToolbarButtons;
    newbuttonset.splice(2, 0, DiscreetButton);

    // Renderer
    const customInline = {
      DISCREET: (children, { key }) => (
        <span key={key} className="discreet">
          {children}
        </span>
      ),
    };



.. admonition:: Complete code of the configuration in :file:`/src/config.js`
    :class: toggle

    ..   code-block:: jsx
      :linenos:

      import React from 'react';
      import createInlineStyleButton from 'draft-js-buttons/lib/utils/createInlineStyleButton';
      import Icon from '@plone/volto/components/theme/Icon/Icon';
      import radiodisabledSVG from '@plone/volto/icons/radio-disabled.svg';

      // Button
      const DiscreetButton = createInlineStyleButton({
        style: 'DISCREET',
        children: <Icon name={radiodisabledSVG} size="24px" />,
      });
      let newbuttonset = defaultSettings.richTextEditorInlineToolbarButtons;
      newbuttonset.splice(2, 0, DiscreetButton);

      // Renderer
      const customInline = {
        DISCREET: (children, { key }) => (
          <span key={key} className="discreet">
            {children}
          </span>
        ),
      };

      export const settings = {
        ...defaultSettings,
        richTextEditorInlineToolbarButtons: newbuttonset,
        ToHTMLRenderers: {
          ...defaultSettings.ToHTMLRenderers,
          inline: {
            ...defaultSettings.ToHTMLRenderers.inline,
            ...customInline,
          },
        },
      };
