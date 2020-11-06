Wouldn't it be nice if we could have a way to customize, per column, how the
values are rendered and go even further then the ``textTemplate`` field would
allow?

Let's create the following extension mechanism: for any column, we'll be able
to choose between available "cell renderers". These would be components that
get passed the value and can render themselves as they want.

For example, let's implement a "progress bar" that could be used to render
a percentage column. Now, we could use the global ``config.settings`` object to
register the new cell renderers, but for now let's just use the block's config
object. Other projects or addons can then tweak that block config to register
new renderers.
