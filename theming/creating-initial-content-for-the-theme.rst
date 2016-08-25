.. _creating-initial-content-for-the-theme:

======================================
Creating initial content for the theme
======================================

Our theme relies on some initial content structure,
specifically the :file:`slider-images` folder with some images inside.
Let's improve our theme package to create this content on install.

To do that we create the :file:`slider-images` folder in our :file:`setuphandlers.py`
and load also some example images into that folder.

We have the needed images inside ``theme/img`` folder. To create the folder and the immages put the following code in your setuphandlers.py.

.. code-block:: python

   from plone import api
   import os


   def post_install(context):
       """Post install script"""
       portal = api.portal.get()
       _create_content(portal)


   def _create_content(portal):
       if not portal.get('slider-images', False):
           slider = api.content.create(
               type='Folder',
               container=portal,
               title=u'Slider',
               id='slider-images'
           )
           for slider_number in range(1, 4):
               slider_name = u'slider-{0}'.format(str(slider_number))
               slider_image = api.content.create(
                   type='Image',
                   container=slider,
                   title=slider_name,
                   id=slider_name
               )
               slider_image.image = _load_image(slider_number)
           # NOTE: if your plone site is not a vanilla plone
           # you can have different workflows on folders and images
           # or different transitions names so this could fail
           # and you'll need to publish the images as well
           # or do that manually TTW.
           api.content.transition(obj=slider, transition='publish')


   def _load_image(slider):
       from plone.namedfile.file import NamedBlobImage
       filename = os.path.join(os.path.dirname(__file__), 'theme', 'img',
                               'slide-{0}.jpg'.format(slider))
       return NamedBlobImage(
           data=open(filename, 'r').read(),
           filename=u'slide-{0}.jpg'.format(slider)
       )


   def uninstall(context):
       """Uninstall script"""
       if context.readDataFile('plonethemetango_uninstall.txt') is None:
           return
           # Do something during the uninstallation of this package

.. note::

  After adding this code to the setuphandlers.py, we need to restart Plone
  and uninstall/install our theme package.
