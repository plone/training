# MyST parser - Markdown support in Sphinx

To support Markdown-based documentation, Sphinx can use MyST-Parser.

## Configuration and setup

Documentation for this can be found at [https://www.sphinx-doc.org/en/master/usage/markdown.html](https://www.sphinx-doc.org/en/master/usage/markdown.html)

If you haven't done so already, please follow the [instructions to build the training docu locally](https://training.plone.org/5/mastering-plone/about_mastering.html#building-the-documentation-locally)

Inside your Sphinx project:

- `pip install -—upgrade myst-parser`

in conf.py:

```py
extensions = [
  # ...
  "myst_parser"
]

myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    # "dollarmath",
    # "html_admonition",
    # "html_image",
    # "linkify",
    # "replacements",
    # "smartquotes",
    # "substitution",
    # "tasklist",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

```

- [Configuration — Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-source_parsers)

## converting rst to myst - rst2myst

There is a pandoc conversion available for converting rst to plain Markdown, but then you need to manually adjust a lot of the specific rst features.
The benefit of the `rst2myst` conversion is that it automatically converts some of the basic rst features into the correct MyST syntax.

### procedure

Inside your Sphinx project:

`pip install rst-to-myst`

Convert all files in a specific folder, eg. `transmogrifier`

- dry run:
  `rst2myst convert --dry-run transmogrifier/*.rst`

- for real, converting all rst files inside the folder `transmogrifier`

  `rst2myst convert transmogrifier/*.rst`

  `rst2myst convert transmogrifier/**/*.rst`

- run `make html` after all is converted to see the result

### notes

- The conversion shows you which extensions were used during conversion.
  We should add all used extensions to `myst_enable_extensions` inside the global `conf.py`.

```console
mastering-plone-myst/zpt.rst -> mastering-plone-myst/zpt.md
CONVERTED (extensions: ['deflist', 'colon_fence'])
mastering-plone-myst/zpt_2.rst -> mastering-plone-myst/zpt_2.md
CONVERTED (extensions: ['colon_fence'])

FINISHED ALL! (extensions: ['deflist', 'colon_fence'])
```

In this example, only the extensions `code-fence` and `deflist` were used.

### found issues

#### mastering-plone training

- The conversion renders warnings on several files:

```console
mastering-plone-myst/volto_custom_addon2.rst -> mastering-plone-myst/volto_custom_addon2.md
RENDER WARNING:235: no visit method for: <class 'docutils.nodes.line_block'>
RENDER WARNING:235: no depart method for: <class 'docutils.nodes.line_block'>
RENDER WARNING:235: no visit method for: <class 'docutils.nodes.line'>
RENDER WARNING:235: no depart method for: <class 'docutils.nodes.line'>
...
```

- In the example this is caused by a `|` at the beginning of line 235 in the original `volto_custom_addon2.rst` file, which is used when you want something to be rendered as a line blocks (see [docutils documentation on line blocks](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#line-blocks)

#### transmogrifier training

- seems to work perfectly, except for `.. glossary::`
  could be replaced with a definition list if we remove the `.. glossary::` line from the top of the file
- using the myst extension for deflist enables using the same syntax for definition lists as in rst:

```rst
Term 1
: Definition

Term 2
: Definition
```

## links

- [MyST - Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/index.html)
- [GitHub - executablebooks/rst-to-myst: Convert ReStructuredText to MyST Markdown](https://github.com/executablebooks/rst-to-myst)
- [Extended Guide — RST-to-MyST: v0.3.1](https://rst-to-myst.readthedocs.io/en/latest/usage.html)
- [Sphinx extension usage guide](https://myst-parser.readthedocs.io/en/latest/sphinx/use.html#migrate-pre-existing-rst-into-myst)
