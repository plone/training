# !/usr/bin/python

import os
metadata_check = """---
html_meta:
"""
metadata = """---
html_meta:
  "description": ""
  "property=og:description": ""
  "keywords": ""
---

"""
for root, dirs, files in os.walk("./docs"):
    for name in files:
        if name.endswith(".md"):
            filename = os.path.join(root, name)
            # print(filename)
            with open(filename, 'r+') as f:
                data = f.read()
                if not data.startswith(metadata_check):
                    f.seek(0)
                    f.write(metadata)
                    f.write(data)
                    print(f"{filename} html_meta prepended.")
