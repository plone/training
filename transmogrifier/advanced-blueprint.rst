=======================
Advanced Blueprint Tips
=======================

Iterator Stages
---------------

https://docs.plone.org/external/collective.transmogrifier/docs/source/transmogrifier.html#iterators-have-3-stages


Migrating Users & Groups
------------------------

Jsonify will not export user and group information.
These will need to be exported separately.
See `Users Migration <users-migration.html>`_ for example code.


Updating Rich Text
------------------

When updating your sites, you may have add-ons that will change in the process.
This can adjust text that appears in the body text of pages.
Check out `PyQuery <https://pypi.org/project/pyquery>`_ to help parse the HTML for you.
Here's an example that updates oembed tags to `uwosh.snippets <https://pypi.org/project/uwosh.snippets/>`_ style:

.. code:: python

   def new_snippet(self, itemuid):
        return '<span class="snippet-tag snippet-tag-html_snippet" \
            contenteditable="false" data-type="snippet_tag" \
            data-snippet-id="{0}" data-header="">\
            Snippet:[ID={0}]</span>'.format(itemuid)

    def __iter__(self):
        for item in self.previous:
            if 'text' not in item:
                yield item
                continue
            if 'oembed oembed-responsive' not in item['text']:
                yield item
                continue
            txt = PyQuery(item['text'])
            full_text = txt.html()
            for snippet in txt(".oembed"):
                link = PyQuery(snippet)
                href = link("a").attr("href")
                if not href:
                    continue
                if 'resolveuid' in href:
                    linkuid = href.replace('resolveuid/', '')
                    if not api.content.get(UID=linkuid):
                        # leave link as is if we can't find the new one
                        continue
                    # replace link with new snippet
                    full_text = full_text.replace(PyQuery(snippet).outer_html(), self.new_snippet(linkuid))
                else:
                    html_snippets = api.content.find(path='/Plone/' + href)
                    if not html_snippets:
                        continue
                    new = self.new_snippet(html_snippets[0].UID)
                    full_text = full_text.replace(PyQuery(snippet).outer_html(), new)
            item['text'] = full_text


Taking parameters in custom blueprints
--------------------------------------