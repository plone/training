---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Writing Custom Blueprints

The mr.bob templates provides an Example Blueprint to serve as a starting point for you.
It is commented out in the pipeline.
Uncommenting (removing the `#`) will include the custom blueprint in the pipleline.

Three files need to be updated to hook up a custom blueprint:
: - Write the blueprint in `blueprints.py`.
  - Define the blueprint in the `configure.zcml`.
  - Add the step to `import_content.cfg` pipeline. The name of the blueprint will match what was set in the configure.zcml.

You will need to determine where your step should appear in the pipeline.
If you need to manipulate the exported data or decide whether or not to import an item based on its data,
it should go before the `constructor`.
If you need to manipulate an object once it is in the Plone site,
the step should go towards the end, after the `schemaupdater`.

The blueprint itself generally has two parts, the `__init__`, and the `__iter__`.
The `__init__` sets up the variables based on the current item in the loop and any arguments passed in the pipeline.
The `__iter__` is where most of your custom code will go.

## Basic Blueprint Tips

- Don't use `return`.
  `__iter__` code should end with a `continue`,
  but you also need to `yield item` to push it forward in the pipeline.
  If you don't `yield item` at the very end or before a continue, the item will not get imported.
  Note that sometimes you don't want to import the item, in which case you can `continue` without the `yield`.

- Always check that the key you are manipulating or accessing is present in the item.
  For example, you can bail out of the blueprint once it realizes the data it needs isn't there:

  ```python
  path = item.get('_path')
  if not path:
      yield item
      continue
  # ...
  ```

- If your step needs to manipulate an object in the site after the `constructor` has created it,
  you can get the object with the following code.
  Your step will need to be placed after the `constructor` in the pipeline,
  since the object does not exist in the Plone site before this point.

  ```python
  from Products.CMFPlone.utils import safe_unicode
  # ...
  obj = self.context.unrestrictedTraverse(
      safe_unicode(item['_path'].lstrip('/')), None)
  ```

- If you like to keep track of all the information about what happens during the import,
  (which can be very useful for debugging later),
  add the information to the logs!

  At the top of the file:

  ```python
  import logging
  logger = logging.getLogger("Transmogrifier")
  ```

  You can set the 'Transmogrifier' text to anything,
  this is what will be prepended to the log message.
  Then in your blueprint:

  ```python
  logger.info("[item skipped] %s due to %s", itempath, failreason)
  ```

  This example assumes you have defined variables for `itempath`, the path to the current item,
  and `failreason`, which could be a condition for why you are not importing an item.
  This log message is fully customizable for what you want it to say.

## Practice

Let's create a blueprint that will only import content modified in the last few years.
This can be useful if you want to clean out the older content in your site.

You can start by copying the entire Example blueprint, and pasting a copy in the same file.

Change the name of the class to `ImportNew`.
Leave everything in the `__init__`, but take everything out of the `__iter__` except for:

```python
def __iter__(self):
    for item in self.previous:
        yield item
```

From here we can start adding our custom code and conditions.
We want to check against the `modified` date,
so open a couple of the exported json files to see what the key is called.
If you are using a jsonify export, you will likely find:

```console
"modification_date": "2017/03/23 12:53:12.608745 GMT-4",
```

Note that your `modification_date` may not look exactly like this one,
and keep in mind that they may not even be consistent throughout your export!

Add some code that checks if the current item has a modification_date, and assigns it to a variable:

```python
mod_date = item.get('modification_date')
if not mod_date:
    yield item
    continue
```

```{note}
Why would an item not have a modification date?
You may end up importing more than basic Plone objects,
but also information like user roles and groups.
These won't have a modification date,
but we still want to yield the item to push it further down the pipleline to a blueprint that handles them.
```

From here, you can determine how you want to check if the item was from the last 5 years.
Like any other value you pull from the `item`, `mod_date` is a string.
You can convert it to a DateTime object to do a comparison,
or you could also take the first 4 characters of the string to get the year.

The path you take is determined by what is best for your data and your situation.
If you plan on using this migration code multiple times,
you'll want it to be more dynamic,
Otherwise you could make it static, by explicitly adding a condition like this:

```python
mod_year = int(mod_date[:4])
if mod_year < 2015:
    continue
```

Notice this does not include the `yield item`,
because we don't want to keep any content older than 2015.
Continuing without yielding the item will not push it through the rest of the pipleine.

Let's also add a log message to show that the item is being skipped:

```python
import logging
logger = logging.getLogger("Transmogrifier")
# ...
mod_year = int(mod_date[:4])
if mod_year < 2015:
    item_path = item.get('_path', '')
    logger.info('[skipped] %s with modified year %s', item_path, mod_year)
    continue
```

Once you are satisfied with your code and conditions,
make the `yield item` line is at the very end
to import all content from the last 5 years.

Now we can hook up the blueprint.
Open the `configure.zcml` found in the same folder as `blueprints.py`, and add a new utility:

```html
<utility
    component=".blueprints.ImportNew"
    name="ploneconf.import_new"/>
```

The `component` points to the `ImportNew` class we created in `blueprints.py`.
The `name` can be anything you want.
It's good practice to use the package name, with the name of the class, but in lowercase letters.

Now this can be added to the pipeline.

In `import_content.cfg` under the `[transmogrifer]` section at the top,
add `import_new` after `jsonsource`, but before the `constructor`.
`jsonsource` should always be the first item in the pipeline.
We don't want an object created for the older items not being imported,
so this is why we want our new step to run before the `constructor`.

Then further down in the file, you can add the new part:

```ini
[import_new]
blueprint = ploneconf.import_new
```

The name of the blueprint is what we set in the configure.zcml.
No other parameters need to be added,
unless you specifically wrote your blueprint to take additional information.
This is covered more in {doc}`advanced-blueprint`.

Restart (or start) your instance.
If you don't have syntax errors, your new blueprint is hooked up and ready for testing!
Head into the next section, {doc}`import`, to learn how to import the content into your site.
