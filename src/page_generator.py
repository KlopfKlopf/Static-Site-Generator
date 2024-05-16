import os
from pathlib import Path
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.split(" ",1)[1]
        else:
            raise Exception("No title found. Please add a title to the page.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_content = ""
    with open(from_path) as sourcefile:
        source_content += sourcefile.read()
    template_content = ""
    with open(template_path) as templatefile:
        template_content += templatefile.read()
    
    html_content = markdown_to_html_node(source_content).to_html()
    title = extract_title(source_content)

    generated_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, 'w') as htmlfile:
        htmlfile.write(generated_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(source_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(source_path, template_path, dest_path)
        else:
            generate_pages_recursive(source_path, template_path, dest_path)
        
        