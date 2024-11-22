from nuclia import sdk
from nucliadb_sdk.v2.exceptions import NotFoundError
import json
import glob
import hashlib
import os
import re
from bs4 import BeautifulSoup


# that's actually an API key, not a NUA one
# but that's the name of the variable on our GitHub repo
API_KEY = os.environ["DEPLOY_NUCLIA_TOKEN"]
KB = os.environ["DEPLOY_NUCLIA_URL"]
PUBLIC_URL = "https://training.plone.org/"


def generate_nuclia_sync():
    """
    Generate a dictionary of HTML files and their MD5 hashes.

    Args:
        None

    Returns:
        dict: A dictionary of HTML files and their MD5 hashes.
    """
    result = {"docs": {}}
    for doc in glob.glob("./_build/html/**/*.html", recursive=True):
        
        # Skip pages that don't need to be indexed
        if any(skip in doc for skip in ['search.html', 'genindex.html','webpack-macros.html']):
            continue

        hash = hashlib.md5(open(doc, "rb").read()).hexdigest()
        result["docs"][doc] = hash
    return result


def extract_content(file_path):
    """
    Extract title and content from HTML file using BeautifulSoup.

    Args:
        file_path (str): The path to the HTML file.
    
    Returns:
        tuple: A tuple containing the title and content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    # Extract title
    title = soup.find('h1').get_text()

    # Extract content
    article = soup.find('article', class_='bd-article')
    if not article:
        return None, None
    
    return title, article


def get_slug(path):
    """
    Extract slug from path.

    Args:
        path (str): The path to the HTML file.
    
    Returns:
        str: The slug.
    """
    path = path.replace('./_build/html/', '')
    path = re.sub(r'\.html$', '', path)
    slug = re.sub(r'[\W_]+', '-', path.lower().strip()).strip('-')
    return slug


def transform_path_to_url(path, base_url):
    """
    Transform a file path to a URL.

    Args:
        path (str): The path to the HTML file.
        base_url (str): The base URL.
    
    Returns:
        str: The transformed URL.
    """
    transformed_path = '/'.join(
        part for part in path.replace('./_build/html/', '').split('/')
    )
    return f"{base_url.rstrip('/')}/{transformed_path}"


def generate_breadcrumb_for_path(path):
    """
    Generate breadcrumbs for a given HTML file path.

    Args:
        path (str): The path to the HTML file.
    
    Returns:
        dict: A dictionary containing breadcrumbs.
    """
    breadcrumb = []
    relative_path = path.replace('./_build/html/', '').split('/')
    current_path = ''

    for i, path_item in enumerate(relative_path):
        is_file = path_item.endswith('.html') and i == len(relative_path) - 1
        
        if is_file:
            current_path += path_item
        else:
            current_path += path_item + '/'
        
        try:
            if not is_file:
                index_path = os.path.join('./_build/html/', current_path, 'index.html')
            else:
                index_path = os.path.join('./_build/html/', current_path)
            
            with open(index_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
            title = soup.find('h1')
            label = title.get_text() if title else path_item
            
            new_data = {
                "url": transform_path_to_url(current_path.rstrip('/'),PUBLIC_URL),
                "label": label
            }

            if new_data not in breadcrumb:
                breadcrumb.append(new_data)

        except (FileNotFoundError, AttributeError):
            continue
    return {"breadcrumbs": breadcrumb}

def upload_doc(path):
    """
    Upload a page to Nuclia Knowledge Base.

    Args:
        path (str): Path to the HTML file.
    
    Returns:
        None
    """
    slug = get_slug(path)
    title, article = extract_content(path)
    origin_url = transform_path_to_url(path, PUBLIC_URL)
    sdk.NucliaUpload().text (
        path=path,
        format="HTML",
        slug=slug,
        field="page",
        title=title,
        url=KB,
        api_key=API_KEY,
        origin={"url": origin_url},
        extra={"metadata": generate_breadcrumb_for_path(path)},
        metadata={"content": article},
    )


def delete_doc(path):
    """
    Delete a page from Nuclia Knowledge Base.

    Args:
        path (str): Path to the HTML file.
    
    Returns:
        None
    """
    slug = get_slug(path)
    print(f"Deleting {slug}")
    res = sdk.NucliaResource()
    try:
        res.delete(
            slug=slug,
            url=KB,
            api_key=API_KEY,
        )
    except NotFoundError:
        pass


def sync():
    """
    Sync Changes with Nuclia Knowledge Base and dump data in nuclia_sync.json

    Args:
        None

    Returns:
        None
    """
    if os.path.exists("./docs/_static/nuclia_sync.json"):
        try:
            with open("./docs/_static/nuclia_sync.json", "r") as sync_info:
                old_data = json.load(sync_info)
        except json.JSONDecodeError:
            old_data = {"docs": {}}
    else:
        old_data = {"docs": {}}

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
        json.dump(new_data, sync_info, indent=4)
    print("Remember to do a make upload-sync to make sure we update status")


if __name__ == "__main__":
    sync()
