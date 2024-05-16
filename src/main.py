import os
import shutil

from copystatic import copy_files
from page_generator import generate_page, generate_pages_recursive

root_path = os.getcwd()
static_path = os.path.join(root_path, r"static")
public_path = os.path.join(root_path, r"public")

def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    print(root_path, static_path, public_path, end="\n")
    if not os.path.exists(static_path):
        raise ValueError("No Static directory found.")
    if len(os.listdir(static_path)) == 0:
        raise ValueError(f"No Files found in static folder: {static_path}")
    copy_files(static_path, public_path)
    source_path = os.path.join(root_path, "content")
    template_path = os.path.join(root_path, "template.html")
    #dest_path = os.path.join(public_path, "index.html")
    dest_path = public_path
    
    generate_pages_recursive(source_path, template_path, dest_path)
    
main()