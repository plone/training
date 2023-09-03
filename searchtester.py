import json
import os
from upload import extract_first_heading, PUBLIC_URL

# Load nuclia_sync.json
try:
    with open("./docs/_static/nuclia_sync.json", "r") as sync_info:
        nuclia_sync_data = json.load(sync_info)
except FileNotFoundError:
    print("Error: nuclia_sync.json not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")


def normalize_path(path):
    return path.replace('.md', '').replace('./docs', '').lstrip('/')


def create_url(origin_url, url_path):
    return f"{origin_url.rstrip('/')}/{url_path}"


def generate_breadcrumb_for_path(path):
    breadcrumb = {}
    temp_path = "./"
    path_items = path.split('/')[1:]

    for path_item in path_items:
        temp_path = os.path.join(temp_path, path_item)
        if temp_path.endswith(".md"):
            heading = extract_first_heading(temp_path)
            breadcrumb[heading] = create_url(
                PUBLIC_URL, normalize_path(temp_path))
        else:
            index_md_path = os.path.join(temp_path, "index.md")
            if os.path.exists(index_md_path):
                heading = extract_first_heading(index_md_path)
                breadcrumb[heading] = create_url(
                    PUBLIC_URL, normalize_path(temp_path))
            temp_path = os.path.join(temp_path, "")
    return breadcrumb


result = {"heading_to_breadcrumb": {}}
for md_path in nuclia_sync_data["docs"]:
    heading = extract_first_heading(md_path)
    breadcrumb = generate_breadcrumb_for_path(md_path)
    result["heading_to_breadcrumb"][heading] = breadcrumb


try:
    with open("./docs/_static/heading_to_breadcrumb_mapping.json", "w") as mapping_file:  # noqa
        json.dump(result, mapping_file, indent=4)
    print("Data written to heading_to_breadcrumb_mapping.json.")
except Exception as e:
    print(f"Error writing JSON: {e}")
