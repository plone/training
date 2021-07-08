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
  ...
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
- [python 3.x - Sphinx and Markdown .md links - Stack Overflow](https://stackoverflow.com/questions/52496591/sphinx-and-markdown-md-links)

## converting rst to myst - rst2myst

There is a pandoc conversion available for converting rst to plain Markown, but then you need to manually adjust a lot of the specific rst features.
The benefit of the `rst2myst` converison is that it automatically converts some of the basic rst features into the correct MyST syntax.

### procedure

Inside your Sphinx project:

`pip install rst-to-myst[sphinx]`

Convert all files in a specific folder, eg. _transmogrifier/_

- dry run:
  `rst2myst convert --dry-run transmogrifier/*.rst`

- for real, converting all rst files inside the folder _transmogrifier_
  `rst2myst convert transmogrifier/*.rst`
  `rst2myst convert transmogrifier/**/*.rst`

- run `make html` after all is converted to see the result

### notes

- the conversion shows you which extensions were used during conversion, we should add all used extensions to `myst_enable_extensions` inside the global conf.py

```console
mastering-plone-myst/zpt.rst -> mastering-plone-myst/zpt.md
CONVERTED (extensions: ['deflist', 'colon_fence'])
mastering-plone-myst/zpt_2.rst -> mastering-plone-myst/zpt_2.md
CONVERTED (extensions: ['colon_fence'])

FINISHED ALL! (extensions: ['deflist', 'colon_fence'])
```

in this case only `code-fence` and `deflist`

### found issues

#### mastering-plone training

- render warnings on several files:

```console
mastering-plone-myst/volto_custom_addon2.rst -> mastering-plone-myst/volto_custom_addon2.md
RENDER WARNING:235: no visit method for: <class 'docutils.nodes.line_block'>
RENDER WARNING:235: no depart method for: <class 'docutils.nodes.line_block'>
RENDER WARNING:235: no visit method for: <class 'docutils.nodes.line'>
RENDER WARNING:235: no depart method for: <class 'docutils.nodes.line'>
...
```

#### transmogrifier training

- seems to work perfectly, except for ::: glossary :::
  could be replaced with definition list if we remove the surrounding `:::` and use the same syntax for deflist as in rst, see example in `transmogrifier-myst/about/glossary.md`

## links

- [MyST - Markedly Structured Text](https://myst-parser.readthedocs.io/en/latest/index.html)
- [GitHub - executablebooks/rst-to-myst: Convert ReStructuredText to MyST Markdown](https://github.com/executablebooks/rst-to-myst)
- [Extended Guide — RST-to-MyST: v0.3.1](https://rst-to-myst.readthedocs.io/en/latest/usage.html)
- [Sphinx extension usage guide](https://myst-parser.readthedocs.io/en/latest/sphinx/use.html#migrate-pre-existing-rst-into-myst)
