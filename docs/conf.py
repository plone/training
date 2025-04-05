# Configuration file for the Sphinx documentation builder.
# Plone Training documentation build configuration file


# -- Path setup --------------------------------------------------------------

from datetime import datetime

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------

project = "Plone Training"
copyright = "Plone Foundation"
author = "Plone community"
trademark_name = "Plone"
now = datetime.now()
year = str(now.year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = year
# The full version, including alpha/beta/rc tags.
release = year


# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*")
# or your custom ones.
extensions = [
    "myst_parser",
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinx_tippy",
    "sphinxext.opengraph",
]

# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# Options for the linkcheck builder
linkcheck_anchors = True
# Ignore localhost
linkcheck_ignore = [
    r"https?://.*localhost.*",
    r"http://0.0.0.0",
    r"http://127.0.0.1",
    r"http://example.com",
    r"https://github.com/plone/training/issues/new/choose",  # requires auth
    r"https://github.com/search",  # always rate limited, causes linkcheck to stall
    r"https://docs.github.com/en/get-started/.*",  # GitHub docs require auth
    r"https://www.linode.com/.*",  # tests say 500 Server Error, but manually they work
    # ### Start of list of anchored links
    # Prior to each PloneConf, uncomment these lines to verify that the links work,
    # although the anchor cannot be found.
    # GitHub rewrites anchors with JavaScript.
    # See https://github.com/plone/training/issues/598#issuecomment-1105168109
    # Ignore github.com pages with anchors
    r"https://github.com/.*#.*",
    # Ignore other specific anchors
    # ### End of list of anchored links
]
linkcheck_allowed_redirects = {
    # All HTTP redirections from the source URI to the canonical URI will be treated as "working".
}
linkcheck_retries = 1
linkcheck_report_timeouts_as_broken = True
linkcheck_timeout = 5

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "plone_sphinx_theme"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"
# The default value includes icon-links, so override it with that one omitted, and add it to html_theme_options[footer_content_items].
html_sidebars = {
    "**": [
        "navbar-logo",
        "search-button-field",
        "sbt-sidebar-nav",
    ]
}

html_theme_options = {
    "article_header_start": ["toggle-primary-sidebar", "chapter-title"],
    "extra_footer": """<p>The text and illustrations in this website are licensed by the Plone Foundation under a Creative Commons Attribution 4.0 International license. Plone and the Plone® logo are registered trademarks of the Plone Foundation, registered in the United States and other countries. For guidelines on the permitted uses of the Plone trademarks, see <a href="https://plone.org/foundation/logo">https://plone.org/foundation/logo</a>. All other trademarks are owned by their respective owners.</p>
    <p>Pull request previews by <a href="https://readthedocs.org/">Read the Docs</a>.</p>""",
    "footer_content_items": [
        "author",
        "copyright",
        "last-updated",
        "extra-footer",
        "icon-links",
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/plone/documentation",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "Mastodon",
            "url": "https://plone.social/@plone",
            "icon": "fa-brands fa-mastodon",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "YouTube",
            "url": "https://www.youtube.com/@PloneCMS",
            "icon": "fa-brands fa-youtube",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
        {
            "name": "X (formerly Twitter)",
            "url": "https://x.com/plone",
            "icon": "fa-brands fa-square-x-twitter",
            "type": "fontawesome",
            "attributes": {
                "target": "_blank",
                "rel": "noopener me",
                "class": "nav-link custom-fancy-css"
            }
        },
    ],
    "logo": {
        "text": "Plone Training 2025",
    },
    "navigation_with_keys": True,
    "path_to_docs": "docs",
    "repository_branch": "main",
    "repository_url": "https://github.com/plone/training",
    "search_bar_text": "Search",
    "show_toc_level": 2,
    "use_edit_page_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
}

# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://6.docs.plone.org"

html_css_files = ["custom.css", ("print.css", {"media": "print"})]
html_extra_path = [
    "robots.txt",
]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for MyST markdown conversion to HTML -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "attrs_block",  # Support parsing of block attributes.
    "attrs_inline",  # Support parsing of inline attributes.
    "colon_fence",  # You can also use ::: delimiters to denote code fences, instead of ```.
    "deflist",  # Support definition lists. https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "html_image",  # For inline images. See https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#html-images
    "linkify",  # Identify "bare" web URLs and add hyperlinks.
    "strikethrough",  # See https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-strikethrough
    "substitution",  # Use Jinja2 for substitutions. https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#substitutions-with-jinja2
]


# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
intersphinx_mapping = {
    "plone5docs": ("https://5.docs.plone.org/", None),
    "plone6docs": ("https://6.docs.plone.org/", None),
    "python": ("https://docs.python.org/3/", None),
    "training2024": ("https://2024.training.plone.org/", None),
    "training2023": ("https://2023.training.plone.org/", None),
    "training2022": ("https://2022.training.plone.org/", None),
}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://training.plone.org/"
ogp_description_length = 200
ogp_image = "https://training.plone.org/_static/Plone_logo_square.png"
ogp_site_name = "Plone Training"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- Options for sphinx.ext.todo -----------------------

# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True


# -- Options for sphinx-notfound-page ----------------------------------

notfound_urls_prefix = ""
notfound_template = "404.html"


# -- Options for sphinx_sitemap to HTML -----------------------------

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://training.plone.org/"
# https://sphinx-sitemap.readthedocs.io/en/latest/advanced-configuration.html#customizing-the-url-scheme
sitemap_url_scheme = "{link}"


# -- sphinx-tippy configuration ----------------------------------
tippy_anchor_parent_selector = "article.bd-article"
tippy_enable_doitips = False
tippy_enable_wikitips = False
tippy_props = {
    "interactive": True,
    "placement": "auto-end",
}
