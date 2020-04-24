.. _volto-component-label:

From Viewlet to Component
=========================

.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout


To be solved task in this part:

* Display sponsors on all pages sorted by level

In this part you will:

* Display data from collected content

Topics covered:

* Create React component
* Use React action of Volto to fetch data from Plone via REST API
* Localize your component
* Semantic UI components


.. _volto-component-component-label:

A component
-----------

.. only:: not presentation

  A component is a block of information independent of the content of the current page. It can be placed in various locations on a site, even multiple times on one page.

* Inspect existing components with the React developer tools.
* Volto comes with several components like header, footer, sidebar. In fact everything in Volto is build of nested components.

.. _volto-component-sponsors-label:

Sponsors component
------------------

We will now see how to achieve in the new frontend the equivalent to the viewlet of the previous chapter :doc:`dexterity_3`.

The sponsors shall live in the footer. To modify the given footer component we copy the Footer.jsx file from Volto to our app regarding the original folder structure but inside our customizations folder :file:`customizations/components/theme/Footer/Footer.jsx`.

.. only:: not presentation

  In this file we can now modify the returned html by adding a subcomponent *Sponsors* which we have to create.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 9

    const Footer = ({ intl }) => (
      <>
        <Segment
          role="contentinfo"
          vertical
          padded
        >
          <Container>
            <Sponsors />
            ...

.. only:: not presentation

  We import this to be created component at the top of our new footer component with a

.. code-block:: jsx
    :linenos:

    import { Sponsors } from '../../../../components'; TODO path of subcomponent

.. only:: not presentation

    This shows an additional component.

    * It is visible on all content.
    * Later on it can be made conditional if necessary.

To create the component *Sponsors* we add a folder Sponsors components/Sponsors and a file components/Sponsors.jsx

.. only:: not presentation

  In this file we can now define our new component as a class that extends Component. It calls the action getQueryStringResults from @plone/volto/actions
  For this it is not necessary to understand the redux way to store data in the global app store but you need to know that Volto actions fetching data do use the redux store to store fetched data.

  So if we call the action getQueryStringResults to fetch data of sponsors, that means data of Plone portal types "Sponsor", then we can access this data from the store.

  The **connection** to the store is made by the following code which passes the data of the store to the component prop *items*.

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

We call the action in lifecycle event componentDidMount.

.. code-block:: jsx
    :linenos:

    componentDidMount() {
      this.props.getQueryStringResults('/', {...toSearchOptions, fullobjects: 1}, 'sponsors');
    }

With the data fetched and accessible in component prop *items* we can render the sponsors data:

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


We create a presentation component *SponsorsBody* in components/Sponsors/SponsorsBody.jsx

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


Restart your frontend and see the new footer:

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
