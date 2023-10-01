from nuclia import sdk
from nucliadb_sdk.v2.exceptions import NotFoundError
import json
import glob
import hashlib
import os
import re


# that's actually an API key, not a NUA one
# but that's the name of the variable on our GitHub repo
API_KEY = os.environ["DEPLOY_NUCLIA_TOKEN"]
KB = os.environ["DEPLOY_NUCLIA_URL"]
PUBLIC_URL = "https://training.plone.org/"


def generate_nuclia_sync():
    result = {"docs": {}}
    for doc in glob.glob("./docs/**/*.md", recursive=True):
        hash = hashlib.md5(open(doc, "rb").read()).hexdigest()
        result["docs"][doc] = hash
    return result


def extract_first_heading(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # The pattern matches lines starting with one or more hash symbols followed by any non-empty text
    pattern = r'^\s*#+\s+(.+)$'
    match = re.search(pattern, content, re.MULTILINE)

    if match:
        # Removing backticks
        heading = match.group(1).replace('`', '').strip()
        return heading

    # If no heading is found
    return None


# re.sub() is used to perform substitution
# r'[\W_]+' matches any non-word characters (including underscores),and replaces them with a single hyphen '-'
# strip('-') removes any leading or trailing hyphens from the resulting string
get_slug = lambda path: re.sub(r'[\W_]+', '-', path.lower().strip()).strip('-')


def normalize_path(path):
    return path.replace('.md', '').replace('./docs', '').lstrip('/')


def create_url(origin_url, url_path):
    return f"{origin_url.rstrip('/')}/{url_path}"


def generate_breadcrumb_for_path(path):
    breadcrumb = []
    temp_path = "./"
    path_items = path.split('/')[1:]

    for path_item in path_items:
        temp_path = os.path.join(temp_path, path_item)
        if temp_path.endswith(".md"):
            heading = extract_first_heading(temp_path)
            new_data = {"url":create_url(
                PUBLIC_URL, normalize_path(temp_path)),"label":heading}
        else:
            index_md_path = os.path.join(temp_path, "index.md")
            if os.path.exists(index_md_path):
                heading = extract_first_heading(index_md_path)
                new_data = {"url":create_url(
                PUBLIC_URL, normalize_path(temp_path)),"label":heading}
            else:
                continue
        # Check if the new_data entry already exists in the breadcrumb
        if new_data not in breadcrumb:
            breadcrumb.append(new_data)
    return {"breadcrumbs": breadcrumb}


def upload_doc(path):
    slug = get_slug(path)
    title = extract_first_heading(path)
    origin_url = f"{PUBLIC_URL}{path.replace('.md', '').replace('./docs/', '')}"  # noqa
    sdk.NucliaUpload().text(
        path=path,
        format="MARKDOWN",
        slug=slug,
        field="page",
        title=title,
        url=KB,
        api_key=API_KEY,
        origin={"url": origin_url},
        extra={"metadata": generate_breadcrumb_for_path(path)},
    )


def delete_doc(path):
    slug = get_slug(path)
    print(f"Deleting {slug}")
    kb = sdk.NucliaKB()
    try:
        res = kb.get_resource_by_slug(slug=slug, url=KB, api_key=API_KEY)
        kb.delete(
            rid=res.id,
            url=KB,
            api_key=API_KEY,
        )
    except NotFoundError:
        pass


def sync():
    # Get all pages uploaded and last sync
    with open("./docs/_static/nuclia_sync.json", "r") as sync_info:
        old_data = json.load(sync_info)
    new_data = generate_nuclia_sync()

    to_delete = []
    for doc, _ in old_data["docs"].items():
        if doc not in new_data["docs"]:
            to_delete.append(doc)

    for doc, hash in new_data["docs"].items():
        if doc not in old_data["docs"]:
            upload_doc(doc)
        elif hash != old_data["docs"][doc]:
            upload_doc(doc)

    for doc in to_delete:
        delete_doc(doc)

    with open("./docs/_static/nuclia_sync.json", "w") as sync_info:
        json.dump(new_data, sync_info)
    print("Remember to do a make upload-sync to make sure we update status")


if __name__ == "__main__":
    sync()
