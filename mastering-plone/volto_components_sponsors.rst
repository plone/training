.. _viewlets1-label:

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

* Component

.. _viewlets1-sponsors-label:

A component for the sponsors in the footer
------------------------------------------

.. only:: not presentation

    A component is a block of information independendent of the content of the current page that can be put in various places in the site.

* Inspect existing components with the React developer tools.
* Volto comes with several components like header, footer, sidebar. In fact everything in Volto is build of nested components.

.. _viewlets1-sponsors2-label:

Sponsors component
------------------

The sponsors shall live in the footer. To modify the given footer we copy the Footer.jsx file from Volto to our app regarding the original folder structure but inside our customizations folder :file:`customizations/components/theme/Footer/Footer.jsx`.

In this file we can now modify the returned html by adding a subcomponent *Sponsors* which we have to create.

.. code-block:: jsx
    :linenos:

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

We import this to be created component at the top of our new footer component with a

.. code-block:: jsx
    :linenos:

    import { Sponsors } from '../../../../components'; TODO path of subcomponent

.. only:: not presentation

    This shows an additional component.

    * It is visible on all content.
    * Later on it can be made conditional if necessary.

To create the component *Sponsors* we add a folder Sponsors components/Sponsors and a file components/Sponsors.jsx

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

      asyncConnect([
        {
          key: 'querystringsearch',
          promise: ({ store: { dispatch } }) =>
            dispatch(
              getQueryStringResults(
                '/',
                {...toSearchOptions, fullobjects: 1},
                'sponsors'
              ),
            ),
        },
      ]),

    )(Sponsors);

We call the action in lifecycle event UNSAFE_componentWillMount.

.. code-block:: jsx
    :linenos:

    UNSAFE_componentWillMount() {
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

Keep in mind this common pattern to split a component in two parts: a container component to fetch data and a presentation component to render a presentation.


We create a presentation component *SponsorsBody* in components/Sponsors/SponsorsBody.jsx

This is a stateless component which gets the necessary data via props and renders the sponsors grouped by sponsor level and some sugar.






**TODO To be continued here**

The viewlet class :py:class:`FeaturedViewlet` is expected in a file :file:`browser/viewlets.py`.

.. _BrowserLayer: https://docs.plone.org/develop/plone/views/layers.html?highlight=browserlayer#introduction

.. code-block:: python
    :linenos:

    from plone.app.layout.viewlets import ViewletBase

    class FeaturedViewlet(ViewletBase):
        pass


.. only:: not presentation

    This class does nothing except rendering the associated template (That we have yet to write)

Let's add the missing template :file:`templates/featured_viewlet.pt`.

.. code-block:: html
    :linenos:

    <div id="featured">
        <p tal:condition="python:view.is_featured">
            This is hot news!
        </p>
    </div>


.. only:: not presentation

    As you can see this is not a valid HTML document.
    That is not needed, because we don't want a complete view here, a HTML snippet is enough.

    There is a :samp:`tal:define` statement, querying for :samp:`view/is_featured`.
    Same as for views, viewlets have access to their class in page templates, as well.

We have to extend the Featured Viewlet now to add the missing attribute:


.. only:: not presentation

    .. sidebar:: Why not to access context directly

        In this example, :samp:`IFeatured(self.context)` does return the context directly.
        It is still good to use this idiom for two reasons:

          #. It makes it clear that we only want to use the IFeatured aspect of the object
          #. If we decide to use a factory, for example to store our attributes in an annotation, we would `not` get back our context, but the adapter.

        Therefore in this example you could simply write :samp:`return self.context.featured`.

.. code-block:: python
    :linenos:
    :emphasize-lines: 2, 6-8

    from plone.app.layout.viewlets import ViewletBase
    from ploneconf.site.behaviors.featured import IFeatured

    class FeaturedViewlet(ViewletBase):

        def is_featured(self):
            adapted = IFeatured(self.context)
            return adapted.featured

So far, we

  * register the viewlet to content that has the IFeatured Interface.
  * adapt the object to its behavior to be able to access the fields of the behavior
  * return the link


.. _viewlets1-excercises-label:

Exercise 1
----------

Register a viewlet 'number_of_talks' in the footer that is only visible to admins (the permission you are looking for is :py:class:`cmf.ManagePortal`).
Use only a template (no class) to display the number of talks already submitted.

Hint: Use Acquisition to get the catalog (You know, you should not do this but there is plenty of code out there that does it...)

..  admonition:: Solution
    :class: toggle

    Register the viewlet in :file:`browser/configure.zcml`

    ..  code-block:: xml

        <browser:viewlet
          name="number_of_talks"
          for="*"
          manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
          layer="zope.interface.Interface"
          template="templates/number_of_talks.pt"
          permission="cmf.ManagePortal"
          />


    For the ``for`` and ``layer``-parameters ``*`` is shorthand for :py:class:`zope.interface.Interface` and the same effect as omitting them: The viewlet will be shown for all types of pages and for all Plone sites within your Zope instance.

    Add the template :file:`browser/templates/number_of_talks.pt`:

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog python:context.portal_catalog;
                         number_of_talks python:len(catalog(portal_type='talk'));">
            There are <span tal:replace="number_of_talks" /> talks.
        </div>

    :samp:`python:context.portal_catalog` will return the catalog through Acquisition. Be careful if you want to use path expressions: :samp:`context/portal_catalog` calls the catalog (and returns all brains). You need to prevent this by using :samp:`nocall:context/portal_catalog`.

    Relying on Acquisition is a bad idea. It would be much better to use the helper view ``plone_tools`` from :file:`plone/app/layout/globals/tools.py` to get the catalog.

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog context/@@plone_tools/catalog;
                         number_of_talks python:len(catalog(portal_type='talk', review_state='pending'));">
            There are <span tal:replace="number_of_talks" /> talks.
        </div>

    :samp:`context/@@plone_tools/catalog` traverses to the view ``plone_tools`` and calls its method :py:meth:`catalog`. In python it would look like this:

    ..  code-block:: html

        <div class="number_of_talks"
             tal:define="catalog python:context.restrictedTraverse('plone_tools').catalog();
                         number_of_talks python:len(catalog(portal_type='talk'));">
            There are <span tal:replace="number_of_talks" /> talks.
        </div>

    It is not a good practice to query the catalog within a template since even simple logic like this should live in Python.
    But it is very powerful if you are debugging or need a quick and dirty solution.

    In Plone 5 you could even write it like this:

    ..  code-block:: html

        <?python

        from plone import api
        catalog = api.portal.get_tool('portal_catalog')
        number_of_talks = len(catalog(portal_type='talk'))

        ?>

        <div class="number_of_talks">
            There are ${python:number_of_talks} talks.
        </div>


Exercise 2
----------

Register a viewlet 'days_to_conference' in the header.
Use a class and a template to display the number of days until the conference.

You get bonus points if you display it in a nice format (think "In 2 days" and "Last Month") by using either JavaScript or a Python library.

..  admonition:: Solution
    :class: toggle

    In :file:`configure.zcml`:

    ..  code-block:: xml

        <browser:viewlet
          name="days_to_conference"
          for="*"
          manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
          layer="*"
          class=".viewlets.DaysToConferenceViewlet"
          template="templates/days_to_conference.pt"
          permission="zope2.View"
          />

    In :file:`viewlets.py`:

    ..  code-block:: python

        from plone.app.layout.viewlets import ViewletBase
        from datetime import datetime
        import arrow

        CONFERENCE_START_DATE = datetime(2015, 10, 12)


        class DaysToConferenceViewlet(ViewletBase):

            def date(self):
                return CONFERENCE_START_DATE

            def human(self):
                return arrow.get(CONFERENCE_START_DATE).humanize()

    Setting the date in python is not very user-friendly. In the chapter :ref:`registry-label` you learn how store global configuration and easily create controlpanels.

    And in :file:`templates/days_to_conference.pt`:

    ..  code-block:: html

        <div class="days_to_conf">
            ${python: view.human()}
        </div>

    Or using the moment pattern in Plone 5:

    ..  code-block:: html

        <div class="pat-moment"
             data-pat-moment="format: relative">
            ${python: view.date()}
        </div>
