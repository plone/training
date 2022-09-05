---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Advanced Diazo

**"Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology."**

To do this, Diazo does some real complicated stuff on your behalf: it writes XSLT!

But sometimes basic rules are not enough and you need to write a bit of XLST yourself.

## Modify Theme And Content On The Fly

Let's look at some examples from the [official diazo docs](http://docs.diazo.org/en/latest/advanced.html#modifying-the-theme-on-the-fly).

### Extend Rules

You can [re-use or extend rules](http://docs.diazo.org/en/latest/advanced.html#xinclude)
from another theme or from another file in your theme.

A good example of a use case is the one described by
[Asko Soukka](https://twitter.com/datakurre)  (thanks!!!) in this blog post about
[how to  Customize Plone 5 default theme on the fly](http://datakurre.pandala.org/2015/05/customize-plone-5-default-theme-on-fly.html).

### Include External Content

You can [include external content](http://docs.diazo.org/en/latest/advanced.html#including-external-content)
from another website or from a custom view.

## Recipes And Snippets

- The docs provide [a basic recipe set](http://docs.diazo.org/en/latest/recipes/index.html) and you can have your own, but how to remember and re-use them?
- [David Bain introduces a "diazo snippets library"](http://blog.dbain.com/2014/12/introducing-diazo-snippets-library.html) that allows you to get snippets from a chrome extensions.
- [All the snippets are available here](http://pigeonflight.github.io/lessArcane/).

### More Snippets

#### Make Some Links Open In New Window

```xml
<!-- add target="_blank" to all links in portlet-collection-links -->
<xsl:template match="//dl[contains(@class,'portlet-collection-links')]//a">
  <a target="_blank"><xsl:apply-templates select="./@*[contains(' href title class rel ', concat(' ', name(), ' '))]"/><xsl:value-of select="." /></a>
</xsl:template>
```

At [diazo.org](http://docs.diazo.org/en/latest/recipes/adding-an-attribute/index.html) is another way described.

#### Add CSS Marker Classes Depending On Existing `portal-columns`

This adds a CSS class for every existing `portal-column` to the `body` tag.
If `portal-column-one` exists, we add `col-one`;
if `portal-column-content` exists, we add `col-content`;
and if `portal-column-two` exists, we add `col-two`.

```xml
<before theme-children="/html/body" method="raw">
  <xsl:attribute name="class">
    <xsl:value-of select="/html/body/@class" />
    <xsl:if css:test="#portal-column-one"> col-one</xsl:if>
    <xsl:if css:test="#portal-column-content"> col-content</xsl:if>
    <xsl:if css:test="#portal-column-two"> col-two</xsl:if>
  </xsl:attribute>
</before>
```

Now, one can use these markers to define the grid in a semantic way like this:

```less
body.col-one.col-content.col-two #content-wrapper {
  .make-row();

  #portal-column-content {
    .make-lg-column(6);
    .make-lg-column-offset(3);
  }

  #portal-column-one {
    .make-lg-column(3);
    .make-lg-column-pull(9);
  }

  #portal-column-two {
    .make-lg-column(3);
  }
}
body.col-content #content-wrapper {
  .make-row();

  #portal-column-content {
    .make-lg-column(12);
  }
}
```

```{note}
This way, you don't need the xsl-rules Barceloneta uses to create the main content area.
It's more flexible than Barceloneta's approach.

Another way could be, to change Plone to provide these classes already ;).
```

#### Move Plone Elements Around

Sometimes one needs to move Plone elements from one place to another or merge some elements together.
In the following example we merge the language flags together with the document actions.

```xml
<replace css:content-children=".documentActions > ul">
  <xsl:for-each select="//*[@class='documentActions']/ul/li">
    <xsl:copy-of select="." />
  </xsl:for-each>
  <xsl:for-each select="//*[@id='portal-languageselector']/*">
    <xsl:copy-of select="." />
  </xsl:for-each>
</replace>
```

#### Taking Over Specific Portlets

```xml
<!-- all portal-column-two portlets but not portletNews and not portletEvents -->
<after
  content="//div[@id='portal-column-two']//dl[not(contains(@class,'portletNews')) and not(contains(@class,'portletEvents'))]"
  css:theme-children="#portal-column-two"
  />
```

```xml
<!-- all portal-column-one portlets but not portletNavigationTree -->
<after
  content="//div[@id='portal-column-one']//dl[not(contains(@class,'portletNavigationTree'))]"
  css:theme-children='#portal-column-two'
  />
```
