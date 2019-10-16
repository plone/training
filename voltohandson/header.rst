.. _voltohandson-header-label:

======
Header
======

Logo
====

Starting with the Logo, we use `component shadowing <#component-shadowing>`_ to customize (and override) Volto original components.
Get the Plone logo (`Logo.svg`) from the `training-resources` directory and copy it using this path and name: ``src/customizations/components/theme/Logo/Logo.svg``.

.. note:: Every time you add a file to the customizations folder or to the theme folder, you must restart the server for changes to take effect.
          From that on, the hot reloading should kick-in and reload the page automatically.

Header component
================

We will customize the existing Volto header, since the one we want doesn't differ much from the original.
We will do so by copying the original Volto ``Header`` component from the ``omelette`` folder into the ``customizations/components/theme/Header/Header.jsx``.

We have to do some amendments to that component, such as removing the search widget, and moving the ``Anontools`` component.

This will be the outcome:

.. code-block:: js

    import { Logo, Navigation } from '@plone/volto/components';

    ...

    render() {
      return (
        <Segment basic className="header-wrapper" role="banner">
          <Container>
            <div className="header">
              <div className="logo-nav-wrapper">
                <div className="logo">
                  <Logo />
                </div>
                <Navigation pathname={this.props.pathname} />
              </div>
            </div>
          </Container>
        </Segment>
      );
    }

.. warning:: When using component shadowing remember to replace any relative import with ``@plone/volto``.

Header styling
==============

We will start introducing the basic styling for the header. We use the ``themes/extras/custom.overrides`` to apply general styling to our site theme.

.. note:: Use this rule of thumb when building Volto themes. Use the default Semantic overrides system when the override is site-wide and applies to Semantic components.
          When using your own components and specific theme styling, then use ``custom.overrides``. Applying styling in this later is much faster than doing it in the Semantic default components.

We want this styling in the Header component:

.. code-block:: less

    .ui.basic.segment.header-wrapper {
      background-color: #191919;
      border-bottom: 1px solid #939393;
      margin-bottom: 20px;
    }

    .ui.basic.segment .header .logo-nav-wrapper {
      justify-content: space-between;
    }

    .logo .ui.image {
      height: 50px;
    }

So we have the familiar black background of plone.com, the right logo height, and the proper flex distribution for the header elements.
Please notice the specificity of the CSS class declarations.
We need them in order to override the original theme. This is rather common when overriding SemanticUI theme styles due to the high specificity that SemanticUI enforces.

We adjust the navigation menu for match plone.com one:

.. code-block:: less

    .navigation .ui.secondary.pointing.menu {
      min-height: initial;
      margin: 0;

      a.item {
        padding: 5px 10px !important;
        margin: 0;
        border: none;
        color: #fff;
        font-size: 14px;
        font-weight: bold;

        &:not(:last-child) {
          margin-right: 5px;
        }

        &:hover {
          background: #212020;
          color: #00a1df;
        }
      }
    }

Then we adjust the margin for the homepage:

.. code-block:: less

    .siteroot .ui.basic.segment.header-wrapper {
      margin-bottom: 0;
    }

Component shadowing
===================

We use a technique using **component shadowing** to override an existing component in Volto and use our local custom version, without having to modify Volto's source code at all.
You have to place the replacing component in the same original folder path inside the ``src/customizations`` folder.

.. note:: Component shadowing is very much the same as the good old Plone technique named JBOT, but you can customize virtually any module in Volto, actions and reducers too, not only components.
