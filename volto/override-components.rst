.. _override_components-label:

===================
Override Components
===================

Override The Logo
=================

When we want to override a specific file we can create an alias pointing to
our own theme. So for example if we want to replace the logo, which is located
in Volto at :file:`components/theme/Logo/Logo.svg`, we will add an logo to
our theme and create an alias. The folder structure needs to match the folder
structure of Volto in the :file:`customizations` folder.

Excercise
=========

Replace the logo with a hello kitty logo.

Change The Tags Component
=========================

When we want to override a specific component it works exactly the same as the
above example with an image. Locate the `Tags.jsx` file and override this file so
that there is a label in front of the tags with: 'Tags:'.

..  admonition:: Solution
    :class: toggle

    ::

        /**
         * Tags component.
         * @module components/theme/Tags/Tags
         */

        import React from 'react';
        import { Link } from 'react-router-dom';
        import PropTypes from 'prop-types';
        import { Container } from 'semantic-ui-react';

        /**
         * Tags component class.
         * @function Tags
         * @param {array} tags Array of tags.
         * @returns {string} Markup of the component.
         */
        const Tags = ({ tags }) =>
          tags && tags.length > 0 ? (
            <Container>
              Tags:
              {tags.map(tag => (
                <Link className="ui label" to={`/search?Subject=${tag}`} key={tag}>
                  {tag}
                </Link>
              ))}
            </Container>
          ) : (
            <span />
          );

        /**
         * Property types.
         * @property {Object} propTypes Property types.
         * @static
         */
        Tags.propTypes = {
          tags: PropTypes.arrayOf(PropTypes.string),
        };

        /**
         * Default properties.
         * @property {Object} defaultProps Default properties.
         * @static
         */
        Tags.defaultProps = {
          tags: null,
        };

        export default Tags;
