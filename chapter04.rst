
4. Simple Customisations (45min) (Philip)
=========================================

 * Configuring Plone with /plone_control_panel
 * Portlets
 * Viewlets
 * ZMI (plus intro to ZMI)
 * portal_actions


Configuring Plone with /plone_control_panel
-------------------------------------------

Click name
Click "Site Setup"

1. Add-ons (later...)
2. Calendar
3. Configuration Registry
4. Content Rules (we know this already)
5. Discussion
6. Editing
7. Errors
8. HTML Filtering
9. Image Handling
10. Language
11. Mail
12. Maintenance
13. Markup
14. Navigation
15. Search
16. Security
17. Site
18. Themes
19. TinyMCE Visual Editor
20. Types
21. Users and Groups
22. Workflow Manager
23. Zope Management Interface (here be dragons)


Portlets
---------

explain portlets:

* ``@@manage-portlets``
* UI fit for smart content-editors
* explain various types
* inheritance
* managing them
* ordering/weighting
* will be replaced by tiles?

Example:

* right: add static portlet "Sponsors".


Viewlets
--------

* ``@@manage-viewlets``
* no UI - not for content-editors
* not locally addable, no configurable inheritance
* will be replaced by tiles?
* the code is much simpler (we'll create one tomorrow)
* viewlet-manager
* ttw-reordering only within the same viewlet-manager
* the programer descides when it's where and what it shows

Portlets save Data, Viewlets usually don't. Viewlets are often used for UI-Elements.

example: hide collophon


ZMI
---

Köln ist eine Stadt die über 1000 Jahre alt ist. Es gibt heutzutage aber keine Infrastruktur mehr die von den Römern geschaffen und von uns noch genutzt werden. Zope ist der Unterbau von Plone und der Altersunterschied zwischen Zope und Plone ist wesentlich geringer als zwischen Köln und Colonia, aber als Kölner muss man Köln ja auch mal erwähnen. Aber in einem Aspekt hinkt der Vergleich nicht, wenn man im modernen Köln Mist baut, wird man nicht den Löwen zum Frass vorgeworfen, im alten Zope/Colonia kann das passieren. Es gibt Dinge die man dort nicht tun sollte, weil Plone dadurch kaputt geht. Wenn man doch etwas in Zope machen muss, ist das normalerweise gut auf Plone.org dokumentiert. Lustige Geschichten, wir sich andere (also wir noch nie!) In den Fuss geschossen haben erzählen wir gerne beim Social Event. Daher werden wir erst später was zu Zope und dem Zope Management Interface, ZMI erzählen.


Actions
-------

Go into the ZMI (explain ``/manage``)

Mostly links but really flexible links :-)

Manchmal soll ein Link aber mehr Eigenschaften haben, Links sollten eine Beschreibung haben können, und Bedingungen, zum Beispiel der Kontext oder ein benötigtes Recht. Ausserdem sollte das ganze Konfigurierbar sein, ohne das wir dazu HTML anpassen müssen. Dazu gibt es in Plone schon seit dem alten Rom das Konzept der Portal Actions. Dort werden kleine Objekte angelegt mit all diesen Eigenschaften, und im HTML werden diese Objekte, die Actions heissen abgefragt und entsprechend Texte geschrieben, Icons angezeigt und dergleichen.

Ein Beispiel für diese Links sind die grauen Reiter oben. Wir nehmen nun den Link auf die Startseite raus, die Besucher können auch auf das Logo klicken.

Kräftig durchatmen, wir sind nun in den Katakomben dem ZMI, bitte nichts berühren, sonst stürzt alles ein ;-)

go to ``portal_actions`` > ``portal_tabs``

Where is my navigation?

The navigation shows content-objects, which are in Plone's root. Plus all actions in portal_tabs

explain & edit index_html

Derzeit gibt es nur diese eine, die wir uns vor dem Löschen ganz kurz anschauen, bitte drauf klicken

Add a link to the imprint to the bottom:

go to ``site_actions`` (we know that because we checked in manage-viewlets) > add a CMF Actions ``'imprint' and point it at string:${globals_view/navigationRootUrl}/imprint``

Explain permissions, condition,

If time explain:

* user > undo (cool!)
* user > login/logout

