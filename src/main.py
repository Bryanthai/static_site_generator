import os
import shutil
import sys
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode
from convert import *

def initialize(current_path):
    content_list = os.listdir(os.path.join("static", current_path))
    for content in content_list:
        static_content = os.path.join("static", current_path,  content)
        if os.path.isdir(static_content):
            public_path = os.path.join("docs", current_path, content)
            os.mkdir(public_path)
            initialize(os.path.join(current_path, content))
        else:
            public_path = os.path.join("docs", current_path, content)
            shutil.copy(static_content, public_path)
    return

def nuke_public_initialize():
    if os.path.isdir("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    return

def generate_page(from_path, template_path, dest_path, base_path):
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
    href_change = re.sub("href=\"", f"href=\"{base_path}", content_change)
    src_change = re.sub("src=\"", f"src=\"{base_path}", href_change)
    d = open(dest_path, "w")
    d.write(src_change)
    return

def generate_page_recursive(template_path, base_path, current_path):
    content_list = os.listdir(os.path.join("content", current_path))
    for content in content_list:
        static_content = os.path.join("content", current_path,  content)
        if os.path.isdir(static_content):
            public_path = os.path.join("docs", current_path, content)
            os.mkdir(public_path)
            generate_page_recursive(template_path, base_path, os.path.join(current_path, content))
        elif static_content.endswith(".md"):
            html_content = re.sub(".md", ".html", content)
            public_path = os.path.join("docs", current_path, html_content)
            generate_page(static_content, template_path, public_path, base_path)
    return

def main():
    if len(sys.argv) < 2:
        base_path = ""
    else:
        base_path = sys.argv[1]
    nuke_public_initialize()
    initialize("")
    generate_page_recursive("template.html", base_path, "")


main()