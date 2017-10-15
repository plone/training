Sessions
========

Our goal is to create a middleware that stores information in some kind of
a persistant storage. For simplicity we start by writing this infromation
to a file on a disk, but this can easily be extended to a Redis storgae,
MongoDB or any database of your liking.
Let's assume though that session data is unstructured might look like
a dictionary of session ID as keys, with values which are another dictionary:

.. code:: python

   sessions = {
        "id1": {'data': {'k1': 'v1', 'k2': 'v2', ..., 'kn': 'vn'}},
        "id2": {'data': {'ka1': 'va1', 'ka2': 'va2', ..., 'kan': 'van'}},
        ...
        }

To make our session store easy to as if it was a dictionary, we implement
out middleware by crafting a class which behaves like that. For that purpose,
we are taking a small diversion from WSGI to Python's Data Model.

