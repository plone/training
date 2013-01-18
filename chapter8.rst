

8. Creating your own eggs to customize Plone (15min) (Patrick)
==============================================================

 * creating plonekonf.talk with zopeskel/templer
 * what's in an egg?

Eigener Code von uns muss in ein egg. Ein Egg ist eine Zip Datei oder ein
Verzeichnis das einige Konventionen einhalten muss. Wir machen es uns hier
einfach und verwenden templer. Mit templer kann man ein Anwendungsskelett
erstellen, und muss nur noch die Lücken ausfüllen.
Noch haben wir ZopeSkel aber nicht, wir müssen es noch über unser
Buildout installieren.
Dazu gehen wir nun in das src Verzeichnis, und rufen folgendes auf:
zopeskel
Dann:
zopeskel dexterity
Description: Plonekonferenz Talk
Wir gehen die Fragen durch
Wir gehen die Verzeichnisse durch
Wir tragen das Egg in buildout ein.

ZCML:
    Konfigurationssprache um das Zopetoolkit Komponententsystem zu
    konfigurieren

Grok:
    Alternative Konfigurationssprache zu ZCML.

Genericsetup:
    Konfiguration die in der Plone Datenbank gespeichert ist kann
    hiermit importiert und exportiert werden.

Nachdem wir alles eingetragen haben, starten wir Zope und aktivieren die Erweiterung in Plone.

Nun noch schnell ein wenig Scaffolding für später!
Wir legen im static Verzeichnis 2 Dateien an, plonekonf.css und
plonekonf.js

Dann gehen wir in das ZMI... und tragen die Ressourcen in
portal_javascripts und portal_css ein.
Plone hat eine Ressourcenverwaltung für CSS und Javascript Dateien,
mit der man Plone noch ein wenig effizienter machen kann.
Die Standardeinstellungen hier reichen in der Regel.

Nun haben wir Anpassungen gemacht die in der ZODB gespeichert
wurden. Diese wollen aber auch versionieren, dafür ist Genericsetup
da.

Wieder im ZMI, gehen wir nun nach portal_setup, und exportieren dort
die JS und CSS Einstellungen. Wir bekommen eine ZIP Datei, welche
die XML Dateien enthält, die wir haben wollen. Wir kopieren diese in
das Profilverzeichnis und passen sie an.

Wir müssen lediglich unsere eigenen Dateien hier rein schreiben,
Genericsetup löscht nicht die anderen Einträge, und es fügt auch
nicht die Dateien doppelt ein.

If this is your first egg, this is a very special moment. We are going to create the egg with a script that pregenerates a lot of necessary files. They all are necessary, but sometimes in a sublte way. It takes a while do understand their full meaning. Only this year I learnt and understood why I should have a manifest.in file. You can get along without one, but trust me, you get along better with a proper manifste file.
Lets have a look at it.
bootstrap.py, buildout.cfg CHANGES.txt CONTRIBUTORS.txt docs/* README.txt setup.py
configure.zcml metadata.xml

