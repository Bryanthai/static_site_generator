import os
import shutil
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
from convert import *

def check_path():
    if not os.path.exists("public"):
        raise Exception("Public path does not exist")
    return

def initialize(current_path):
    content_list = os.listdir(os.path.join("static", current_path))
    for content in content_list:
        static_content = os.path.join("static", current_path,  content)
        if os.path.isdir(static_content):
            public_path = os.path.join("public", current_path, content)
            os.mkdir(public_path)
            initialize(os.path.join(current_path, content))
        else:
            public_path = os.path.join("public", current_path, content)
            shutil.copy(static_content, public_path)
    return

def nuke_public_initialize():
    shutil.rmtree("public")
    os.mkdir("public")
    return

def generate_page(from_path, template_path, dest_path):
    print(f"GENERATING PAGE FROM {from_path} TO {dest_path} USING {template_path}")
    f = open(from_path, "r")
    from_content = f.read()
    t = open(template_path, "r")
    template_content = t.read()
    root_node = markdown_to_html_node(from_content)
    html_content = root_node.to_html()
    html_title = extract_title(from_content)
    title_change = re.sub("{{ Title }}", html_title, template_content)
    content_change = re.sub("{{ Content }}", html_content, title_change)
    check_path()
    d = open(dest_path, "w")
    d.write(content_change)
    return

def main():
    nuke_public_initialize()
    initialize("")
    generate_page("content/index.md", "template.html", "public/index.html")


main()