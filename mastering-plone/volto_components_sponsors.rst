.. _volto-component-label:

======================
The Sponsors Component
======================

.. sidebar:: Volto chapter

  .. figure:: _static/Volto.svg
     :alt: Volto Logo

  This chapter is about the react frontent Volto.

  Solve the same tasks in classic frontend in chapter :doc:`viewlets_advanced_classic`


  .. topic:: Description

      Create a React component for content fetched from the backend

  .. contents:: Table of Contents
    :depth: 2
    :local:


.. sidebar:: Get the code! (:doc:`More info <code>`)

   Code for the beginning of this chapter::

       git checkout TODO tag to checkout

   Code for the end of this chapter::

        git checkout TODO tag to checkout


In the previous chapter :doc:`dexterity_3` you created the ``sponsor`` content type.
Now let's learn how to display content of this type.

To be solved task in this part:

* Advert to sponsors on all pages sorted by level

In this part you will:

* Display data from collected content

Topics covered:

* Create React component
* Use React action of Volto to fetch data from Plone via REST API
* Style component with Semantic UI


.. figure:: _static/volto_component_sponsors.png
   :alt: Sponsors component



.. only:: not presentation

  For sponsors we will stay with the default view as we will only display the sponsors in the footer and do not modify their own pages.
  The default-view of Volto does not show any of the custom fields you added to the sponsors.
  Using what you learned in :doc:`volto_talkview` you should be able to write a view for sponsors if you wanted to.


.. _volto-component-component-label:

A React component
-----------------

React Components let you split the UI into independent, reusable pieces, and think about each piece in isolation.

* You can write a view component for the current context - like the ``TalkView``.
* You can write a view component that can be selected as view for a set of content objects like the TalkListView.
* You can also write components that are visible on all content objects. In classic Plone we use *viewlets* for that.

* Volto comes with several components like header, footer, sidebar. In fact everything of the UI is build of nested components.
* Inspect existing components with the React Developer Tools.


.. _volto-component-sponsors-label:

The sponsors component
----------------------

We will now see how to achieve in Volto frontend the equivalent to the Plone viewlet of chapter :doc:`dexterity_3`.


**Steps to take**

* Copy and customize Footer component.
* Create component to fetch data from backend.
* Create component to display the fetched data.


.. _volto-component-customizing-label:

Customizing the Footer
----------------------

You can override any component that lives inside Volto's source folder ``frontend/omelette/src/components`` and adapt it to your needs, without touching the original component. 

The sponsors shall live in the footer of a page. To customize the given footer component we copy the ``Footer.jsx`` file :file:`frontend/omelette/src/components/theme/Footer/Footer.jsx` from Volto. We insert the copied file to our app regarding the original folder structure but inside our customizations folder :file:`frontend/src/customizations/components/theme/Footer/Footer.jsx`.


.. only:: not presentation

  In this file ``Footer.jsx`` we can now modify the to be rendered html by adding a subcomponent ``Sponsors``. 


  Be aware that the following code is JSX. JSX is Javascript that can handle html in a handy way. What you see is a component defined as an arrow function. The function returns markup consisting of enriched html: The tag ``<Sponsors />`` forces a rendering of the Sponsors component.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 4

    const Footer = ({ intl }) => (
      <Segment role="contentinfo" vertical padded>
        <Container>
          <Sponsors />
          <Segment
            basic
            inverted
            color="grey"
            textAlign="center"
            className="discreet"
          >

.. only:: not presentation

    This will show an additional component. It is visible on all pages as it is a subcomponent of footer. Later on it can be made conditional if necessary.

To create the component ``Sponsors`` we add a folder :file:`frontend/src/components/Sponsors/` with a file :file:`Sponsors.jsx`. In this file we can now define our new component.

Start with a placeholder to see if your registration actually works:

.. code-block:: jsx
    :linenos:

    import React, { Component } from 'react';

    class Sponsors extends Component {
      render() {
        return <h3>We ❤ our sponsors</h3>;
      }
    }

    export default Sponsors;

.. note::

  Defining a component as a class is the classic and still valid React way. We have already seen the new approach with *hooks* in chapter :doc:`volto_talk_listview`, ``TalkListView`` component.

The component is a class extending the template class ``Component``. As you see the minimum to define is a render method which returns some markup.


Go back to your modified ``Footer`` component. The ``Footer`` component needs to know where to find the added ``Sponsor`` component. We import the ``Sponsor`` component at the top of our modified ``Footer`` component.

:file:`frontend/src/customizations/components/theme/Footer/Footer.jsx`:

.. code-block:: jsx
    :linenos:

    import { Sponsors } from '../../../../components';

The path reflects the fact that ``Footer.jsx`` lives in ``frontend/src/customizations`` whereas ``Sponsors`` lives in ``frontend/src/components``.



After restarting the frontend with ``yarn start``, we are now ready to visit an arbitrary page to see the new component. A restart is necessary on newly added files. As long as you just edit existing files of your app, your browser is updating automagically by app configuration.


.. _volto-component-datafetching-label:

Getting the sponsors data
-------------------------

With our ``Sponsors`` component in place we can take the next step and explore Volto some more to figure out how it does data fetching.

As the data is in the backend, we need to find a way to address it. Volto provides various predefined actions to communicate with the backend (fetching data, creating content, editing content, etc). A Redux action (that communicates with the backend) has a common pattern: It addresses the backend via REST API and updates the global app store according to the response of the backend. A component calls an action and has hereupon access to the global app store (shortened: store) with the fetched data. 


For more information which actions are already provided by Volto have look at :file:`frontend/omelette/src/actions`. 

Our component will use the action ``getQueryStringResults`` to fetch data of all sponsors. It takes as arguments the path where to search, the information what to search and an argument with which key the data should be stored in the store. Remember: the result is stored in the global app store.

So if we call the action ``getQueryStringResults`` to fetch data of sponsors, that means data of the instances of portal type ``sponsor``, then we can access this data of the store.

The component traverses through a lifecycle (mounting, the moment where the raw structure is set, rendering, where the dynamic content is filled in, and some more lifecycle events). To have the necessary data for the rendering, we call the ``getQueryStringResults`` action on mounting the component. Therefor React has one of many lifecycle methods: ``componentDidMount``.
Find detailed information on lifecycles in the `React documentation: The Component Lifecycle <https://reactjs.org/docs/react-component.html#the-component-lifecycle>`_.


.. admonition:: Call of ``getQueryStringResults`` in the lifecycle event ``componentDidMount`` of our ``Sponsors`` component:
    :class: toggle

    .. code-block:: jsx
        :linenos:
        :emphasize-lines: 14-22,61-68

        /**
        * Sponsors component.
        * @module components/Sponsors/Sponsors
        */

        import React, { Component } from 'react';
        import PropTypes from 'prop-types';
        import { connect } from 'react-redux';

        import { getQueryStringResults } from '@plone/volto/actions';

        import SponsorsBody from './SponsorsBody';

        const toSearchOptions = {
          query: [
            {
              i: 'portal_type',
              o: 'plone.app.querystring.operation.selection.any',
              v: ['sponsor'],
            },
          ],
        };

        /**
        * Component to display the sponsors.
        * @class Sponsors
        * @extends Component
        */
        class Sponsors extends Component {
          /**
          * Property types.
          * @property {Object} propTypes Property types.
          * @static
          */
          static propTypes = {
            getQueryStringResults: PropTypes.func.isRequired,
            items: PropTypes.arrayOf(
              PropTypes.shape({
                '@id': PropTypes.string,
                '@type': PropTypes.string,
                title: PropTypes.string,
                description: PropTypes.string,
              }),
            ),
          };

          /**
          * Default (values of) properties.
          * @property {Object} defaultProps Default properties.
          * @static
          */
          static defaultProps = {
            items: [],
          };

          /**
          * Component did mount
          * @method componentDidMount
          * @returns {undefined}
          */
          componentDidMount() {
            // call action getQueryStringResults
            this.props.getQueryStringResults(
              '/',
              { ...toSearchOptions, fullobjects: 1 },
              'sponsors',
            );
          }

          /**
          * Component did update
          * @method componentDidUpdate
          * @param {Object} prevProps Previous properties
          * @returns {undefined}
          *
          * Update component when a new sponsor is created / deleted / updated.
          * Two steps are necessary:
          * - subscription of a value / of values in store that reflects
          *   the fact that a new sponsor is created / deleted / updated.
          * - call search action on property change; do it here in componentDidUpdate
          */
          componentDidUpdate(prevProps) {
            if (
              // content type instance created and instance is sponsor
              (this.props.subscribedValueContent.create.loaded &&
                this.props.subscribedValueContent.data['@type'] === 'sponsor' &&
                this.props.subscribedValueContent !==
                  prevProps.subscribedValueContent) ||
              // content pasted in /contents
              (this.props.subscribedValueClipboard.request.loaded &&
                this.props.subscribedValueClipboard !==
                  prevProps.subscribedValueClipboard) ||
              // content deleted
              (this.props.subscribedValueContent.delete.loaded &&
                this.props.subscribedValueContent !== prevProps.subscribedValueContent) ||
              // content updated
              (this.props.subscribedValueContent.update.loaded &&
                this.props.subscribedValueContent !== prevProps.subscribedValueContent)
            ) {
              // then call action getQueryStringResults
              this.props.getQueryStringResults(
                '/',
                { ...toSearchOptions, fullobjects: 1 },
                'sponsors',
              );
            }
          }

          /**
          * Render method.
          * @method render
          * @returns {string} Markup for the component.
          */
          render() {
            return <SponsorsBody sponsorlist={this.props.items} />;
          }
        }

        export default connect(
          state => ({
            items: state.querystringsearch.subrequests.sponsors?.items || [],
            // subsription of something in store that is updated on creation of a sponsor
            // see docstring componentDidUpdate
            subscribedValueContent: state.content,
            subscribedValueClipboard: state.clipboard,
          }),
          { getQueryStringResults },
        )(Sponsors);



.. _volto-component-store-label:

Connection of component and store
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's connect the store to our component. On export we define a mapping of the requested data of the store to props of the component. With the following code the prop *item* is set to the fetched sponsors data from the store. It's worth exploring the store of our app with the Redux Dev Tools (additional Dev Tools to React Dev Tools) There you can see what is stored like ``state.querystringsearch.subrequests.sponsors``. And you can walk through time and watch how the store is changing.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 2-4

    export default connect(
      state => ({
        items: state.querystringsearch.subrequests.sponsors?.items || [],
      }),
      { getQueryStringResults },
    )(Sponsors);

A further mapping enables the component to use the action `getQueryStringResults`. The following code maps the action to the prop of the component. What you see is a shortened definition. Read more on actions and store in `Volto documentation <https://training.plone.org/5/volto/actions-reducers.html>`_

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 5

    export default connect(
      state => ({
        items: state.querystringsearch.subrequests.sponsors?.items || [],
      }),
      { getQueryStringResults },
    )(Sponsors);

With these both mappings in place, the component can call the predefined action `getQueryStringResults` and has access to the fetched data via `this.props.items`.

The next step is advanced and can be skipped on a first reading. As by now we fetch the sponsors data on mounting event of the component. The mounting is done once on the first visit of a page of our app. 
What if a new sponsor is added? We want to achieve a re-rendering of the component on changed sponsorship. To subscribe to these changes in sponsorship, we extend our already defined connection.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 4-7

    export default connect(
      state => ({
        items: state.querystringsearch.subrequests.sponsors?.items || [],
        // subsription of something in store that is updated on creation of a sponsor
        // see docstring componentDidUpdate
        subscribedValueContent: state.content,
        subscribedValueClipboard: state.clipboard,
      }),
      { getQueryStringResults },
    )(Sponsors);

Listening to this subscription the component shall fetch the data from the store if necessary. For this the component calls the same action as before also in lifecycle event ``componentDidUpdate``.

.. code-block:: jsx
    :linenos:
    :emphasize-lines: 31-35

    /**
    * Component did update
    * @method componentDidUpdate
    * @param {Object} prevProps Previous properties
    * @returns {undefined}
    *
    * Update component when a new sponsor is created / deleted / updated.
    * Two steps are necessary:
    * - subscription of a value / of values in store that reflects
    *   the fact that a new sponsor is created / deleted / updated.
    * - call search action on property change; do it here in componentDidUpdate
    */
    componentDidUpdate(prevProps) {
      if (
        // content type instance created and instance is sponsor
        (this.props.subscribedValueContent.create.loaded &&
          this.props.subscribedValueContent.data['@type'] === 'sponsor' &&
          this.props.subscribedValueContent !==
            prevProps.subscribedValueContent) ||
        // content pasted in /contents
        (this.props.subscribedValueClipboard.request.loaded &&
          this.props.subscribedValueClipboard !==
            prevProps.subscribedValueClipboard) ||
        // content deleted
        (this.props.subscribedValueContent.delete.loaded &&
          this.props.subscribedValueContent !== prevProps.subscribedValueContent) ||
        // content updated
        (this.props.subscribedValueContent.update.loaded &&
          this.props.subscribedValueContent !== prevProps.subscribedValueContent)
      ) {
        // then call action getQueryStringResults
        this.props.getQueryStringResults(
          '/',
          { ...toSearchOptions, fullobjects: 1 },
          'sponsors',
        );
      }
    }
      


.. _volto-component-container-presentation-label:

Pass prepared data for presentation
-----------------------------------

With the data fetched and accessible in the component prop ``items`` we can
now render the sponsors data:

.. code-block:: jsx
    :linenos:

    render() {
      return <SponsorsBody sponsorlist={this.props.items} />;
    }


.. admonition:: Complete code of the ``Sponsors`` component
    :class: toggle

    .. code-block:: jsx
        :linenos:
        :emphasize-lines: 3

        /**
         * Sponsors component.
         * @module components/Sponsors/Sponsors
         */

        import React, { Component } from 'react';
        import PropTypes from 'prop-types';
        import { connect } from 'react-redux';

        import { getQueryStringResults } from '@plone/volto/actions';

        import SponsorsBody from './SponsorsBody';

        const toSearchOptions = {
          query: [
            {
              i: 'portal_type',
              o: 'plone.app.querystring.operation.selection.any',
              v: ['sponsor'],
            },
          ],
        };

        /**
        * Component to display the sponsors.
        * @class Sponsors
        * @extends Component
        */
        class Sponsors extends Component {
          /**
          * Property types.
          * @property {Object} propTypes Property types.
          * @static
          */
          static propTypes = {
            getQueryStringResults: PropTypes.func.isRequired,
            items: PropTypes.arrayOf(
              PropTypes.shape({
                '@id': PropTypes.string,
                '@type': PropTypes.string,
                title: PropTypes.string,
                description: PropTypes.string,
              }),
            ),
          };

          /**
          * Default (values of) properties.
          * @property {Object} defaultProps Default properties.
          * @static
          */
          static defaultProps = {
            items: [],
          };

          /**
          * Component did mount
          * @method componentDidMount
          * @returns {undefined}
          */
          componentDidMount() {
            // call action getQueryStringResults
            this.props.getQueryStringResults(
              '/',
              { ...toSearchOptions, fullobjects: 1 },
              'sponsors',
            );
          }

          /**
          * Component did update
          * @method componentDidUpdate
          * @param {Object} prevProps Previous properties
          * @returns {undefined}
          *
          * Update component when a new sponsor is created / deleted / updated.
          * Two steps are necessary:
          * - subscription of a value / of values in store that reflects 
          *   the fact that a new sponsor is created / deleted / updated.
          * - call search action on property change; do it here in componentDidUpdate
          */
          componentDidUpdate(prevProps) {
            if (
              // content type instance created and instance is sponsor
              (this.props.subscribedValueContent.create.loaded &&
                this.props.subscribedValueContent.data['@type'] === 'sponsor' &&
                this.props.subscribedValueContent !==
                  prevProps.subscribedValueContent) ||
              // content pasted in /contents
              (this.props.subscribedValueClipboard.request.loaded &&
                this.props.subscribedValueClipboard !==
                  prevProps.subscribedValueClipboard) ||
              // content deleted
              (this.props.subscribedValueContent.delete.loaded &&
                this.props.subscribedValueContent !== prevProps.subscribedValueContent) ||
              // content updated
              (this.props.subscribedValueContent.update.loaded &&
                this.props.subscribedValueContent !== prevProps.subscribedValueContent)
            ) {
              // then call action getQueryStringResults
              this.props.getQueryStringResults(
                '/',
                { ...toSearchOptions, fullobjects: 1 },
                'sponsors',
              );
            }
          }

          /**
          * Render method.
          * @method render
          * @returns {string} Markup for the component.
          */
          render() {
            return <SponsorsBody sponsorlist={this.props.items} />;
          }
        }

        export default connect(
          state => ({
            items: state.querystringsearch.subrequests.sponsors?.items || [],
            // subsription of something in store that is updated on creation of a sponsor
            // see docstring componentDidUpdate
            subscribedValueContent: state.content,
            subscribedValueClipboard: state.clipboard,
          }),
          { getQueryStringResults },
        )(Sponsors);




.. only:: not presentation

  .. note::

      Keep this common pattern in mind: splitting a component in two parts: a container component to fetch data and a presentation component to render a presentation.



.. _volto-component-presentation-label:

The presentation component
--------------------------

We create a presentation component ``SponsorsBody`` in :file:`frontend/src/components/Sponsors/SponsorsBody.jsx`.

Presentation component means that it is a stateless component which gets the necessary data via props from the parent component. It doesn't communicate with the global app store, does not fetch data, doesn't do elaborated logic, it just renders the passed data of sponsors.

Start with a simple component.

.. code-block:: jsx
    :linenos:

    import React from 'react';
    import { Segment } from 'semantic-ui-react';

    const SponsorsBody = ({ sponsorlist }) => {
      return (
        <div>
          <h3>We ❤ our sponsors</h3>
        </div>
      );
    };

    export default SponsorsBody;

You see the component receives the data of the parent component *Sponsors* via prop *sponsorlist*.

Restart your frontend with ``yarn start`` and see the new footer. A restart is necessary as we added a new file ``SponsorsBody.jsx``.

Exercise
^^^^^^^^

Extend the code by displaying the list of sponsors. The data is available via prop *sponsorlist*.

..  admonition:: Solution
    :class: toggle

      .. code-block:: jsx
        :linenos:
        :emphasize-lines: 12-28

        <Segment
          basic
          textAlign="center"
          className="sponsors"
          aria-label="Sponsors"
          inverted
        >
          <div className="sponsorheader">
            <h3 className="subheadline">We ❤ our sponsors</h3>
          </div>
          {sponsorlist?.length && (
            <List>
              {sponsorlist.map(item => (
                <List.Item key={item['UID']} className="sponsor">
                  {item.logo ? (
                    <Image
                      className="logo"
                      src={flattenToAppURL(item.logo.scales.preview.download)}
                      size="small"
                      alt={item.title}
                      title={item.title}
                    />
                  ) : (
                    <a href={item['@id']}>{item.title}</a>
                  )}
                </List.Item>
              ))}
            </List>
          )}
        </Segment>
    
    This is just one solution. You achieved to display the data? That's great! You'll see in the next step why we use <List>, <List.Item> and <Image> components and how to use Semantic UI components to simplify your code.


We group the sponsors by sponsorship level.

An Object *sponsors* using the sponsorship level as key helps to build rows with sponsors by sponsorship level. 

The Semantic UI compontent *Image* is used to display the logo. It cares about the markup of an html image node with all necessary attributes in place.

We also benefit from Semantic UI component *List* to build our list of sponsors. The styling can be customized but these predefined components help simplifying the code and achieve an app wide harmonic style. 

.. seealso::

    Chapter :doc:`volto_semantic_ui`


.. code-block:: jsx
    :linenos:
    :emphasize-lines: 23-50

    const SponsorsBody = ({ sponsorlist }) => {
      const groupedSponsorsByLevel = array =>
        array.reduce((obj, item) => {
          obj[item.level.token] = obj[item.level.token]
            ? obj[item.level.token].push(item)
            : [item];
          return obj;
        }, {});
      const sponsors = groupedSponsorsByLevel(sponsorlist);

      return (
        <Segment
          basic
          textAlign="center"
          className="sponsors"
          aria-label="Sponsors"
          inverted
        >
          <div className="sponsorheader">
            <h3 className="subheadline">We ❤ our sponsors</h3>
          </div>
          {sponsorlist?.length && (
            <List>
              {Object.keys(sponsors).map(level => {
                return (
                  <List.Item key={level} className={'sponsorlevel ' + level}>
                    <h3>{level.toUpperCase()}</h3>
                    <List horizontal>
                      {sponsors[level].map(item => (
                        <List.Item key={item['UID']} className="sponsor">
                          {item.logo ? (
                            <Image
                              className="logo"
                              src={flattenToAppURL(
                                item.logo.scales.preview.download,
                              )}
                              size="small"
                              alt={item.title}
                              title={item.title}
                            />
                          ) : (
                            <a href={item['@id']}>{item.title}</a>
                          )}
                        </List.Item>
                      ))}
                    </List>
                  </List.Item>
                );
              })}
            </List>
          )}
        </Segment>
      );
    };


.. admonition:: Complete code of the presentation component ``SponsorsBody`` component
    :class: toggle

    .. code-block:: jsx
        :linenos:

        import React from 'react';
        import { Segment, List, Image } from 'semantic-ui-react';
        import { flattenToAppURL } from '@plone/volto/helpers';

        /**
        * sponsors presentation
        * @function SponsorsBody
        * @param {Array} sponsorlist list of sponsors with name, level, logo.
        * @returns {string} Markup of the component.
        */
        const SponsorsBody = ({ sponsorlist }) => {
          const groupedSponsorsByLevel = array =>
            array.reduce((obj, item) => {
              obj[item.level.token] = obj[item.level.token]
                ? obj[item.level.token].push(item)
                : [item];
              return obj;
            }, {});
          const sponsors = groupedSponsorsByLevel(sponsorlist);

          return (
            <Segment
              basic
              textAlign="center"
              className="sponsors"
              aria-label="Sponsors"
              inverted
            >
              <div className="sponsorheader">
                <h3 className="subheadline">We ❤ our sponsors</h3>
              </div>
              {sponsorlist?.length && (
                <List>
                  {Object.keys(sponsors).map(level => {
                    return (
                      <List.Item key={level} className={'sponsorlevel ' + level}>
                        <h3>{level.toUpperCase()}</h3>
                        <List horizontal>
                          {sponsors[level].map(item => (
                            <List.Item key={item['UID']} className="sponsor">
                              {item.logo ? (
                                <Image
                                  className="logo"
                                  src={flattenToAppURL(
                                    item.logo.scales.preview.download,
                                  )}
                                  size="small"
                                  alt={item.title}
                                  title={item.title}
                                />
                              ) : (
                                <a href={item['@id']}>{item.title}</a>
                              )}
                            </List.Item>
                          ))}
                        </List>
                      </List.Item>
                    );
                  })}
                </List>
              )}
            </Segment>
          );
        };

        export default SponsorsBody;




See the new footer. A restart is not necessary as we didn't added a new file. The browser updates automagically by configuration.

.. figure:: _static/volto_component_sponsors.png
   :alt: Sponsors component
   :align: center


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


.. volto-component-summary-label:

Summary
-------

You know how to fetch data from backend. With the data you are able to create a component displayed at any place in the website.


.. todo::

    Lookout
