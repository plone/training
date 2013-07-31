
6. Buildout I (30min) (Patrick)
===============================

You write a list of eggs you want to have. Buildout retrieves the eggs. In doing this, buildout retrieves the eggs, resolving dependencies, including dependencies where an egg states that it must have a specific minimum or maximum version of another egg. Buildout can also create configuration files and folder. Plone, for example, needs a folder to writes it logfiles into, a folder for the database and multiple configuration files. All of this is assembled by buildout. The Unified installer created configuration files already. Let's have a look at them now.

The syntax of buildout configuration files is similar to classic ini files. You write a parameter name, an equals sign and the value. If you enter another value in the next line and indent it, buildout understands that both values belong to the parameter name, and the parameter receives a list of all values. Here is an example::

    parts = alpha
        beta

Many developers created extensions for buildout.
Zusätzlich gibt es Buildout Erweiterungen die eigene Einstellungen brauchen. Damit es da keine Überschneidungen gibt, teilt man seine Konfiguration in Sektoren auf, eine Sektion beginnt mit dem Sektionsnamen in eckigen Klammern. Zu guter letzt verwenden einige Erweiterungen die gleichen Einstellungen, um diese dort wieder nutzen zu können, schreibt man keinen konkreten Wert sonderne eine Referenz auf das Ursprungsfeld.

* buildout.cfg

Wenn man buildout ausführt, sucht buildout zuerst nach dieser Datei.
Die Buildout Sektion vermischt hier Buildout Konfigurationen und
wichtige Parameter die von mehreren Erweiterungen verwendet werden.::

    extends =

Hier wird gesagt, welche weiteren Konfigurationsdateien noch geladen
werden. Die Reihenfolge ist wichtig!::

    http-address =

Der Port auf dem Plone laufen wird.::

    effective-user =
    eggs =

Die Softwarepakete die wir haben wollen. Hier kommen die
Erweiterungen rein.::

    develop =

Hier müssen links rein auf die Verzeichnisse in denen der Quelltext
eigener Pakete sind.

parts =

Ich habe bisher den Begriff Erweiterung verwendet für die
Erweiterungen, in buildout heissen sie aber in wirklichkeit recipes.
Wie ein Rezept kann man dann weitere Dinge installieren lassen.
Wenn man tatsächlich ein Recipe einmal oder mehrfach verwendet,
nennt man die Sektion einen Part.

Hier trägt man ein, welche Parts tatsächlich verwendet werden
sollen. Wenn man einen Part geschrieben hat, und nach einem buildout
ist nicht das passiert, was man erwartet hat, liegt es
wahrscheinlich daran, das man vergessen hat, diesen Part
einzutragen.

[versions]

Wichtig und nervig zu gleich.

Wenn man ein Softwarepaket braucht, schreibt man nur den Namen, und
buildout versucht, das aktuellste Egg zu holen.

Wenn man auf einem neuen Rechner das selbe buildout zum ersten mal
laufen lässt, hat man deswegen im Zweifel anderne Code, und wundert
sich, warum das Plone auf dem einen Rechner läuft und auf dem
anderen nicht. Um das zu vermeiden, muss man immer alle Versionen
runter schreiben. Der Unifiedinstaller hat eine Buildouterweiterung,
welche alle Pakete auflistet, bei denen man kein Versionspinning
gemacht hat. das kann man direkt kopieren.

In diese Datei trägt man diese Pakete übrigens nicht ein.

* base.cfg

Hier ist die grundlegende Plone Struktur eingetragen, wobei alle
Werte die man vielleicht ändern wollen würde aus der [buildout]
Sektion geholt werden. Diese wurde in buildout.cfg zusammengestellt.

* versions.cfg

Hier werden alle Versionen gepinnt. In diesen Dateien trägt man
normalerweise eigene Versionen ein.
Diese ganzen Dateien werden normalerweise von Zope/Plone auf einem
Webserver bereitgestellt. Die Dateien haben alle einen
auskommentierten Link auf die Quelle. Man kann diese URLs auch
direkt auskommentieren und auf die neuesten Plone Versionen zeigen
lassen.

* development.cfg

Diese Datei hat die gleiche Aufgabe wie buildout.cfg. Buildout.cfg
konfiguriert das Plone so, wie man es Produktiv verwenden sollte,
develop.cfg konfiguriert es so, wie es einem Entwickler hilft.

Everybody hates buildout, but there is nothing better.
Zope 2.7 was 7 MB big, thats the size of django nowadays btw.
When eggs came around, the zope community decided to hop on the bandwagon.
Make zope smaller, better defined components and all that.
Now development can go on faster, because you modify a smaller subset of the code.
Ok, now, which version is safe to use for your plone?
Plone uses about 300 Packages, all packages get new versions on their own.
Package a requires package b, but at least version 3. Package c requires
Package b, but at most version 4. Version 5 is current. This gets a mess,
but there is a solution, buildout.
Buildout will download all required eggs, check the dependencies and get the
right version of everything.
The tool is quite configurable, as such, people not only use it to download
eggs, but also to set up infrastructure. Create config files, compile a custom
version of xml, install and configure varnish, create a zope instance, and so on.
Another type of extension allows whole new functionality, like mr.developer, an
awesome way to manage your checked out sources.

You use buildout by writing a configuration file. It has an ini like style.
The configuration consists of sections, the meaning of a section is given by a recipe. There is a special buildout section, it does not declare its recipe, but other general things. Lets checkout the minimal buildout to get an example.

You see here only one part, and it declares its recipe. This is the standard recipe to create a zope instance. Each recipe is an egg, and the recipe name is the egg name. As such, you can find recipes on pypi. There is something else you should know. Everybody has his preferred default settings that he wishes to use in every buildout. You can declare this in a special file. Every time, buildout parses the buildout configuration, it also looks for ~/.buildout/default.cfg

This is the perfect place to declare cache locations. Running a buildout without such a cache directory, the first time buildout runs, it needs more than half an hour because it has to get all these eggs. By declaring all these caches, things are much much faster.

Your virtualenv already has a very special location for the caches. The point it to the directories of the unified installer. This safes us half an hour now.

We already created an, egg, lets use it. But we will not use it as an egg, we use it as a source checkout. A source checkout is like an opened egg, you can easily modify the egg. Not everything gets reloaded automatically, but some things.
While buildout lets you use source checkouts directly, there is a buildout extension thats much more sophisticated and useful, mr.developer.
With mr.developer, you can declare, which packages you want to check out from which version control system and which repository url. You can check out sources from git, svn, bzr, hg, whatever. Also, you can say that some source are in your local file system.
mr.developer comes with a command, ./bin/develop. You can use it to update your code, to check for changes and so on. You can activate and deactivate your source checkouts. If you develop your extensions in eggs with separate checkouts, which is a good practice, you can plan releases by having all source checkouts deactivated, and only activate them, when you write changes that require a new release. You can activate and deactivate eggs via the develop command or the buildout configuration. You should always use the buildout way. Your commit serves as documentation.

Now, we want to install something very important, the omelette recipe. This thing creates a very very convenient way to access all used source code. It creates a lot of symlinks to point to the real file. We will see this in more detail later. There is something special we have to take care of. Ourbuildout directory is in the shared directory, and unfortunately this does not work will a number of things, one of them is our omelette.

Lastly, later during the tutorial, we will create our own egg, for this we need a to install a program. We use another part for this. zc.recipe.egg

SHOW WEBSITE
So we do not use the defaults, but change our path.
Here you see some important property, you can reference data from other sections. This is an important property, on a big site you might have multiple zope instance with only minor differences. You can define the minor differences and pull in the general settings from a template section. This way you only need to change variables in one place.
Or, even better, if you define services that work together, you can reference each others listening interfaces. So an nginx gets the port information from the buildout.

You see, buildout is very versatile, so lets get to the warnings. It is very easy to overdo with GenericSetup, what is too much and what isn't is hard to say, some people make deployments from their buildouts, some prefer, not to do that.
Be careful how far you buy the buildout mindset. Supervisor is a program to manage running servers, its pretty good. There is a recipe for it.
SHOW WEBSITE. The configuration is more complicated than the supervisor configuration itself! By using this recipe, you force others to understand the recipes specific configuration syntax AND the supervisor syntax. For such cases, collective.recipe.template might be a better match. It just iflls the variables ofa  given configuration template.

Another problem is error handling. Buildout sucks balls at error handling. You get in a weird dependency? Buildout will not tell you, where it is coming from. There is a bad egg? Your newborn gives more helpful messages after consuming a bad egg.
If there is a problem, you can always run buildout with -v, to get more verbose output, sometimes it help. If strange egg versions are requested, check the dependencies declaration of your eggs and your version pinnings. There is NO warning if uppercase and lowercase typing do not match, and for some parts of the code the casing is not an issue. Check out the ordering of your extends, use the annotate command of buildout, to see if it interprets your configuration differently. Restrict yourself to simple buildout files. You can reference variables from other sections, but you can also use a section as a whole template. We learned that this does not work well with complex hierarchies and abandoned that feature.

