Extending Dexterity-Types with Behaviors
========================================

* What are Behaviours?


simple social behavior
----------------------

* Behavior "IVoteable"
* The Plone API

The behavior needs a bunch of features:

* It needs to store the votes somewhere
* It needs some logic to process the votes

We could use schema fields, but these would be visible in the edit view.
But what we store does not really adapt very well to standard form elements.

We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations.
Annotations in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without coliding.

The current implementation, which is not the official API is just a dictionary under the attribute name __annotations__ When I want to get my annotations, I ask for a specific value of that dictionary.

So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so must be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisisons.

Additionally, we are no
We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations.
Annotations in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without coliding.

The current implementation, which is not the official API is just a dictionary under the attribute name __annotations__ When I want to get my annotations, I ask for a specific value of that dictionary.

So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so must be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisisons.

Additionally, we are not
We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations.
Annotations in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without coliding.

The current implementation, which is not the official API is just a dictionary under the attribute name __annotations__ When I want to get my annotations, I ask for a specific value of that dictionary.

So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so must be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisisons.

Additionally, we are not
We are going to store the information in an annotation. Not because it is needed but because you will find code that uses annotations.
Annotations in Zope/Plone mean that data won't be stored directly on an object but in an indirect way and with namespaces so that multiple packages can store information under the same attribute, without coliding.

The current implementation, which is not the official API is just a dictionary under the attribute name __annotations__ When I want to get my annotations, I ask for a specific value of that dictionary.

So using annotations avoids namespace conflicts. The cost is an indirection. The dictionary is persistent so must be stored separately. Also, one could give attributes a name containing a namespace prefix to avoid naming collisisons.

The attribute where we store our data will be declared as a schema field. We set permissions so that it will never be displayed, because we are not going to create z3c.form widgets for displaying them. We do provide a schema, because many other packages use the schema information to get knowledge of the relevant fields.
For example, when files have been migrated to blobs, new objects had to be created and every schema field was copied. The code can't know about our field, except if we provide schema information.






Was jetzt noch fehlt ist die Funktionalität, Stimmen abzugeben.
Damit die Menschen abstimmen können, benötigen wir:

* Einen Ort zum Abspeichern von Stimmabgaben,
* Eine Logik um aus den Stimmen einen Durchschnitt zu berechnen
* Eine Möglichkeit, den Durchschnitt anzugeben
* Eine Möglichkeit, eine Stimme abzugeben

Wir könnten einfach Stimmen als Feld hinzufügen, aber dann müsste
man die Felder verstecken und die ganze Logik in den Views machen.

Stattdessen schreiben wir ein Behavior. Ein Behavior ist so ähnlich
wie ein Adapter. Ein Adapter adaptiert einen bestimmten Typ. Ein
Behavior kann prinzipiell für alle Inhalte verwendet werden, und
bei Dexterity Content Typen kann man zur Laufzeit ein Behavior einem
Contenttyp zuweisen. Dank dem Annotations Adapter kann man beliebige
Daten einem Objekt hinzufügen ohne zu riskieren, Daten von anderen
zu überschreiben. Ausserdem kann man auch noch einstellen, das
Objekte die dieses Behavior unterstützen ein Marker Interface
bekommen. Durch das Marker Interface kann man diesen Objekten eigene
Views, Viewlets oder auch Portlets zuweisen.


Writing the Behavior
--------------------

Viel Code, zunächst kümmern wir uns darum, den Context weg zu
speichern. Dann holen wir uns die Annotations. Der Annotationadapter
ist ein Standardweg, zusätzliche Informationen auf einem Objekt zu
speichern. Der Adapter implementiert eigentlich nur folgenes:
Er speichert ein PeristentDict auf dem Attribute ``__annotations__`` und
liefert dieses zurück. Wer etwas speichern möchte, muss sich einen
möglichst eindeutigen Schlüssel ausdenken, wir nehmen den Namen
unserer Klasse.

Dann schreiben wir ein wenig Code um sicherzustellen, das unsere
Datenstruktur schon da ist.

Warum initalisieren wir das Dict mit version 1 und nicht mit Version 2?

Wir haben evtl. schon Objekte mit Daten, aber noch mit der alten
Version an Daten. Dieses Objekt wird beim ersten neuen Laden auf den
aktuellen Stand gebracht.

Die nächste Methode, _hash ist ein wenig Magie um halbwegs
sicherzustellen, das jemand nicht mehrfach abstimmt. Wer Langeweile
hat kann seine DSL Verbindung trennen, wieder aufbauen und nochmal
abstimmen.

Nun kommt das Herzstück, die vote Methode. Das Userinterface erlaubt
eigentlich nicht, zweimal abzustimmen, trotzdem fangen wir das ab
und werfen eine Exception. Wenn diese Exception ausgelöst wird,
kriegt der Nutzer eine hässliche Fehlermeldung, aber er ist sowieso
nur ein kleiner Hacker. Wir speichern nicht nur die Bewertung,
sondern auch einen Hash des Requestobjekts, um sicherzustellen, das
der Nutzer nicht mehrfach abstimmt.

Nun kommt die Methode zur Berechnung der Durchschnittsstimmen.

Wir speichern die Daten wie folgt:
self.annotations['votes'][-1] = "Anzahl der -1 Stimmen
self.annotations['votes'][0] = "Anzahl der 0 Stimmen
self.annotations['votes'][+1] = "Anzahl der +1 Stimmen

Wir multiplizieren nun einfach die Anzahl der Stimmen mit dem
Stimmenschlüssel, summerieren die einzelnen Ergebnisse und teilen
diese Zahl durch die Gesamtzahl der Stimmen.

has_votes benötigen wir für views, wir wollen kein
Durchschnittsrating abgeben, wenn noch keiner abgestimmt hat.

already_voted wird im Userinterface verwendet um Leute kein
Stimmrecht zu geben, wenn sie schon abgestimmt haben.

clear Wir haben beim Testen festgestellt, das es sehr hilfreich ist,
mal eben schnell die Stimmen alle zu löschen.

.. code-block:: bash

    $ git checkout tutorial-7-behavior

Ergänzen wir nun unsere Listenansicht um das Durchschnittsvoting.

.. code-block:: bash

    $ git checkout tutorial-8-listview-mit-behavior

Ok, wie stimmen wir nun ab?

