Addons - advanced topics
------------------------

Q: Is it possible to customize Volto with an addon?
A: Yes, the code path used is the same, so you can use the same convention.
Make sure you have the ``src/customizations`` folder inside your addon.

Q: Can I customize an addon?
A: Depends on the addon. The shadowing/customization mechanism relies on
non-relative import being used everywhere. If that addon uses relative import
paths, then it won't be possible right now to customize it. With that said, you
can customize files from an addon with the same algorithm used for Volto.
In the ``src/customizations`` folder, move any Volto customized files to the
``src/customizations/volto`` and then customize the addon by reconstructing the
full path (for example ``@plone/datatable-tutorial/CellRenderer/Progress.jsx``)
would be the fullpath for the file that customizes
``datatable-tutorial/src/CellRenderer/Progress.jsx``

Q: Can I have a theme in an addon?
A: Yes, you can alias the ``../../theme.config`` with a ``razzle.extend.js``
file in the addon root folder. Just don't customize the ``theme.config`` in the
project, don't add any files in the project's theme folder.

.. code-block:: jsx

    const modify = (config, { target, dev }, webpack) => {
      const themeConfigPath = `${__dirname}/theme/theme.config`;
      config.resolve.alias['../../theme.config$'] = themeConfigPath;
      config.resolve.alias['../../theme.config'] = themeConfigPath;

      return config;
    };

    module.exports = {
      modify,
    };

Some other stuff that addons can do:

- Register custom Express middleware. You could, for example, include a custom
  http proxy for ElasticSearch, expose it to the Volto frontend and avoid
  security issues. See volto-corsproxy for a redux-integrated CORS proxy

Bundle optimization
-------------------

Once you start approaching the project delivery, you'll need to check your
bundle sizes. Nobody wants to make their visitors wait for a 2 MB gzipped file
before the application becomes interactive.

Volto integrates a solution to split the generated JS code in "chunks", which
will then be loaded on-demand (when the component that uses them is loaded in
browser).

When dealing with React components, it's easy:

.. code-block:: jsx

    const Select = loadable(() => import('react-select'));

But for libraries it's a bit more difficult, as you have to manifest the
library as a React component, which gets passed as parameter to a render prop:

.. code-block:: jsx

    const D3 = loadable.lib(() => import('d3'));

    const FormattedValue = ({ value }) => {
      return (
        <D3 fallback={null}>
          {(d3) => d3.format(value)}
        </D3>
      );
    };

You can analyze your bundle by running:

.. code-block:: sh

    BUNDLE_ANALYZE=true yarn build

If you're running automated builds you can configure a new bundle analyzer with
static output, to save the report in a static html file. See
webpack-bundle-analyzer docs.
