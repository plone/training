.. _volto-component-label:
======================
The Sponsors Component
======================

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about the react frontent Volto.

  Solve the same tasks in classic frontend in chapter :doc:`viewlets_advanced_classic`


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout


In the previous chapter :doc:`deterity_3` you created the ``sponsor`` content type.
Now let's learn how to display them at the bottom of every page.

To be solved task in this part:

* Display sponsors on all pages sorted by level

In this part you will:

* Display data from collected content

Topics covered:

* Create React component
* Use React action of Volto to fetch data from Plone via REST API
* Localize your component
* Semantic UI components


.. note::

  For sponsors we will stay with the default view since we will only display the sponsors in the footer and not on their own pages.
  The default-view of Volto does not show any of the custom fields you added to the sponsors.
  Using what you learned in :doc:`volto_talkview` you should be able to write a view for sponsors if you wanted to.


.. _volto-component-component-label:

A component
===========

React Components let you split the UI into independent, reusable pieces, and think about each piece in isolation.

* You can write a view component for the current context - like the ``TalkView``.
* You can write a view components that can be selected as views for content objects - like the TalkListView.
* You can also write components that are visible on all content objects. In classic Plone we used *Viewlets* for that.

* Inspect existing components with the React developer tools.
* Volto comes with several components like header, footer, sidebar. In fact everything in Volto is build of nested components.


.. _volto-component-sponsors-label:

Sponsors component
==================

We will now see how to achieve in the new frontend the equivalent to the viewlet of the chapter :doc:`dexterity_3`.

Overriding the Footer
---------------------

The sponsors shall live in the footer. To modify the given footer component we copy the Footer.jsx file from Volto to our app regarding the original folder structure but inside our customizations folder :file:`frontend/src/customizations/components/theme/Footer/Footer.jsx`.

You will find the original footer in :file:`frontend/omelette/src/components/theme/Footer/Footer.jsx`

.. only:: not presentation

  In this file we can now modify the returned html by adding a subcomponent *Sponsors* which we have to create.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 12

    ...
    const Footer = ({ intl }) => (
      <Segment
        role="contentinfo"
        vertical
        padded
        inverted
        color="grey"
        textAlign="center"
      >
        <Container>
          <Sponsors />
          <Segment basic inverted color="grey" className="discreet">
          ...

.. only:: not presentation

  We import this to be created component at the top of our new footer component with a

.. code-block:: jsx
    :linenos:

    import { Sponsors } from '../../../../components';

.. todo::

  Explain paths of subcomponents

.. only:: not presentation

    This shows an additional component.

    * It is visible on all content.
    * Later on it can be made conditional if necessary.

To create the component ``Sponsors`` we add a folder :file:`frontend/src/components/Sponsors/` and a file :file:`Sponsors.jsx` in it.

In this file we can now define our new component as a class that extends Component.

As usual you should start with a placeholder to see if your registration actually works:

..  code-block:: js
    :linenos:

    import React, { Component } from 'react';
    class Sponsors extends Component {
      render() {
        return <h2>We ❤ our sponsors</h2>;
      }
    }
    export default Sponsors;

This should now show up on all pages in the footer.


Getting the sponsors data
-------------------------

The component will use the action ``getQueryStringResults`` from ``@plone/volto/actions`` to fetch data of all sponsors.

.. todo::

    Why use getQueryStringResults? How and why is this different to what we did in the talklistview?

    So far not explained:

    * props
    * actions
    * store
    * compose
    * injectIntl

    Go step by step with working code for each step.

For this it is not necessary to understand the Redux way to store data in the global app store.
You only need to know that Volto actions that fetch data use the redux store to store fetched data.

So if we call the action ``getQueryStringResults`` to fetch data of sponsors, that means data of the portal types ``sponsor``, then we can access this data from the store.

The **connection** to the store is made by the following code which passes the data of the store to the component prop ``items``.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 5

    export default compose(
      injectIntl,
      connect(
        state => ({
          items: state.querystringsearch.subrequests.sponsors?.items || [],
        }),
        { getQueryStringResults },
      ),
    )(Sponsors);

We call this action in the lifecycle event ``componentDidMount``:

.. code-block:: jsx
    :linenos:

    componentDidMount() {
      this.props.getQueryStringResults('/', {...toSearchOptions, fullobjects: 1}, 'sponsors');
    }


Pass prepared data for presentation
-----------------------------------

With the data fetched and accessible in the component prop ``items`` we can then render the sponsors data:

.. code-block:: jsx
    :linenos:

    render() {
      const sponsorlist = this.props.items;
      return (
        <>
         <SponsorsBody sponsorlist={sponsorlist} />
        </>
    )}

.. only:: not presentation

  Keep in mind this common pattern to split a component in two parts: a container component to fetch data and a presentation component to render a presentation.

.. todo::

    Add final code of ``Sponsors.jsx`` to copy.


The presentation component
--------------------------

We create a presentation component ``SponsorsBody`` in :file:`frontend/src/components/Sponsors/SponsorsBody.jsx`

Presentation component means that this is a stateless component which gets the necessary data via props and renders the data of sponsors grouped by sponsor level.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 33

    /**
     * sponsors presentation
     * @function SponsorsBody
     * @param {Array} sponsorlist list of sponsors with name, level, logo.
     * @returns {string} Markup of the component.
     `*/`
    const SponsorsBody = ({sponsorlist}) => {
      // ...

      const sponsors = groupedSponsors(sponsorlist);

      return (
        <Segment
          basic
          textAlign="center"
          className="sponsors"
          aria-label="Sponsors"
          inverted>
          <div className="sponsorheader">
            <h3 className="subheadline">
              <FormattedMessage
                id="Our sponsors do support and are supported of Plone."
                defaultMessage="Our sponsors do support and are supported of Plone."
              />
            </h3>
            <h2 className="headline">
            <FormattedMessage
              id="We ❤ our sponsors"
              defaultMessage="We ❤ our sponsors"
            />
            </h2>
          </div>
            {levelList()}
        </Segment>
      )
    }

    export default SponsorsBody

.. todo::

    Add final code of ``SponsorsBody.jsx`` to copy.


Reload your frontend and see the new footer:

.. figure:: _static/volto_component_sponsors.png



.. _volto-component-exercise-label:

Exercise
--------

Modify the component to display a sponsor logo as a link to the sponsors website. The address is set in sponsor field "url". See the documentation of `Semantic UI React <https://react.semantic-ui.com/elements/image/#types-link>`_.

..  admonition:: Solution
    :class: toggle

    .. code-block:: jsx
        :linenos:
        :emphasize-lines: 3-5

        <Image
          className="logo"
          as="a"
          href={item.url}
          target='_blank'
          src={flattenToAppURL(item.logo.scales.preview.download)}
          size="small"
          alt={item.title}
          title={item.level?.title + ' ' + item.title}
        />

    The Semantic Image component is now rendered with a wrapping anchor tag.

    .. code-block:: html
        :linenos:

        <a
          target="_blank"
          title="Gold Sponsor Violetta Systems"
          class="ui small image logo"
          href="https://www.nzz.ch">
            <img
              src="/sponsors/violetta-systems/@@images/d1db77a4-448d-4df3-af5a-bc944c182094.png"
              alt="Violetta Systems">
        </a>
