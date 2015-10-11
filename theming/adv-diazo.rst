==============
Advanced Diazo
==============

    **"Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology."**

To do this diazo do some real complicated stuff on your behalf: it writes XSLT!

But sometimes basic rules are not enough and you need to write a bit of XLST your self.


Modify the theme and the content on the fly
===========================================

Let's see some example from the `official diazo docs <http://docs.diazo.org/en/latest/advanced.html#modifying-the-theme-on-the-fly>`_.


Extend rules
============

You can `re-use or extend rules <http://docs.diazo.org/en/latest/advanced.html#xinclude>`_ from another theme or from another file in your theme.

A good example of a use case is the one described by `Asko Soukka <https://twitter.com/datakurre>`_  (thanks!!!) in this blog post about `how to  Customize Plone 5 default theme on the fly <http://datakurre.pandala.org/2015/05/customize-plone-5-default-theme-on-fly.html>`_.


Include external content
========================

You can `include external content <http://docs.diazo.org/en/latest/advanced.html#including-external-content>`_ from another website or from a custom view.


Recipes and snippets
====================

The docs provide `a basic recipe set <http://docs.diazo.org/en/latest/recipes/index.html>`_ and you can have your own, but how to remember and re-use them?

`David Bain introduces a "diazo snippets library" <http://blog.dbain.com/2014/12/introducing-diazo-snippets-library.html>`_ that allows you to get snippets from a chrome extensions. `All the snippets are available here <http://pigeonflight.github.io/lessArcane/>`_.

More snippets
-------------

Make some links open in new window
**********************************

.. code-block:: xml

   <!-- add target="_blank" to all links in portlet-collection-links -->
   <xsl:template match="//dl[contains(@class,'portlet-collection-links')]//a">
     <a target="_blank"><xsl:apply-templates select="./@*[contains(' href title class rel ', concat(' ', name(), ' '))]"/><xsl:value-of select="." /></a>
   </xsl:template>

At diazo.org is another way described in the recipes: http://docs.diazo.org/en/latest/recipes/adding-an-attribute/index.html

Add CSS marker classes depending on existing portal-columns
***********************************************************

This adds a CSS class for every existing portal-column to the body tag. If portal-column-one exist we add col-one, if portal-column-content exsists we add col-content and if portal-column-two exists we add col-two.

.. code-block:: xml

   <before theme-children="/html/body" method="raw">
     <xsl:attribute name="class"><xsl:value-of select="/html/body/@class" /><xsl:if css:test="#portal-column-one"> col-one</xsl:if><xsl:if css:test="#portal-column-content"> col-content</xsl:if><xsl:if css:test="#portal-column-two"> col-two</xsl:if></xsl:attribute>
   </before>

Now one can use these markers to define the grid in a semantic way like this:

.. code-block:: css

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


Move plone elements around
**************************

Sometimes one need to move Plone elements from one place to another or merge some elements together. In the following example we merge the language flags together with the document actions.

.. code-block:: xml

   <replace css:content-children=".documentActions > ul">
     <xsl:for-each select="//*[@class='documentActions']/ul/li">
       <xsl:copy-of select="." />
     </xsl:for-each>
     <xsl:for-each select="//*[@id='portal-languageselector']/*">
       <xsl:copy-of select="." />
     </xsl:for-each>
   </replace>


Taking over specific portlets
*****************************

.. code-block:: xml

   <!-- all portal-column-two portlets but not portletNews and not portletEvents -->
   <after
     content="//div[@id='portal-column-two']//dl[not(contains(@class,'portletNews')) and not(contains(@class,'portletEvents'))]"
     css:theme-children="#portal-column-two"
     />

.. code-block:: xml

   <!-- all portal-column-one portlets but not portletNavigationTree -->
   <after
     content="//div[@id='portal-column-one']//dl[not(contains(@class,'portletNavigationTree'))]"
     css:theme-children='#portal-column-two'
     />

