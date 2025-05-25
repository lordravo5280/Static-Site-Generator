from markdown_parser import markdown_to_html_node
from extract import extract_title
from pathlib import Path

import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as markdown_file:
        m_content = markdown_file.read()
    with open(template_path, 'r') as template:
        t_content = template.read()
    html_nodes = markdown_to_html_node(m_content)
    title = extract_title(m_content)
    html_final = html_nodes.to_html()
    result = t_content.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", html_final)
    result = result.replace('href="/', 'href="' + basepath)
    result = result.replace('src="/', 'src="' + basepath)

    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)
    with open(dest_path, 'w') as full_html:
        full_html.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)