from textnode import TextNode, TextType
from generate_page import generate_pages_recursive
import os
import shutil
import sys

default_basepath = "/"

#print("hello world")

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    items = os.listdir(source_dir)
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            copy_static(source_path, dest_path)


def main():
    my_node = TextNode("wizard", TextType.BOLD, "https://bear.com")
    print(my_node)

    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists("public"):
        shutil.rmtree("public")

    copy_static("static", "public")
    print("Static files successfully copied to public directory")

    generate_pages_recursive("content", "template.html", "./docs", basepath)

if __name__ == "__main__":
    main()